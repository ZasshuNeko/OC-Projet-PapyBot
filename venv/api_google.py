# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les fonctionnalités de l'API google."""
import requests
import re
import json


class Api_google:
    """Cette classe permet de créer les demandes avec l'API google."""

    def __init__(self):
        #self.adresse_api = 'https://www.google.com/maps/search/?api=1&query='
        self.adresse_api = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
        self.key = 'AIzaSyD72ipLMIMctyuEMV2hsnWSqCozg8uE9Ok'
        self.geometry_dict = {}
        self.geometry_tab = []
        self.reponse_tab = [] 

    def search_api(self, demande):
        """Créer la demande et permet d'obtenir la réponse avec la variable
        selection."""
        #question_api = self.adresse_api + demande
        #r = requests.get(question_api)
        #reponse = str(r.content)

        parametres = self.config_requests(demande,self.key)
        rtest = requests.get(url=self.adresse_api, params=parametres)
        reponseG = rtest.json()
        selection = self.geometry_json(reponseG)
        print(selection)

        # Permet de sélectionner le lien vers l'image google map
        #selection = selection_api(reponse)
        return selection

    def config_requests(self,demande,key):
        parametres = {'query' : demande,
        'region' : 'fr',
        'key' : key }

        return parametres


    def geometry_json(self,reponsejson):

        x = 0
        for dic in reponsejson['results']:
            position = "position" + str(x)
            self.geometry_dict[position] = dic['geometry']['location']
            x += 1
        fichier_json = json.dumps(self.geometry_dict)
        self.geometry_tab.append(fichier_json)
        self.reponse_tab.append(self.geometry_tab)
        if x == 1:
            insert_localisation = dic['formatted_address']
            self.reponse_tab.append(insert_localisation)

        #----------------------------------
        # A mettre dans un autre module
            localisation_rue = insert_localisation.split(",")
            rue = localisation_rue[0].strip()
        #-----------------------------------

            self.reponse_tab.append(rue)

        return self.reponse_tab


