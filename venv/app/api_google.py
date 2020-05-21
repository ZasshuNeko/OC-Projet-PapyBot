# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les fonctionnalités de l'API google.
This file file contains the functionality of the google API."""

import configparser
import json
import re

import requests


class Api_google:
    """Cette classe permet de créer les demandes avec l'API google.
    This class is used to create requests with the google API."""

    def __init__(self):

        self.adresse_api = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
        self.geometry_dict = {}
        self.geometry_tab = []
        self.reponse_tab = []
        self.config = configparser.ConfigParser()
        self.config.read('app/config.ini')

    def search_api(self, demande):
        """Créer la demande et permet d'obtenir la réponse avec la variable
        selection.
        Create the request and get the answer with the variable
        selection."""
        key = self.config.get('GOOGLE', 'Key')
        parametres = self.config_requests(demande, key)
        rtest = requests.get(url=self.adresse_api, params=parametres)
        reponseG = rtest.json()
        selection = self.geometry_json(reponseG)
        return selection

    def config_requests(self, demande, key):
        """Paramètres pour le request vers l'api.
        Parameters for the request to the API."""
        parametres = {'query': demande,
                      'region': 'fr',
                      'key': key}

        return parametres

    def geometry_json(self, reponsejson):
        """ Récupération des informations renvoyé par l'API.
        Retrieving information sent by the API."""
        try:
            x = 0
            for dic in reponsejson['results']:
                position = "position" + str(x)
                self.geometry_dict[position] = dic['geometry']['location']
                x += 1
            fichier_json = json.dumps(self.geometry_dict)
            self.geometry_tab.append(fichier_json)
            self.reponse_tab.append(self.geometry_tab)
            if x == 1 and dic['formatted_address'].find(",") != -1:
                insert_localisation = dic['formatted_address']
                self.reponse_tab.append(insert_localisation)

                localisation_rue = insert_localisation.split(",")
                rue = localisation_rue[0].strip()

                self.reponse_tab.append(rue)
        except BaseException:
            self.reponse_tab = ['error']

        return self.reponse_tab
