# -*-coding:Utf-8 -*

"""Ce Fichier fichier contient le corp de l'application."""

import json


class Sourcejson():
    def __init__(self):
        self.warning = "<li class='list-group-item list-group-item-warning'>Vous : "
        self.success = "<li class='list-group-item list-group-item-success'>"
        self.end = "</li>"

    def creation_json(self, demande, gestion_demande):
        """Gestion du json à envoyer vers Ajax"""
        if len(gestion_demande[0]) >= 1:
            resultat = self.return_var(util=demande,google=gestion_demande[0][0],loc=gestion_demande[2],ad=gestion_demande[3],opt=gestion_demande[0],wiki=gestion_demande[1])   
        elif len(gestion_demande[1]) == 0:
            resultat = self.return_var(util=demande)
        else:
            resultat = self.return_var(util=demande,loc=gestion_demande[2],ad=gestion_demande[3],wiki=gestion_demande[1])

        dictionnaire = {
            'resultat': resultat[0],
            'url_google': resultat[2],
            'localisation': resultat[3],
            'wiki': resultat[1]}
        fichier_json = json.dumps(dictionnaire)
        return fichier_json

    def return_var(self,**dict_var):
        """retour des informations pour le json"""
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
            reponse_papy = self.success + "Papy : Petit ... ne sais-tu pas faire des phrases ?" + self.end
            papy_wiki = ""
            url_google = [{}]

        return [demande,papy_wiki,url_google,reponse_papy]


    def papy_reponse(self, salutation, boolean_error,
                     *adresse):
        """Génère la réponse de papy."""
        if boolean_error:
            indication_papy = self.success + \
                "Papy : Hmmmm attends ...heu..." + self.end
        else:
            selection_adresse = self.try_adress(adresse)
            if len(selection_adresse) >= 2 and type(selection_adresse) is list:
                lieu = selection_adresse[1]
                ss_chaine = str(lieu[0:1])
                if ss_chaine.isalpha() == False:
                    indication_papy = self.reponse_add(lieu)
                else:
                    indication_papy = self.reponse_nom(lieu)
            elif type(selection_adresse) is str:
                indication_papy = self.success + \
                    selection_adresse + self.end
            else:
                if type(selection_adresse) is str:
                    indication_papy = selection_adresse
                else:
                    indication_papy = "Voyons, il y a beaucoup d'endroit pour tous te les citer"
            
            indication_papy = self.success + "Papy : " + \
                salutation + "</br>" + indication_papy + self.end
        return indication_papy

    def reponse_nom(self, adresse):
        """Réponse formaté avec nom devant l'adresse."""
        texte_papy = adresse.split(",")
        x = 0
        if len(texte_papy) > 1:
            while x <= len(adresse):
                if x == 0:
                    indication_papy = "Alors mon petit ! Sache que " + \
                        texte_papy[x]
                elif x == 1:
                    indication_papy = indication_papy + \
                        " est situé " + texte_papy[x]
                elif x == 2:
                    indication_papy = indication_papy + \
                        " code postal " + texte_papy[x]
                x += 1
        return indication_papy

    def reponse_add(self, adresse):
        """Réponse formaté sans le nom de la recherche."""
        texte_papy = adresse.split(",")
        x = 0
        if len(texte_papy) > 1:
            while x <= len(adresse):
                if x == 0:
                    indication_papy = "Alors mon petit ! Sache que cela est situé " + \
                        texte_papy[x]
                elif x == 1:
                    indication_papy = indication_papy + \
                        " code postal " + texte_papy[x]
                x += 1
        return indication_papy

    def try_adress(self,adresse):
        try:
            selection_adresse = adresse[0]
        except:
            selection_adresse = "Papy : Au vu de ta question ...Une carte serait superflu !"
        return selection_adresse

