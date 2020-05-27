import numpy as np
import xlrd
import pandas
from MR_PrevProdMT.ConnexionDatabase import ConnexionDatabase

"""
ENTREES : le fichier par_central_validé.ods enregistrer en excel
          le fichier de facteur de charge en open data => se connecter à l'API pour être en direct

HYPOTHESES : On ne prend que le bloc à partir de la ligne 9 qui correspond aux datas qui nous 
interesse
            Le fichier par_centrale_validé à été modifié à la main pour remplir notamment le 
total OA de 0 et pour supprimer les derniére lignes quasi vides qui posaient des problémes à 
la lecture => le code n'est donc pas automatique sur le fichier de base de RPM

            Dans la dataBase une table est créer en amont de ce script de la forme dans le fichier
            historique_hydro.sql

SORTIES : L'insertion de toute les lignes 9 et + de toutes les pages du fichiers par_central_validé.ods en base 
          La lecture du fichier fc-tc-régionaux (réduit aux données utiles) en dataframe      
"""


class LectureHistoriqueOds:

    def __init__(self):
        self.workbook = xlrd.open_workbook('Data/par_centrale_validé_2020_05_04.xlsx')
        self.sheetnames = self.workbook.sheet_names()
        self.lignedebut = 9

        self.opendata = pandas.read_csv('Data/fc-tc-regionaux-mensuels-eolien-solaire.csv')


    def pandas_lecture(self, sheetname):
        df = pandas.read_excel(self.workbook, sheetname,
                               names=['nbjours', 'date', 'bilan_mensuel_kw', 'marché', 'facteur_de_charge',
                                      'Total_Puissance',
                                      'Total_ML', 'Total_OA', 'Evenement', 'Commentaire'],
                               usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], skiprows=self.lignedebut - 1)

        df['padt'] = sheetname

        return df

    def inserer_database(self, sheetname):
        try:
            conn = ConnexionDatabase()
            conn.write_database(self.pandas_lecture(sheetname), 'historique_hydro')
        except:
            print("Error : ", sheetname)

    def lire_workbook(self):  # Todo Beaucoup d'erreurs de lecture à corriger pour insérer proprement en base
        for i in np.arange(1, len(self.sheetnames)):
            print(self.sheetnames[i])
            self.inserer_database(str(self.sheetnames[i]))

    def fc_opendata_df(self): # TODO se connecter à l'API pour être en direct
# API : https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=fc-tc-regionaux-mensuels-eolien-solaire&q=&sort=mois&facet=mois&facet=region
        return self.opendata


def main():
    lecture = LectureHistoriqueOds()
    # lecture.lire_workbook() => bugs sur pas mal de sheet (noter dans le cahier)
    print(lecture.fc_opendata_df())


if __name__ == "__main__":
    main()