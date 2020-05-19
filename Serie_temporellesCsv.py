import matplotlib
import statsmodels.api as sm
from conn_data import SqlQuery
from statsmodels.tsa.holtwinters import ExponentialSmoothing

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

"""
Entree : file = le nom du fichier en csv qui doit être mis dans le dossier Data
        NomColoneDate = le str de la colone lié à la date 
        analyse = la colone à analyser par les graphiques des séries temporelles
        
Hypothéses : La période à un pas mensuels (period = 12) 
             Le modéle de Holt Winters qui approxime la tendance et la saisonalité convient à la série        
        
Sortie : Graphique_production = affichage simple de la série 
         Decompose_affichage = affichage de la série temporelle décomposer
         Holt_Winters = Prediction celon Holt-Winters de la série
"""

class serie_temporelles_csv_affichage():

    def __init__(self, file, nomColoneDate, coloneAnalyser):
        self.data = SqlQuery.read_csv(file)
        self.date = self.data[nomColoneDate]
        self.analyse = self.data[coloneAnalyser]
        self.analyseBis = self.data[[nomColoneDate, coloneAnalyser]]

    def decompose_affichage(self):
        result = sm.tsa.seasonal_decompose(self.analyse, model='add', period=12)
        result.plot()

    def decompose_result(self):
        result = sm.tsa.seasonal_decompose(self.analyse, model='add', period=12)
        return result.trend, result.seasonal[0:11], result.resid, result.observed

    def holt_winters(self):
        plt.figure()
        HW = ExponentialSmoothing(self.analyse,
                                    seasonal_periods=12, trend='add', seasonal='add', damped=True).fit(use_boxcox=True)

        self.data['Production'].plot(style='--', marker='o', color='black', legend=True)
        HW.forecast(12).plot(style='--', marker='o', color='green', legend=True)

    def graphique_prod(self):
        self.analyseBis.set_index("Date", inplace=True)
        self.analyseBis.plot(figsize=(12, 4))


def main():
    df = serie_temporelles_csv_affichage('classeur.csv', 'Date', 'Production')
    df.graphique_prod()
    df.decompose_affichage()
    df.holt_winters()
    plt.show()


if __name__ == "__main__":
    main()
