from model.edge import Edge

from database.DB_connect import DBConnect
from model.country import Country


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNodes(anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []


        query = """select distinct c.*
                    from country c, contiguity co
                    where (c.CCode = co.state1no or c.CCode = co.state2no) 
                           and co.year <= %s and co.conttype > 0
                    order by c.StateAbb ASC"""

        cursor.execute(query, (anno, ))

        for row in cursor:
            res.append(Country(**row))

        cursor.close()
        conn.close()
        return res

    def getAllEdges(anno, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select distinct least(c.state1no, c.state2no) as c1, greatest(c.state1no, c.state2no) as c2
                    from contiguity c
                    where c.year <= %s and c.conttype = 1
                    group by c1, c2"""
        cursor.execute(query, (anno, ))
        for row in cursor:
            res.append(Edge(idMap[row["c1"]], idMap[row["c2"]]))

        cursor.close()
        conn.close()
        return res
