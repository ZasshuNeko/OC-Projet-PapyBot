# -*-coding:Utf-8 -*

""" This file file contains the class managing the creation of the response in json.
Ce Fichier fichier contient la classe gérant la création de la réponse en json."""

import json


class Sourcejson():
    """Cette classe permet de completer la réponse des apis puis de former 
    un json renvoyé vers le code en javascript.
    This class allows you to complete the API response and then train
    a json returned to the code in javascript."""
    def __init__(self):
        self.warning = "<li class='list-group-item list-group-item-warning'>Vous : "
        self.success = "<li class='list-group-item list-group-item-success'>"
        self.end = "</li>"

    def creation_json(self, demande, gestion_demande):
        """Gestion du json à envoyer vers Ajax.
        Management of the json to send to Ajax."""
        if len(gestion_demande[0]) >= 1:
            resultat = self.return_var(
                util=demande,
                google=gestion_demande[0][0],
                loc=gestion_demande[2],
                ad=gestion_demande[3],
                opt=gestion_demande[0],
                wiki=gestion_demande[1])
        elif len(gestion_demande[1]) == 0:
            resultat = self.return_var(util=demande)
        else:
            resultat = self.return_var(
                util=demande,
                loc=gestion_demande[2],
                ad=gestion_demande[3],
                wiki=gestion_demande[1])

        dictionnaire = {
            'resultat': resultat[0],
            'url_google': resultat[2],
            'localisation': resultat[3],
            'wiki': resultat[1]}
        fichier_json = json.dumps(dictionnaire)
        return fichier_json

    def return_var(self, **dict_var):
        """retour des informations pour le json.
        feedback for the json."""
        demande = self.warning + dict_var.get("util") + self.end
        if (dict_var.get("wiki")):
            papy_wiki = self.success + "<p>Papy :" + \
                dict_var.get("wiki") + "</p>" + self.end
            if (dict_var.get("opt")):
                url_google = dict_var.get("google")
                reponse_papy = self.papy_reponse(
                    dict_var.get("loc"), dict_var.get("ad"), dict_var.get("opt"))
            else:
                url_google = [{}]
                reponse_papy = self.papy_reponse(
                    dict_var.get("loc"), dict_var.get("ad"))
        else:
            reponse_papy = self.success + \
                "Papy : Petit ... ne sais-tu pas faire des phrases ?" + self.end
            papy_wiki = ""
            url_google = [{}]

        return [demande, papy_wiki, url_google, reponse_papy]

    def papy_reponse(self, salutation, boolean_error,
                     *adresse):
        """Complète la réponse du bot.
        Complete the bot response."""
        if boolean_error:
            indication_papy = self.success + \
                "Papy : Hmmmm attends ...heu..." + self.end
        else:
            selection_adresse = self.try_adress(adresse)
            if len(selection_adresse) >= 2 and isinstance(
                    selection_adresse, list):
                lieu = selection_adresse[1]
                indication_papy = self.reponse(lieu)
            elif isinstance(selection_adresse, str):
                indication_papy = self.success + \
                    selection_adresse + self.end
            else:
                if isinstance(selection_adresse, str):
                    indication_papy = selection_adresse
                else:
                    indication_papy = "Voyons, il y a beaucoup d'endroits pour tous te les citer"

            indication_papy = self.success + "Papy : " + \
                salutation + "</br>" + indication_papy + self.end
        return indication_papy

    def reponse(self, adresse):
        """Format une indication avec l'adresse trouvé.
        Format an indication with the address found."""
        indication_papy = "Alors mon petit ! Sache que cela est situé " + \
            adresse
        return indication_papy

    def try_adress(self, adresse):
        """Test si une carte doit être généré.
        Test if a map should be generated."""
        try:
            selection_adresse = adresse[0]
        except BaseException:
            selection_adresse = "Papy : Au vu de ta question ...Une carte serait superflue !"
        return selection_adresse
