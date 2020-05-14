from conn_data import SqlQuery
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter


data = SqlQuery.read_csv("producteurs_2020_05_04.csv")

class histogramme(file):

    def __init__(self, file, intervalle, type):
        self.data = SqlQuery.read_csv(file)
        self.intervalle = intervalle
        self.type = type

    @staticmethod
    def graphique():
        print("ok")



# --- Create histogram, legend and title ---
plt.figure()
r = np.random.randn(100)
r1 = r + 1
labels = ['Rabbits', 'Frogs']
H = plt.hist([r, r1], label=labels)
containers = H[-1]
leg = plt.legend(frameon=False)
plt.title("From a web browser, click on the legend\n"
                  "marker to toggle the corresponding histogram.")
