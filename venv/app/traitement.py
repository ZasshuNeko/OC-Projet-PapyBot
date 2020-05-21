# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les fonctions de traitement de la demande.
This File File contains the request processing functions."""

import configparser
import json
import unicodedata
from random import randint

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer

from app.api_google import Api_google
from app.api_wiki import Api_wiki

nltk.data.path.append('nltk_data/')
# nltk.download('stopwords')


class Traitement:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('app/config.ini', 'utf8')
        self.liste_terme = self.config.get('LISTE', 'terme').split(',')
        self.liste_temporelle = self.config.get('LISTE', 'temporelle').split(',')
        self.liste_histoire = self.config.get('LISTE', 'histoire').split(',')
        self.liste_aleatoire = self.config.get('LISTE', 'terme_aleatoire').split(',')
        self.liste_mapoff = self.config.get('LISTE', 'map').split(',')
        self.liste_cg = self.config.get('LISTE', 'map_true').split(',')
        self.liste_except = self.config.get('LISTE', 'except').split(',')
        self.reponse = self.config.get('LISTE', 'reponse').split(',')

    def gestion_question(self, demande):
        """Charge la question de l'utilisateur et de la traiter et de l'envoyer
        vers les API google et wikipedia.
        Load the user question and process and send it
        to the google and wikipedia APIs."""

        liste_demande = self.correction_demande(demande)
        salutation = self.salutation_utilisateur(liste_demande[0])

        if len(liste_demande) == 1:
            reponse_apigoogle = []
            reponse_wiki = []
            terme_selection = False
            return [
                reponse_apigoogle,
                reponse_wiki,
                salutation,
                terme_selection]
        else:
            terme_selection = self.chercher_termes(liste_demande)
            search_terme = terme_selection[0]
            reponse_api = self.tris_api(terme_selection, search_terme)
            reponse_apigoogle = reponse_api[0]
            reponse_wiki = reponse_api[1]
            return [
                reponse_apigoogle,
                reponse_wiki,
                salutation,
                terme_selection[1]]

    def tris_api(self, terme_selection, search_terme):
        """Determine quelle API doit être utilisé.
        Determine which API should be used."""
        if terme_selection[1]:
            reponse_apigoogle = []
            reponse_wiki = search_terme
        else:
            if terme_selection[2]:
                terme_wiki = search_terme
                reponse_apigoogle = self.api_google(search_terme)
                if len(reponse_apigoogle) > 2 and isinstance(
                        reponse_apigoogle, list):
                    terme_wiki = reponse_apigoogle[2]
            else:
                terme_wiki = search_terme
                reponse_apigoogle = []
            reponse_wiki = self.api_wiki(terme_wiki)
        return [reponse_apigoogle, reponse_wiki]

    def correction_demande(self, demande):
        """En utilisant nltk nous scindons la demande de l'utilisateur en liste
        de terme, nous profitons d'appliquer des corrections pour
        l'orthorgraphe de certain mots.
        Using nltk we split the user request into a list
        term we take advantage of applying corrections for
        the orthorograph of certain words."""
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        demande_minuscule = demande.lower()
        demande_minuscule = "".join((c for c in unicodedata.normalize(
            'NFD', demande_minuscule) if unicodedata.category(c) != 'Mn'))
        liste_demande = tokenizer.tokenize(demande_minuscule)
        for index, mot in enumerate(liste_demande):
            if index + 1 >= len(liste_demande):
                break
            elif mot == "ou" or mot == "est" and liste_demande[index + 1] == "est" or liste_demande[index + 1] == "sont":
                liste_demande[index] = "où"
            elif mot.isnumeric():
                del liste_demande[index]

        return liste_demande

    def chercher_termes(self, liste_demande):
        """Permet de déterminer s'il y a un terme intéréssant pour l'API
        wikipedia, cela se base sur différent terme que l'on va chercher.
        Determines if there is an interesting term for the API
        wikipedia, it is based on different term that we are going to look for."""
        filtered_words = [
            word for word in liste_demande if word not in stopwords.words('french')]
        for index, mot in enumerate(filtered_words):
            if mot in self.liste_terme:
                try:
                    index_second = filtered_words[index + 1]
                    retour_var = self.renvois_terme(
                        filtered_words, index_second, index, mot)
                    terme = retour_var[0]
                    error = retour_var[1]
                    maping = retour_var[2]
                except BaseException:
                    terme = " Quoi répète plus fort ?!!"
                    error = True
                    maping = False
                break
            elif len(filtered_words) == 1:
                if mot not in self.liste_terme:
                    terme = mot
                    error = True
                    maping = False
        if len(filtered_words) == 0:
            terme = 'Dit moi ce que tu veux mon enfant ...'
            error = True
            maping = False

        try:
            return [terme, error, maping]
        except:
            index_terme = randint(0, 3)
            print(self.reponse)
            print(index_terme)
            return [self.reponse[index_terme], True, False]

    def renvois_terme(self, liste, index, num, mot):
        """Renvois le ou les termes important.
        Return the important term."""
        x = 1
        terme = ""
        error = False
        maping = True
        if index not in self.liste_temporelle and index not in self.liste_histoire:
            index_val = int(num) + int(x)
            while index_val <= len(liste):
                try:
                    if liste[index_val] not in self.liste_except:
                        terme = terme + liste[index_val] + " "
                    x += 1
                    index_val = int(num) + int(x)
                except BaseException:
                    break
            terme.strip()
            if mot in self.liste_mapoff:
                for except_map in self.liste_cg:
                    if terme.find(except_map) != -1:
                        maping = True
                    else:
                        maping = False
        elif index in self.liste_temporelle and index not in self.liste_histoire:
            terme = "Tu sais ce qui se passera plus tard est un mystère et parfois il faut le chérir..."
            error = True
        elif index in self.liste_histoire:
            index_terme = randint(0, 11)
            terme = self.liste_aleatoire[index_terme]
            maping = False

        return [terme, error, maping]

    def api_google(self, terme_important):
        """Permet d'initialiser la classe gérant l'api google et de l'intéroger
        avec le terme important de la question.
        Allows you to initialize the class handling the google API and to interrogate it
        with the important term of the question."""
        apigoogle = Api_google()
        resultat = apigoogle.search_api(terme_important)
        return resultat

    def api_wiki(self, terme_important, *autres):
        """Permet d'initialiser la classe gérant l'api wikipedia et de
        l'intéroger avec le terme important de la question.
        Allows you to initialize the class managing the wikipedia API and to
        question it with the important term of the question."""
        apiwiki = Api_wiki()
        resultat = apiwiki.search_api(terme_important, autres)
        return resultat 

    def salutation_utilisateur(self, terme):
        """Gérer si utilisateur à salué papy.
        Manage if user greeted grandpa."""
        if terme == "salut" or terme == "bonjour" or terme == "yo":
            salutation = "Un jeune bien élevé comme on les apprécie tant ! "
        else:
            salutation = "Petit malotru ! On salue son ainé avant de demander ... "
        return salutation
