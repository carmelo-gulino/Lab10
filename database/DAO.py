from database.DB_connect import DBConnect
from model.contiguity import Contiguity
from model.country import Country


class DAO:
    @staticmethod
    def get_all_countries():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select *
                    from country c """
        cursor.execute(query)
        countries = []
        for row in cursor:
            countries.append(Country(**row))
        cursor.close()
        cnx.close()
        return countries

    @staticmethod
    def get_contiguities(year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select *
                    from contiguity c 
                    where c.`year`<= %s
                    order by c.state1ab, c.state2ab """
        cursor.execute(query, (year,))
        result = []
        for row in cursor:
            result.append(Contiguity(**row))
        cursor.close()
        cnx.close()
        return result


if __name__ == '__main__':
    ctg = DAO.get_contiguities(2004)
    for c in ctg:
        print(c)
