import psycopg2



class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="proft",
            user="banco",
            password="tsc10012000@",
            host="186.226.56.84",
            port="5432"


        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, values=None):
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
