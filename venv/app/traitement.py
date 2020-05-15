# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient le corp de l'application."""

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
        self.liste_terme = self.config.get('LISTE', 'terme')
        self.liste_temporelle = self.config.get('LISTE', 'temporelle')
        self.liste_histoire = self.config.get('LISTE', 'histoire')
        self.liste_aleatoire = self.config.get('LISTE', 'terme_aleatoire')
        self.liste_mapoff = self.config.get('LISTE', 'map')

    def gestion_question(self, demande):
        """Charge la question de l'utilisateur et de la traiter et de l'envoyer
        vers les API google et wikipedia."""
        # Appel la fonction qui corrige l'orthographe des mots
        # important et ramène s'il y a une salutation
        liste_demande = self.correction_demande(demande)
        salutation = self.salutation_utilisateur(liste_demande)

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
        l'orthorgraphe de certain mots."""
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        demande_minuscule = demande.lower()
        demande_minuscule = "".join((c for c in unicodedata.normalize(
            'NFD', demande_minuscule) if unicodedata.category(c) != 'Mn'))
        liste_demande = tokenizer.tokenize(demande_minuscule)
        for index, mot in enumerate(liste_demande):
            if index + 1 >= len(liste_demande):
                break
            elif mot == "ou" and liste_demande[index + 1] == "est" or liste_demande[index + 1] == "sont":
                liste_demande[index] = "où"
            elif mot.isnumeric():
                del liste_demande[index]

        return liste_demande

    def chercher_termes(self, liste_demande):
        """Permet de déterminer s'il y a un terme intéréssant pour l'API
        wikipedia, cela se base sur différent terme que l'on va chercher."""
        # Retire les stopword de la liste des mots fait à partir de la
        # demande
        filtered_words = [
            word for word in liste_demande if word not in stopwords.words('french')]
        for index, mot in enumerate(filtered_words):
            if mot in self.liste_terme:
                index_second = filtered_words[index + 1]
                retour_var = self.renvois_terme(
                    filtered_words, index_second, index, mot)
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
                break
            elif len(filtered_words) == 1:
                if mot not in self.liste_terme:
                    terme = mot
        return [terme, error, maping]

    def renvois_terme(self, liste, index, num, mot):
        x = 1
        terme = ""
        error = False
        maping = True
        if index not in self.liste_temporelle and index not in self.liste_histoire:
            index_val = int(num) + int(x)
            while index_val <= len(liste):
                try:
                    terme = terme + liste[index_val] + " "
                    x += 1
                    index_val = int(num) + int(x)
                except BaseException:
                    break
            terme.strip()
            if mot in self.liste_mapoff:
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
        avec le terme important de la question."""
        apigoogle = Api_google()
        resultat = apigoogle.search_api(terme_important)
        return resultat

    def api_wiki(self, terme_important, *autres):
        """Permet d'initialiser la classe gérant l'api wikipedia et de
        l'intéroger avec le terme important de la question."""
        apiwiki = Api_wiki()
        resultat = apiwiki.search_api(terme_important, autres)
        return resultat

    def salutation_utilisateur(self, terme):
        """Gérer si utilisateur à salué papy."""
        if terme == "salut" or terme == "bonjour" or terme == "yo":
            salutation = "Un jeune bien élevé comme on les apprécie tant ! "
        else:
            salutation = "Petit malotru ! On salue son ainé avant de demander ... "
        return salutation
