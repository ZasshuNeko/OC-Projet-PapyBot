OpenClassRooms - Projet 7

*##Version française*

I. Description
==============

Ce programme a pour but de créer un bot capable de réponse à des questions de position et de connaissance.
Basé sur l'API Wikipedia et Google, cette application permet d'afficher les lieux et de tirer une information de ce dernier.

II. Installation de python 3
============================

**Windows 10**
> Rendez-vous sur (https://python.org/downloads/)
> Téléchargez la dernière version de python 3.X.X
> Installez la sur votre système

III. Installation de Git et copie du programme
==============================================

> Rendez-vous sur (https://git-scm.com/downloads)
> Téléchargez la dernière version de git
> Installez cette dernière puis lancer l'application "Git Bash"

Copiez le répertoire du programme avec la commande : `git clone https://github.com/ZasshuNeko/OC-Projet_5.git`


IV. Executer le programme
=========================

Pour une exécution local, lancez l'environnement virtuel Flask puis placez vous dans le dossier venv. 
Lancez l'application en executant :

`set FLASK_APP=main.py`
`python -m flask run`

Une fois lancé, rendez-vous sur votre adresse local pour profiter de l'application.

Pour une exécution sur héroku, envoyer le contenu du dossier venv sur héroku pour qu'il déploie et mette en ligne l'application.

V. Le programme
================

Le programme est composé d'une unique page html. 
Utiliser la zone de texte du formulaire pour poser la question.

Toute question telle que : Où est xxxx ?
Sera traitée en fournissant une map avec les différentes adresses trouvées et une explication de la part du bot.

Toute question tel que : C'est quoi xxxx ?
Sera traitée en fournissant des informations sur l'objet de votre demande et aucune carte ne sera montrée.

Les demandes uniques sont rejetées.
Les autres questions qui peuvent vous venir à l'esprit sont traitées de manière aléatoire par le bot et pensez bien à le saluer à chaque question sinon il pourrait se fâcher.

Les chiffres sont interdits et renvoie un refus du bot sans créer de rafraichissement.

VI. Les tests
=============

Les tests pour le programme se trouvent dans le dossier pytest.
La couverture des ces tests est de 85% et ils peuvent être executés avec ces lignes :
pytest -v -s pytest\test_projet.py
pytest -v -s pytest\test_api.py

Pour executer le test de couverture :
pytest --cov=app --cov-report html pytest/

Vous trouverez les résultats dans le dossier venv/htmlco


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

For local execution, launch the Flask virtual environment then go to the venv folder.
Launch the application by executing:

`set FLASK_APP = main.py`
`python -m flask run`

Once launched, go to your local address to take advantage of the application.

For an execution on heroku, send the content of the venv folder on heroku so that it deploys and puts the application online.

V. The program
================

The program consists of a single html page.
Use the text box on the form to ask the question.

Any questions such as: Où est xxxx?
Will be processed by providing a map with the different addresses found and an explanation from the bot.

Any question such as: C'est quoi xxxx?
Will be processed by providing information about the subject of your request and no cards will be shown

Single requests are rejected.
The other questions which can come to your mind are dealt with randomly by the bot and remember to greet him with each question otherwise he might get angry.

Numbers are prohibited and return a bot refusal without creating a refresh.

VI. The tests
==============

The tests for the program can be found in the pytest folder.
The coverage of these tests is 85% and they can be run with these lines:
pytest -v -s pytest \ test_projet.py
pytest -v -s pytest \ test_api.py

To run the coverage test:
pytest --cov = app --cov-report html pytest /

You will find the results in the folder venv / htmlco

