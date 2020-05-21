# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient les fonctionnalités de l'API wikipedia.
This File File contains the functionality of the Wikipedia API."""

import json

import requests
from bs4 import BeautifulSoup


class Api_wiki:
    """Cette classe permet d'émettre une demande via l'API wikipédia à
    l'initialisation nous chargeons les différentes variable dont on a
    besoin.
    This class is used to issue a request via the Wikipedia API to
    initialization we load the different variables which we have
    need."""

    def __init__(self):
        self.adresse_api = 'https://fr.wikipedia.org/w/api.php'
        self.action = "query"
        self.format = "json"
        self.liste = "search"
        self.session = requests.Session()

    def search_api(self, terme_recherche, autres):
        """Permet d'éffectuer la recherche représenté par la variable
        demande.
        Allows you to perform the search represented by the variable
        request."""
        reponse = api_wikipedia(
            terme_recherche,
            self.adresse_api,
            self.session,
            autres)
        chaine_content = try_content(reponse, terme_recherche)
        if not chaine_content[1]:
            chaine_finale = informations(chaine_content[0], reponse[1])
        else:
            chaine_finale = chaine_content[1]

        return chaine_finale


def informations(information, type_section):
    """Création de la réponse de papy à partir de la réponse api.
    Creation of grandpa's response from the API response."""
    if type_section == "pages":
        for key in information.keys():
            dict_extract = information.get(key)
            chaine_content = dict_extract.get('extract')
            pageid = dict_extract.get('pageid')
            break
    else:
        chaine_content = information[0].get('snippet')
        chaine_content = gestion_chaine(chaine_content)
        pageid = information[0].get('pageid')
    information_complementaire = " Suit ce <a href='https://fr.wikipedia.org/?curid=" + \
        str(pageid) + "' >lien</a> et plus d'informaiton tu trouvera !"
    reponse_papy = chaine_content + information_complementaire + "</br>"
    return reponse_papy


def config_request_demande_loc(chaine):
    """Paramétre de l'API pour la requête en recherche.
    API setting for search query."""
    parametres = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": chaine,
        "srlimit": 1
    }
    return parametres


def config_request_demande_D(chaine):
    """Paramétre de l'API pour la requete en utilisant le titre.
    API parameters for the request using the title."""
    parametres = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "redirects": 1,
        "exintro": 1,
        "explaintext": 1,
        "exchars": "575",
        "titles": chaine
    }
    return parametres


def api_wikipedia(
        terme_recherche,
        adresse_api,
        session,
        *autres):
    """Envoie de la requête à l'API.
    Sends a request to the API."""
    mot = terme_recherche[0]
    if mot.isdigit():
        parametres = config_request_demande_loc(terme_recherche)
        section = "search"
        r = session.get(url=adresse_api, params=parametres)
    else:
        parametres = config_request_demande_D(terme_recherche)
        r = session.get(url=adresse_api, params=parametres)
        section = "pages"
        verification = try_page(
            r, section, terme_recherche, adresse_api, session)
        if len(verification) != 0:
            r = verification[0]
            section = verification[1]
    reponse = r.json()
    return [reponse, section]


def try_content(reponse, demande):
    """Cette fonction effectue un test sur les réponses de l'API.
    This function performs a test on the API responses."""
    try:
        chaine_content = reponse[0]["query"][reponse[1]]
    except KeyError:
        error = True
        chaine_content = "Mais... je n'ai rien à te dire sur " + demande + " !"
    else:
        error = False
    return [chaine_content, error]


def try_page(r, section, terme_recherche, adresse_api, session):
    """Vérifie que la réponse de l'api convient si ce n'est pas le cas 
    test une autre request.
    Check that the API response is appropriate if it is not
    test another request."""

    reponse = r.json()
    try:
        chaine_content = reponse["query"][section]
        if len(chaine_content.get('-1')) > 0:
            parametres = config_request_demande_loc(terme_recherche)
            section = "search"
            r = session.get(url=adresse_api, params=parametres)
            return [r, section]
    except BaseException:
        return []


def gestion_chaine(chaine):
    """Permet de récupérer la totalité ou partie de la réponse selon la demande
    de l'utilisateur.
    Allows you to recover all or part of the response according to the request
    of the user."""
    if chaine.find('homonymes') != - \
            1 or chaine.find('homonymie') != -1:
        homonyme_chaine = chaine.split(".")
        del homonyme_chaine[0]
        s = "."
        chaine = s.join(homonyme_chaine)
    chaine_parser = BeautifulSoup(chaine, 'html.parser')
    chaine_finale = chaine_parser.get_text()
    return chaine_finale
