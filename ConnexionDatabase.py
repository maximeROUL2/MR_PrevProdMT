import io

import keyring
import pandas
from sqlalchemy import create_engine
import psycopg2


""" 
ENTREE : une requête SQL et la connexion à la BDD d'enercoop du pôle énérgie
        
HYPOTHESES : Les mots de passe sont cryptées par la méthode keyring (https://pypi.org/project/keyring/)
             On souhaite avoir un dataFrame en sortie pour les traitements futur
             Les formats d'écriture dans la base de données doivent être respecter en amont 
             
SORTIES : pandas_sql : le data frame lié à la requête 
         pandas_sql_chunk : un dataframe par morceau pour un traitement optimisé
         read_csv : la lecture d'un csv à partir du chemin et du fichier
         write_database : inserer une data_frame dans une table associé 
"""

class ConnexionDatabase:

    def __init__(self):
        self.host = "data-db.enercoop.infra"
        self.database = keyring.get_password("system", "database")
        self.user = keyring.get_password("system", "username")
        self.pwd = keyring.get_password("system", "password")
        self.port = 5432
        self.connection = psycopg2.connect(host=self.host, user=self.user, password=self.pwd, dbname=self.database)

    def pandas_sql(self, query):
        engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(self.user, self.pwd, self.host, self.port,
                                                                    self.database),
                               execution_options=dict(stream_results=True))
        data = pandas.read_sql_query(query, engine)

        return data

    def pandas_sql_chunk(self, query, chunksize):
        engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(self.user, self.pwd, self.host, self.port,
                                                                    self.database),
                               execution_options=dict(stream_results=True))
        for df_chunk in pandas.read_sql_query(query, engine, chunksize=chunksize):
            yield df_chunk
        engine.dispose()  # closes the thread

    @staticmethod
    def read_csv(chemin, file):
        data = pandas.read_csv(chemin + file)

        return data

    def write_database(self, dataframe, table):
        cursor = self.connection.cursor()

        cols = ",".join([str(i) for i in dataframe.columns.tolist()])

        for i, row in dataframe.iterrows():
            sql = "INSERT INTO " + table + " (" + cols + ") VALUES (" + "%s," * (len(row) - 1) + "%s)"
            cursor.execute(sql, tuple(row))
            self.connection.commit()

        cursor.close()

    def write_database_opti(self, dataframe, table): # TODO pas fonctionnel mais sans erreur du terminal
        sio = io.StringIO()
        sio.write(dataframe.to_csv(sep=";", quotechar="\"", escapechar='\\', index=False))

        cursor = self.connection.cursor()
        cursor.copy_from(sio, table, sep=";")
        sio.seek(0)
        self.connection.commit()
        cursor.close()

def main():
    data = ConnexionDatabase()
    df = data.pandas_sql('select * from producteurs limit 100')
    data.write_database(df, 'producteurs2')
    # print(data.pandas_sql_chunk(10))


if __name__ == "__main__":
    main()
