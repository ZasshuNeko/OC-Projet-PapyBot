# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les tests du projet 7
"""

import json
import sys

import mock
import requests
import requests_mock
from io import BytesIO

import traitement as script
import fichierjson as script_json
import api_wiki as script_wiki
import api_google as script_google


class Testmain:

    def setup_method(self):
        self.traitement = script.Traitement()
        self.correction = self.traitement.correction_demande(
            "Ou est OpenClassrooms ?")
        self.salutation = self.traitement.salutation_utilisateur("bonjour")
        self.fichierjson = script_json.Sourcejson()


    def json(sefl):
        sortie_json = fichierjson.creation_json("Test demande",["test",True,"Test"])
        print(sortie_json)

    def test_reponse_papy_add(self):
        reponse_papy =  self.fichierjson.papy_reponse(
            'test', False, [
                "lien", "25 rue test,75000 Paris", "add"])
        assert reponse_papy == "<li class='list-group-item list-group-item-success'>Papy : test</br>Alors mon petit ! Sache que cela est situé 25 rue test code postal 75000 Paris</li>"

    def test_reponse_papy_nom(self):
        reponse_papy =  self.fichierjson.papy_reponse(
            "test", False, [
                "lien", "TrucTruc,25 rue test,75000 Paris", "add"])
        assert reponse_papy == "<li class='list-group-item list-group-item-success'>Papy : test</br>Alors mon petit ! Sache que TrucTruc est situé 25 rue test code postal 75000 Paris</li>"

    def test_correction_demande(self):
        assert self.correction == [["où", "est", "openclassrooms"],
                                   'Petit malotrue ! On salut son ainé avant de demander ... ']

    def test_salutation(self):
        assert self.salutation == 'Un jeune bien élevé comme on les apprécie tant ! '

    def test_chercher_terme(self):
        terme = self.traitement.chercher_termes(["quoi", "velo"])
        assert terme == ["velo", False]


class MockReponseWiki:
    @staticmethod
    def json():
        return {'Pytest': 'Réponse test'}


def test_request_wiki(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockReponseWiki()

    monkeypatch.setattr(requests, "get", mock_get)
    result = script_wiki.api_wikipedia(
        "TEST",
        "query",
        "search",
        "json",
        "https://fr.wikipedia.org/w/api.php",
        requests,
        ((),
         ))
    assert result['Pytest'] == 'Réponse test'

class MockReponseGoogle:
    @staticmethod
    def json():
        return {'results':'test'}


def test_request_google(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockReponseGoogle()

    monkeypatch.setattr(requests, "get", mock_get)
    script_ini = script_google.Api_google()
    result = script_ini.search_api('test')
    assert type(result) is list
