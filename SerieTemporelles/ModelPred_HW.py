import matplotlib
import pandas
from statsmodels.tsa.holtwinters import ExponentialSmoothing

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from MR_PrevProdMT.SerieTemporelles.SerieTemporellesCsv import SerieTemporellesCsv

"""
Entree : dataframe = la dataframe globale à analyser
        NomColoneDate = le str de la colone lié à la date 
        analyse = la colone à analyser par les graphiques des séries temporelles
        nbpred = le nombre de prédictions que l'on veux 

Hypothéses : On utilise le modéle de Holt Winters (Lissage Exponentionnel optimisé)  
qui approxime la tendance et la saisonalité optimum quiconvient à la série 
en prenant plus en compte plus le passé récent que le lointain       

Sorties : predictions = retourne les X predictions de la série
         HW = affiche dans le terminal et retourne les erreurs du modéle (MSE, RMSE et %)
        Affichage = Une affichage des predictions future et un affichage 
des predictions superposés au reel sur le X derniéres valeurs
"""

class HoltWinters(SerieTemporellesCsv):

    def __init__(self, nbpred, df, coloneDate, coloneAnalyser):
        SerieTemporellesCsv.__init__(self, df, coloneDate, coloneAnalyser)
        self.model = ExponentialSmoothing(self.analyse,
                                          seasonal_periods=12, trend='add', seasonal='add', damped=True).fit(
            use_boxcox=True)

        self.nbPredictions = nbpred
        self.modelTest = ExponentialSmoothing(self.analyse[:-self.nbPredictions],
                                              seasonal_periods=12, trend='add', seasonal='add', damped=True).fit(
            use_boxcox=True)

    def predictions(self):
        predictions = self.model.forecast(self.nbPredictions)
        return predictions

    def HW_erreurs(self):
        predictions = self.modelTest.forecast(self.nbPredictions)
        erreurs = SerieTemporellesCsv.analyse_erreur(
            self.nbPredictions, predictions, self.analyse.tail(self.nbPredictions))

        return erreurs

    def affichage_predfutur(self):
        plt.figure()
        self.analyse.plot(style='--', marker='o', color='black', legend=True)
        self.predictions().plot(style='--', marker='o', color='green', legend=True)

    def affichage_pred_cache(self):
        plt.figure()
        self.analyse.plot(style='--', marker='o', color='black', legend=True)

        predictions = self.modelTest.forecast(self.nbPredictions)
        predictions.plot(style='--', marker='o', color='green', legend=True)


def main():
    model = HoltWinters(12, pandas.read_csv('Data/classeur.csv'),
                        'Date', 'Facteur de charge (par rapport à la puissance en ML)')
    model.HW_erreurs()
    model.affichage_predfutur()
    model.affichage_pred_cache()

if __name__ == "__main__":
    main()
