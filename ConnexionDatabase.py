import keyring
import pandas
from sqlalchemy import create_engine


class SqlQuery:

    def __init__(self, query):
        self.query = query
        self.host = "data-db.enercoop.infra"
        self.database = keyring.get_password("system", "database")
        self.user = keyring.get_password("system", "username")
        self.pwd = keyring.get_password("system", "password")
        self.port = 5432

    def pandas_sql(self):
        engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(self.user, self.pwd, self.host, self.port,
                                                                    self.database),
                               execution_options=dict(stream_results=True))
        data = pandas.read_sql_query(self.query, engine)

        return data

    def pandas_sql_chunk(self, chunksize):
        engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(self.user, self.pwd, self.host, self.port,
                                                                    self.database),
                               execution_options=dict(stream_results=True))
        for df_chunk in pandas.read_sql_query(self.query, engine, chunksize=chunksize):
            yield df_chunk
        engine.dispose()  # closes the thread

    @staticmethod
    def read_csv(chemin, file):
        data = pandas.read_csv(chemin + file)

        return data


def main():
    data = SqlQuery('select * from producteurs limit 100')
    # print(data.pandas_sql())
    print(data.pandas_sql_chunk(10))


if __name__ == "__main__":
    main()
