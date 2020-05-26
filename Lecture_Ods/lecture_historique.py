import numpy as np
import xlrd
import pandas
from MR_PrevProdMT.ConnexionDatabase import ConnexionDatabase


class LectureHistoriqueOds:

    def __init__(self):
        self.workbook = xlrd.open_workbook('Data/par_centrale_validé_2020_05_04.xlsx')
        self.sheetnames = self.workbook.sheet_names()
        self.lignedebut = 9

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
            print(" Error : ", sheetname)

    def lire_workbook(self): #Todo Beaucoup d'erreurs de lecture à corriger pour insérer proprement en base
        for i in np.arange(1, len(self.sheetnames)):
            print(self.sheetnames[i])
            self.inserer_database(str(self.sheetnames[i]))


def main():
    lecture = LectureHistoriqueOds()
    lecture.lire_workbook()


if __name__ == "__main__":
    main()


