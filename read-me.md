OpenClassRooms - Projet 7

*##Version française*

I. Description
==============

Ce programme à pour but de créer un bot capable de réponse à des questions de position et de connaissance.
Basé sur l'API Wikipedia et Google, cette application permet d'afficher les lieux et de tirer une information de ce dernier.

II. Installation de python 3
============================

**Windows 10**
> Rendez-vous sur (https://python.org/downloads/)
> Télécharger la dernière version de python 3.X.X
> Installer la sur votre système

III. Installation de Git et copie du programme
==============================================

> Rendez-vous sur (https://git-scm.com/downloads)
> Télécharger la dernière version de git
> Installer cette dernière puis lancer l'application "Git Bash"

Copier le répertoire du programme avec la commande : `git clone https://github.com/ZasshuNeko/OC-Projet_5.git`


IV. Executer le programme
=========================

Pour une exécution local, lancé l'environnement virtuel Flask puis placez vous dans le dossier venv. 
Lancer l'application en executant 

`export FLASK_APP=main.py`
`python -m flask run`

Une fois lancé, rendez-vous sur votre adresse local pour profiter de l'application.

Pour une exécution sur héroku, envoyer le contenu du dossier venv sur héroku pour qu'il déploie et mette en ligne l'application.

VI. Le programme
================

Le programme se présente d'une unique page html. 
Utiliser la zone de texte du formulaire pour poser la question.

Toutes questions tel que : Où est xxxx ?
Sera traité en fournissant une map avec les différentes adresse trouvé et une explication de la part du bot.

Toutes question tel que : C'est quoi xxxx ?
Sera traité en fournissant des informations sur l'objet de votre demande et aucune carte ne sera montré

Vous pouvez aussi lui indiquer un mot unique, il sera alors traité comme une demande d'emplacement avec carte et définition.
Les autres questions qui peuvent vous venir à l'esprit sont traité de manière aléatoire par le bot et pensez bien à le saluer à chaque question sinon il pourrait se facher.

Les chiffres sont interdit et renvois un raffraichissement de la page.


*##English version*

I. Description
==============

This program aims to educate a healthier substitute for a food chosen by the user
It is based on a data set obtained by the Open Food Facts API.

II. Installation of python 3
============================

** Windows 10 **
> Go to (https://python.org/downloads/)
> Download the latest version of python 3.X.X
> Install it on your system

III. Installation of Gît and copy of the program
================================================

> Go to (https://git-scm.com/downloads)
> Download the latest version of git
> Install the latter then launch the "Git Bash" application

Copy the program directory with the command: `git clone https: // github.com / ZasshuNeko / OC-Projet_5.git`


IV. Execute the program
=========================

Once the directory has been copied to the chosen location, open the command prompt and go to the directory
`cd chemin_du_repertoir`
Then execute the program by typing * OFF_main.py *

V. The program
================

