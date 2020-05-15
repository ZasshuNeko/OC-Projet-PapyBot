# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les tests du projet 7
"""

import json
import sys

import mock
import requests
import requests_mock
from io import BytesIO

import app.traitement as script
import app.fichierjson as script_json
import app.api_wiki as script_wiki
import app.api_google as script_google


class Testmain:

    def setup_method(self):
        self.wiki = script_wiki.Api_wiki()
        self.google = script_google.Api_google()
        self.traitement = script.Traitement()
        self.correction = self.traitement.correction_demande(
            "Ou est OpenClassrooms ?")
        self.salutation = self.traitement.salutation_utilisateur("bonjour")
        self.fichierjson = script_json.Sourcejson()

    #Test fichier du fichier nommé fichierjson


    def test_json(self):
        sortie_json = self.fichierjson.creation_json("Test demande",[[],"Test","Un jeune bien élevé comme on les apprécie tant ! ",False])
        test_sortie = json.loads(sortie_json)
        assert test_sortie["url_google"] == [{}]

    def test_reponse_papy(self):
        reponse_papy =  self.fichierjson.papy_reponse(
            'test', False, [
                "lien", "25 rue test,75000 Paris", "add"])
        assert reponse_papy == "<li class='list-group-item list-group-item-success'>Papy : test</br>Alors mon petit ! Sache que cela est situé 25 rue test,75000 Paris</li>"

    #Test fichier du fichier nommé traitement

    def test_correction_demande(self):
        assert self.correction == ["où", "est", "openclassrooms"]

    def test_salutation(self):
        assert self.salutation == 'Un jeune bien élevé comme on les apprécie tant ! '

    def test_chercher_terme(self):
        terme = self.traitement.chercher_termes(["quoi", "velo"])
        assert terme == ["velo ", False, False]

    def test_gestion_question(self):
        demande_error = "Mot" #Mot unique
        demande_valide = "Ou est paris ?"

        reponse_error = self.traitement.gestion_question(demande_error)
        reponse_valide = self.traitement.gestion_question(demande_valide)

        assert reponse_error[0] == [] and len(reponse_valide[0]) >= 1

    #Test fichier du fichier nommé api_google

    def test_geometry_google(self):
        json_test = json.loads('{"html_attributions": [], "results": [{"formatted_address": "test, test", "geometry": {"location": {"lat": "test", "lng": "test"}}}], "status": "OK"}')
        reponse = self.google.geometry_json(json_test)
        assert reponse[2] == 'test'

    #Test fichier du fichier nommé api_wiki


    def test_wiki_informations_snippet(self):
        section = 'snippet'

        info = [{'pageid': 00000, 'snippet': 'Pif Paf Pouf'}]
        reponse = script_wiki.informations(info,section)
        assert reponse == info[0]['snippet'] + " Suit ce <a href='https://fr.wikipedia.org/?curid=" + str(info[0]['pageid']) + "' >lien</a> et plus d'informaiton tu trouvera !</br>"
    
    def test_wiki_informations_pages(self):
        section = 'pages'
        info = {'test': {'pageid': 11111, 'extract': "Test"}}
        reponse = script_wiki.informations(info,section)
        assert reponse == info['test']['extract'] + " Suit ce <a href='https://fr.wikipedia.org/?curid=" + str(info['test']['pageid']) + "' >lien</a> et plus d'informaiton tu trouvera !</br>"

    def test_try_wiki(self):
        tab = [{"query":{"snippet":"test"}},"snippet"]
        reponse = script_wiki.try_content(tab,'[test]')
        assert reponse[1] == False and reponse[0] == "test"

    def test_gestion_chaine(self):
        mot = "test"
        phrase = "homonymes ///////***/*/**--*/*/." + mot + " : <div>" + mot + "</div> / <span>" + mot + "</span>"
        reponse = script_wiki.gestion_chaine(phrase)
        assert reponse == mot + " : " + mot + " / " + mot
