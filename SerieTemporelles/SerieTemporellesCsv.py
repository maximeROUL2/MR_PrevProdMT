import matplotlib
import pandas
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.holtwinters import ExponentialSmoothing

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

"""
Entree : dataframe = la dataframe globale à analyser
        NomColoneDate = le str de la colone lié à la date 
        analyse = la colone à analyser par les graphiques des séries temporelles
        
Hypothéses : La période à un pas mensuels (period = 12) 
             Le modéle de Holt Winters qui approxime la tendance et la saisonalité convient à la série        
        
Sortie : Graphique_production = affichage simple de la série 
         Decompose_affichage = affichage de la série temporelle décomposer
         Holt_Winters = Prediction celon Holt-Winters de la série
"""


class SerieTemporellesCsv():

    def __init__(self, dataframe, nomColoneDate, coloneAnalyser):
        self.data = dataframe
        self.date = self.data[nomColoneDate]
        self.analyse = self.data[coloneAnalyser]
        self.analyseBis = self.data[[nomColoneDate, coloneAnalyser]]

    def decompose_affichage(self):
        result = sm.tsa.seasonal_decompose(self.analyse, model='add', period=12)
        result.plot()

    def decompose_result(self):
        result = sm.tsa.seasonal_decompose(self.analyse, model='add', period=12)
        return result.trend, result.seasonal[0:11], result.resid, result.observed

    def holt_winters(self, nbpredictions):
        plt.figure()
        HW = ExponentialSmoothing(self.analyse,
                                  seasonal_periods=12, trend='add', seasonal='add', damped=True).fit(use_boxcox=True)

        self.data['Production'].plot(style='--', marker='o', color='black', legend=True)
        HW.forecast(12).plot(style='--', marker='o', color='green', legend=True)

        return HW.forecast(nbpredictions)

    def analyse_erreur_holt_winters(self, nbpredictions):
        HW = ExponentialSmoothing(self.analyse[:-nbpredictions],
                                  seasonal_periods=12, trend='add', seasonal='add', damped=True).fit(use_boxcox=True)

        predictions = HW.forecast(nbpredictions)
        reel = self.analyse.tail(nbpredictions)

        erreur_MSE = (1/nbpredictions) * abs(predictions - reel).sum()
        erreur_RMSE = statsmodels.tools.eval_measures.rmse(predictions, reel)

        erreur_purcent_RMSE = erreur_RMSE * nbpredictions / (predictions + reel).sum()
        erreur_purcent_MSE = erreur_MSE * nbpredictions / (predictions + reel).sum()

        return erreur_purcent_MSE, erreur_purcent_RMSE, erreur_RMSE, erreur_MSE

    def graphique_prod(self):
        self.analyseBis.set_index("Date", inplace=True)
        self.analyseBis.plot(figsize=(12, 4))


def main():
    df = SerieTemporellesCsv(pandas.read_csv('Data/classeur.csv'), 'Date', 'Production')
    print(df.analyse_erreur_holt_winters(24))
    df.graphique_prod()
    df.decompose_affichage()
    df.holt_winters(24)
    plt.show()


if __name__ == "__main__":
    main()
