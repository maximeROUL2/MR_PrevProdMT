import keyring
import pandas
from sqlalchemy import create_engine


""" 
ENTREE : une requête SQL et la connexion à la BDD d'enercoop du pôle énérgie
        
HYPOTHESES : Les mots de passe sont cryptées par la méthode keyring (https://pypi.org/project/keyring/)
             On souhaite avoir un dataFrame en sortie pour les traitements futur
             
SORTIES : pandas_sql : le data frame lié à la requête 
         pandas_sql_chunk : un dataframe par morceau pour un traitement optimisé
         read_csv : la lecture d'un csv à partir du chemin et du fichier
"""

class ConnexionDatabase:

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
    data = ConnexionDatabase('select * from producteurs limit 100')
    # print(data.pandas_sql())
    print(data.pandas_sql_chunk(10))


if __name__ == "__main__":
    main()
