from conn_data import SqlQuery
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters


class graphique():

    def __init__(self, query, label, x, y):
        self.data = SqlQuery.simple_query_pyscopg2(query)
        self.label = label
        self.x = self.data[x]
        self.y = self.data[y]

    def graph(self): # TODO afficher le graphique des erreurs par rapport au temps
        plt.figure()
        pd.Series.plot(self.data)
        plt.title(self.label)
        plt.show()


data = SqlQuery.simple_query_pyscopg2("Select month, sum(diff_kwh) from erreurs_prev_reel group by month limit 3")  # type: dataframe
# objet = graphique("Select month, sum(diff_kwh) from erreurs_prev_reel group by month", "evolution de l'erreur", 0, 1)
"""print(data)
objet.graph()

data.plot(x='1', y='0', color='red')
plt.show()
"""
df = pd.DataFrame({
    'name':['john','mary','peter','jeff','bill','lisa','jose'],
    'age':[23,78,22,19,45,33,20],
    'gender':['M','F','M','M','M','F','M'],
    'state':['california','dc','california','dc','california','texas','texas'],
    'num_children':[2,0,0,3,2,1,4],
    'num_pets':[5,1,0,5,2,2,3]
})
print(df)
print(data)
df.plot(kind='scatter',x='num_children',y='num_pets',color='red')
plt.show()