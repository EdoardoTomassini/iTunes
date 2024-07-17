from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAlbums(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT a.*, sum(t.Milliseconds/(1000*60)) as totD
                    from track t, album a 
                    where a.AlbumId =t.AlbumId 
                    group by a.AlbumId 
                    having totD > %s
                       """

        cursor.execute(query, (durata,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT DISTINCTROW t1.AlbumId as a1, t2.AlbumId as a2
                    FROM playlisttrack p1, track t1, playlisttrack p2, track t2
                    WHERE p2.PlaylistId = p1.PlaylistId
                    and p2.TrackId = t2.TrackId
                    and p1.TrackId = t1.TrackId 
                    and t1.AlbumId < t2.AlbumId 
                """

        cursor.execute(query)

        for row in cursor:
            #IMPORTANTE: verifico prima che i nodi esistano
            if row["a1"] in idMap and row["a2"] in idMap:
                result.append((idMap[row["a1"]], idMap[row["a2"]]))

        cursor.close()
        conn.close()
        return result



