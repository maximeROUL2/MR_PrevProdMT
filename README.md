# MR_PrevProdMT
Prévision à moyen terme de la production selon les différents secteurs (Eolien, Hydraulique, Photovoltaique).
Le projet peut aussi être suivi via un Trello qui référence l'avancée du projet et ces axes de dévellopement : https://trello.com/invite/b/rNhkZyaI/4842e5c596cb24b193ea59c92609cce3/projet-enercoop

La première étape consiste en la visualisation de l'état actuel des choses et  l'évolution du champ des producteurs d'Enercoop par rapport au passé pour ensuite mieux prédire le futur sur des bases mathématiques plus solide. 

# Instalation du projet

- Le projet est codé en python 3.5 et est valable pour les appels à la BDD que sur le VPN de Enercoop
- Concernant les chemins vers les fichiers ils sont pour l'instant valables que pour ma machine 'maxime.roul' il faut donc les modfier pour l'instant avec vos propres chemin pour qu'ils fonctionnent
- Pour installer les librairies à jour il faut ouvrir un environement virtuel 

    - pip install virtualenv #installer la librairie d'environement virtuel (une chambre dans le PC)
    - virtualenv -p python3 env # créer un espace pour l'environement virtuel
    - source env/bin/activate #Entrer dans la "chambre" et activer l'environement virtuel (env dnas le terminal)
    - pip install -r requirements.txt # Installer les dépendances 

 - Ensuite le code est lancable que à partir de pycharm et de son runneur (Je ne sais pas trop pourquoi mais les appels à partir du terminal ne fonctionne pas où je ne connais pas encore les paramétres pour que les importations soit correctement dirigé notamment) 

# Charte du code 

l'ensemble des méthodes de charte du code est référencé dans ce cours de 4 heures 
https://openclassrooms.com/fr/courses/4425111-perfectionnez-vous-en-python/exercises/1668

- Nous travaillons dans un environement virtuel et il suffit d'appeller pip install -r requirements.txt pour mettre à jour l'environement virtuel chez vous avec toute les dépendances des librairies

- Un fichier = une classe + une éventuelle fonction main et un appel (d'essai) de cette fonction avec la condition

if __name__ == "__main__": qui s"appelle que lorsque on lance directement ce fichier et est donc fait pour les tests lié à la classe du fichier

- Les commentaires sont réalisé en haut de chaque classe et référence les entrées, les sorties et les hypothéses lié au programme. Ceux ci doivent toujours être à jour ! (Malheuresement en français car c'est beaucoup plus simple pour moi)

- Des tests unitaires sur chaque objet / test d'erreurs régulièrement (try / except)

- En utilisant pycharm on respecte les normes python PIP8 et la philosophie Pyhton PIP20 => import this dans un terminal python

- Utilisation de Git Régulièrement pour versionner et référencer l'avancé du travail 

- Une modélisation UML du code est disponible dans le fichier Projet_PrevMT.vpd.png

- On utilise les générators avec le mot clef yield pour réduire l'espace mémoire lors des appels de fonctions

- UNE REGLE : Simplicité de la Documentation et possibilité de MAJ rapide en production 

# Source de données 

Pour le secteur hydraulique les données Enercoop étant suffissament riche nous avons décider de traiter le fichier par_centrale_validé.ods de la branche RPM qui est mis à jour pour les nouveaux clients du perimétre. 

https://clood.enercoop.org/index.php/apps/files/?dir=/Approvisionnement%20-%20REZO%20%20-%20Priv%C3%A9/Appro%20EN/01_RPM/historique_production&fileid=18812464

Concernant le photovltaique et l'éolien nous allons travailler sur les données en open data des facteurs de charges par région et les comparer aux données (très récentes) d'enercoop sur les secteurs.

https://opendata.reseaux-energies.fr/explore/dataset/fc-tc-regionaux-mensuels-eolien-solaire/information/?disjunctive.region

Bien évidémment nous complétons avec les flux RP12 de la BDD Data-etl-polen des producteurs et nous négligeons les flux RP9 qui correspondent à des taux très faibles pour l'éolien et l'hydrau. 
Pour le PV cela représente ~25% des fluxs et il y a aussi beaucoup d'autoconsomation donc il faudra rajouter ces paramétres. 

