import pandas

from MR_PrevProdMT.SerieTemporelles.SerieTemporellesCsv import SerieTemporellesCsv

class ModelPred(SerieTemporellesCsv):

    def __init__(self, model, nbpred, df):
        SerieTemporellesCsv.__init__(self, df, 'Date', 'Production')
        self.model = model
        self.nbpredictions = nbpred

    def afficher(self):
        print(self.data)

df = SerieTemporellesCsv(pandas.read_csv('Data/classeur.csv'), 'Date', 'Production')

model = ModelPred('PasEncore', 12, df)
model.afficher()


