import matplotlib
import pandas
import statsmodels
import statsmodels.api as sm

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

"""
Entree : dataframe = la dataframe globale à analyser
        NomColoneDate = le str de la colone lié à la date 
        analyse = la colone à analyser par les graphiques des séries temporelles
        
Hypothéses : La période à un pas mensuels (period = 12) 
             Le modéle de Holt Winters qui approxime la tendance et la saisonalité convient à la série        
        
Sortie : Graphique_production = affichage simple de la série 
         affichage_simple = affichage de la série temporelle décomposer
         Analyse_Erreur = Analyse l'erreur celon les méthodes MSE et RMSE (A appeler lors des predictions)
"""


class SerieTemporellesCsv():

    def __init__(self, dataframe, nomColoneDate, coloneAnalyser):
        self.data = dataframe
        self.date = self.data[nomColoneDate]
        self.analyse = self.data[coloneAnalyser]
        self.analyseBis = self.data[[nomColoneDate, coloneAnalyser]]

    def affichage_serie(self):
        result = sm.tsa.seasonal_decompose(self.analyse, model='add', period=12)
        result.plot()

    def decompose_result(self):
        result = sm.tsa.seasonal_decompose(self.analyse, model='add', period=12)
        return result.trend, result.seasonal[0:11], result.resid, result.observed

    def graphique_serie_date(self):
        self.analyseBis.set_index("Date", inplace=True)
        self.analyseBis.plot(figsize=(12, 4))

    @staticmethod
    def analyse_erreur(nbpredictions, predictions, reel):
        erreur_MSE = (1/nbpredictions) * abs(predictions - reel).sum()
        erreur_RMSE = statsmodels.tools.eval_measures.rmse(predictions, reel)

        erreur_purcent_RMSE = erreur_RMSE * nbpredictions / (predictions + reel).sum()
        erreur_purcent_MSE = erreur_MSE * nbpredictions / (predictions + reel).sum()

        print("L'erreur selon la méthode MSE est de : ", erreur_MSE)
        print("L'erreur selon la méthode RMSE est de : ", erreur_RMSE)
        print("L'erreur en % MSE est : ", erreur_purcent_MSE)
        print("L'erreur en % MSE est : ", erreur_purcent_RMSE)

        return erreur_purcent_MSE, erreur_purcent_RMSE, erreur_RMSE, erreur_MSE


def main():
    df = SerieTemporellesCsv(pandas.read_csv('Data/classeur.csv'), 'Date', 'Production')
    df.graphique_serie_date()
    df.affichage_serie()
    plt.show()


if __name__ == "__main__":
    main()
