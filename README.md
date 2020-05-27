# MR_PrevProdMT
Prévision à moyen terme de la production selon les différents secteurs (Eolien, Hydraulique, Photovoltaique).
Le projet peut aussi être suivi via un Trello qui référence l'avancée du projet et ces axes de dévellopement : https://trello.com/invite/b/rNhkZyaI/4842e5c596cb24b193ea59c92609cce3/projet-enercoop

La première étape consiste en la visualisation de l'état actuel des choses et  l'évolution du champ des producteurs d'Enercoop par rapport au passé pour ensuite mieux prédire le futur sur des bases mathématiques plus solide. 

On va tester notre nouvelle branche pour s'exercer ! 

On change via pycharm

# Charte du code 

- Tous les objets qui peuvent être réutiliser de nombreuses fois sont dans la bibliothèque "tools"

- Un fichier = une classe + une éventuelle fonction main et un appel de cette fonction avec la condition

if __name__ == "__main__":

- Des tests unitaires sur chaque objet / test d'erreurs régulièrement (try / except)

- TUtilisation d'une machine virtuelle qui centralise les versions des biliothéques dans un fichier requirements.txt

- En utilisant pycharm on respecte les normes python PIP8 

- Utilisation de Git Régulièrement pour versionner et référencer l'avancé du travail 

- UNE REGLE : Simplicité de la Documentation et possibilité de MAJ rapide en production 

# Source de données 

Pour le secteur hydraulique les données Enercoop étant suffissament riche nous avons décider de traiter le fichier par_centrale_validé.ods de la branche RPM qui est mis à jour pour les nouveaux clients du perimétre. 

https://clood.enercoop.org/index.php/apps/files/?dir=/Approvisionnement%20-%20REZO%20%20-%20Priv%C3%A9/Appro%20EN/01_RPM/historique_production&fileid=18812464

Concernant le photovltaique et l'éolien nous allons travailler sur les données en open data des facteurs de charges par région et les comparer aux données (très récentes) d'enercoop sur les secteurs.

https://opendata.reseaux-energies.fr/explore/dataset/fc-tc-regionaux-mensuels-eolien-solaire/information/?disjunctive.region

Bien évidémment nous complétons avec les flux RP12 de la BDD Data-etl-polen des producteurs et nous négligeons les flux RP9 qui correspondent à des taux très faibles pour l'éolien et l'hydrau. 
Pour le PV cela représente ~25% des fluxs et il y a aussi beaucoup d'autoconsomation donc il faudra rajouter ces paramétres. 

