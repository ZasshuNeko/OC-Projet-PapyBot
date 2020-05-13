# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les fonctionnalités de l'API google."""
import requests
import re
import json
import configparser


class Api_google:
    """Cette classe permet de créer les demandes avec l'API google."""

    def __init__(self):

        self.adresse_api = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
        self.geometry_dict = {}
        self.geometry_tab = []
        self.reponse_tab = [] 
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def search_api(self, demande):
        """Créer la demande et permet d'obtenir la réponse avec la variable
        selection."""
        key = self.config.get('GOOGLE','Key')
        parametres = self.config_requests(demande,key)
        rtest = requests.get(url=self.adresse_api, params=parametres)
        reponseG = rtest.json()
        selection = self.geometry_json(reponseG)
        print(selection)
        # Permet de sélectionner le lien vers l'image google map
        return selection

    def config_requests(self,demande,key):
        parametres = {'query' : demande,
        'region' : 'fr',
        'key' : key }

        return parametres


    def geometry_json(self,reponsejson):
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
        except:
            self.reponse_tab = ['error']

        return self.reponse_tab


