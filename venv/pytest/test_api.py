# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les tests API du projet 7
"""

import mock
import requests
import requests_mock
from io import BytesIO
import sys

import app.api_wiki as script_wiki
import app.api_google as script_google

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
        "https://fr.wikipedia.org/w/api.php",
        requests,
        ((),
         ))
    assert result[0]['Pytest'] == 'Réponse test'

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