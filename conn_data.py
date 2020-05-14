""" hote = data-db.enercoop.infra
    user name = polen
    database = polen
    mot de passe = kSnRLvf0KB32M0m
"""
from sqlalchemy import create_engine
import psycopg2
import pandas


class SqlQuery:

    @staticmethod
    def yield_query_by_chunks(query, chunksize, pg_user, pg_pass, pg_host, pg_port, db_name):
        print("ok")
        engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(pg_user, pg_pass, pg_host, pg_port, db_name),
                               execution_options=dict(stream_results=True))
        for df_chunk in pd.read_sql_query(query, engine, chunksize=chunksize):
            yield df_chunk
        engine.dispose()  # closes the thread

    @staticmethod
    def simple_query_pyscopg2(query):
        print("ok")
        conn = psycopg2.connect(database="polen",
                                user="polen",
                                host="data-db.enercoop.infra",
                                password="kSnRLvf0KB32M0m",
                                port=5432)

        # Create a cursor. The cursor allows you to execute database queries.
        cur = conn.cursor()

        # Testing
        cur.execute(query)
        print(type(cur.fetchall()))
        print(len(cur.fetchall()))
        print(cur.fetchall())

        # Close connection
        conn.close()

    @staticmethod
    def read_csv(file):
        data = pandas.read_csv("data_db/" + file)

        return data



# sql = SqlQuery()
# SqlQuery.simple_query_pyscopg2("SELECT * FROM rp12 LIMIT 100")
# SqlQuery.yield_query_by_chunks("SELECT * FROM producteurs", 10, "polen", "kSnRLvf0KB32M0m", "data-db.enercoop.infra", 5432, "polen")

data = SqlQuery.read_csv("producteurs_2020_05_04.csv")