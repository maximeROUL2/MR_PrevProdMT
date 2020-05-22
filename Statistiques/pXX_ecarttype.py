import pandas
from MR_PrevProdMT.ConnexionDatabase import ConnexionDatabase

"""
ENTREES : type_de_centrale
          les données historiques de facteurs de charge

SORTIES : la mediane par mois 
          le Q1, Q2 et l'écart-type par mois 
"""


class statistiques:

    def __init__(self, type):
        self.conn = ConnexionDatabase()
        self.dataAll = self.conn.pandas_sql("select * from facteur_de_charge where type_de_centrale ='" + type + "'")
        self.type = type

    def afficher(self):
        print(self.dataAll)

    def Q1_Q2_Q5_annuel(self):
        data = self.conn.pandas_sql("""select avg(facteur_de_charge) as FC_moyen, 
                                date_part('year'::text, month) as annee, padt
                                 from facteur_de_charge
                                where type_de_centrale = 'HY' 
                                group by annee, padt""")

        quantile = data['fc_moyen'].quantile([0.1, 0.2, 0.5])

        return quantile

    def P90_P80_P50_annuel(self):
        df = self.conn.pandas_sql("""select * from producteurs_contrat_2020""")

        quantile = self.Q1_Q2_Q5_annuel()

        df['Q1'] = (df.duree_contrat_annuel / 365) * quantile.loc[0.1] * df.puissance_installee_kw * 24 * 365
        df['Q2'] = (df.duree_contrat_annuel / 365) * quantile.loc[0.2] * df.puissance_installee_kw * 24 * 365
        df['Q5'] = (df.duree_contrat_annuel / 365) * quantile.loc[0.5] * df.puissance_installee_kw * 24 * 365

        print("Le P90 pour l'année 2020 est de :", round(df['Q1'].sum() * 0.001), "MWh",
              "\n Le P80 pour l'année 2020 est de :", round(df['Q2'].sum() * 0.001), "Mwh",
              "\n Le P50 pour l'année 2020 est de :", round(df['Q5'].sum() * 0.001), "Mwh")


appel = statistiques("HY")
appel.P90_P80_P50_annuel()