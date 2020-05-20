#! /usr/bin/env python3
# coding: utf-8

""" hote = data-db.enercoop.infra
    user name = polen
    database = polen
    mot de passe = kSnRLvf0KB32M0m
"""
import pandas
import psycopg2
import os


class SqlQuery:

    def __init__(self, query):
        self.query = query
        self.host = "data-db.enercoop.infra"
        self.dbname = "polen"
        self.user = "polen"
        self.pwd = "kSnRLvf0KB32M0m"
        self.port = 5432

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
        conn = psycopg2.connect(database="polen",
                                user="polen",
                                host="data-db.enercoop.infra",
                                password="kSnRLvf0KB32M0m",
                                port=5432)

        # Create a cursor. The cursor allows you to execute database queries.
        cur = conn.cursor()

        # Testing
        cur.execute(query)
        data = pandas.DataFrame(cur.fetchall())

        # Close connection
        conn.close()

        return data

    def query_psql(self): # TODO corriger cette fonction qui ne marche pas
        conn = psycopg2.connect("host='{}' port={} dbname='{}' user={} password={}".format(self.host, self.port, self.dbname, self.user, self.pwd))
        dat = sqlio.read_sql_query(self.query, conn)  # type: dataframe
        conn.close()
        return dat


    @staticmethod
    def read_csv(chemin, file):
        data = pandas.read_csv(chemin + file)

        return data


def main():
    # sql = SqlQuery()
    data = SqlQuery.query_psql("Select * from producteurs")
    data = SqlQuery.read_csv('SerieTemporelles/Data/', 'classeur.csv')
    print(data)
    # SqlQuery.yield_query_by_chunks("SELECT * FROM producteurs", 10, "polen", "kSnRLvf0KB32M0m", "data-db.enercoop.infra", 5432, "polen")


if __name__ == "__main__":
    main()
