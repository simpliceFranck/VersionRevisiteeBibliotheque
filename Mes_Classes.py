import os, json
from textwrap import dedent

from Constantes import DOSSIER_DATA, MESSAGE_06, MESSAGE_07, MESSAGE_08, MESSAGE_10, MESSAGE_11, MESSAGE_13



class Livre(dict):
    def __init__(self, isbn, titre, auteur):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
    
    def modifier(self, isbn_n, titre_n, auteur_n, type_id_n):
        Utilisateur.mes_livres.pop(self.isbn)
        Utilisateur.mes_livres[isbn_n] = {"titre": titre_n, "auteur": auteur_n, "type_id": type_id_n}

    

class LivrePapier(Livre):
    def __init__(self, isbn, titre, auteur, type_id="papier"):
        super().__init__(isbn, titre, auteur)
        self.type_id = type_id
    
    def modifier(self, isbn_n, titre_n, auteur_n, type_id_n):
        super().modifier(isbn_n, titre_n, auteur_n, type_id_n)
        Utilisateur.mes_livres1.pop(self.isbn)
        Utilisateur.mes_livres1[isbn_n] = {"titre": titre_n, "auteur": auteur_n, "type_id": type_id_n}
        return "La mise à jour a été exécutée avec succès."



class LivreNumerique(Livre):
    def __init__(self, isbn, titre, auteur, type_id="numerique"):
        super().__init__(isbn, titre, auteur)
        self.type_id = type_id
    
    def modifier(self, isbn_n, titre_n, auteur_n, type_id_n):
        super().modifier(isbn_n, titre_n, auteur_n, )
        Utilisateur.mes_livres2.pop(self.isbn)
        Utilisateur.mes_livres2[isbn_n] = {"titre": titre_n, "auteur": auteur_n, "type_id": type_id_n}
        return "La mise à jour a été exécutée avec succès."


class Utilisateur(dict):
    mes_livres = Livre(9, "Docstring", "NKOUARI")  # Dictionnaire contenant tous les livres (papiers comme numeriques) disponibles à l'emprunt.
    mes_livres1 = Livre(10, "Docstring", "NKOUARI")  # Dictionnaire contenant uniquement des livres papiers disponibles à l'emprunt.
    mes_livres2 = Livre(11, "Docstring", "NKOUARI")  # Dictionnaire contenant uniquement des livres numériques disponibles à l'emprunt.
    mes_livres3 = Livre(12, "Docstring", "NKOUARI")  # Dictionnaire contenant tous les livres (papiers ou numérique) empruntés.


    def __init__(self, nom, statut):
        self.nom = nom
        self.statut = statut


    def ajouter_livre(self, isbn, titre, auteur, type_id):
        if self.statut == "usager":
            return MESSAGE_07

        elif self.statut == "admin" and isbn not in Utilisateur.mes_livres:
            if type_id == "papier":
                LivrePapier(isbn, titre, auteur)
                Utilisateur.mes_livres1[isbn] = {"titre": titre, "auteur": auteur, "type_id": type_id}
                Utilisateur.mes_livres[isbn] = {"titre": titre, "auteur": auteur, "type_id": type_id}               
            elif type_id == "numerique":
                LivreNumerique(isbn, titre, auteur)
                Utilisateur.mes_livres2[isbn] = {"titre": titre, "auteur": auteur, "type_id": type_id}
                Utilisateur.mes_livres[isbn] = {"titre": titre, "auteur": auteur, "type_id": type_id}
            return f"{titre} (ISBN = {isbn}) a bien été mis en stock."
        
        elif self.statut == "admin" and isbn in Utilisateur.mes_livres:
            return f"{titre} (ISBN = {isbn}) existe déjà en stock."
        
        else:
            return MESSAGE_11
    

    def supprimer_livre(self, isbn):
        if self.statut == "usager":
            return MESSAGE_07

        elif self.statut == "admin" and isbn in Utilisateur.mes_livres1:
            Utilisateur.mes_livres1.pop(isbn)
            Utilisateur.mes_livres.pop(isbn)
            return f"Le livre (ISBN = {isbn}) a été supprimé."
        
        elif self.statut == "admin" and isbn in Utilisateur.mes_livres2:
            Utilisateur.mes_livres2.pop(isbn)
            Utilisateur.mes_livres.pop(isbn)
            return f"Le livre (ISBN = {isbn}) a été supprimé."
        
        return MESSAGE_13
        


    def rechercher_livre(self, mot):
        if len(Utilisateur.mes_livres) == 0:
            return "Aucun livre n'est disponible !"

        if mot.isdigit() and Utilisateur.mes_livres.get(mot, "introuvable") != "introuvable":
            titre = Utilisateur.mes_livres.get(mot)["titre"]
            auteur =Utilisateur.mes_livres.get(mot)["auteur"] 
            type = Utilisateur.mes_livres.get(mot)["type_id"]
            return dedent(f"""
                          ISBN : {mot}\n  
                          Titre : {titre}\n  
                          Auteur : {auteur}\n  
                          Type : {type}""")
                   
        for valeur in Utilisateur.mes_livres.values():
            if valeur["titre"] == mot:
                for elt in Utilisateur.mes_livres:
                    if Utilisateur.mes_livres[elt] == valeur:
                        return dedent(f"""
                                      ISBN : {elt} \n
                                      Titre : {mot} \n 
                                      Auteur : {valeur["auteur"]} \n 
                                      Type : {valeur["type_id"]}""")
            
            elif valeur["auteur"] == mot:
                for elt in Utilisateur.mes_livres:
                    if Utilisateur.mes_livres[elt] == valeur:
                        return dedent(f"""
                                      ISBN : {elt} \n
                                      Titre : {valeur["titre"]} \n 
                                      Auteur : {mot} \n 
                                      Type : {valeur["type_id"]}""")
    
        return f"Le mot renseigné ne permet pas de faire aboutir cette recherche."
    

    def emprunter_livre(self, isbn, nom_emprunteur):
        if isbn in Utilisateur.mes_livres:
            valeur = Utilisateur.mes_livres.pop(isbn)
            Utilisateur.mes_livres3[isbn] = (nom_emprunteur, valeur)
            if isbn in Utilisateur.mes_livres1:
                del Utilisateur.mes_livres1[isbn] 
            elif isbn in Utilisateur.mes_livres2:
                del Utilisateur.mes_livres2[isbn]  
            return f"L'emprunt, par {nom_emprunteur}, du livre ({isbn}) est validé."
        
        return f"Désolé, vous ne pouvez emprunter ce livre !"    


    def retourner_livre(self, isbn, nom_emprunteur):
        if isbn in Utilisateur.mes_livres3 and Utilisateur.mes_livres3[isbn][0] == nom_emprunteur: 
            Utilisateur.mes_livres[isbn] = Utilisateur.mes_livres3[isbn][1]
                
            if Utilisateur.mes_livres3[isbn][1]["type_id"] == "papier": 
                Utilisateur.mes_livres1[isbn] = Utilisateur.mes_livres3[isbn][1]

            elif Utilisateur.mes_livres3[isbn][1]["type_id"] == "numerique":
                Utilisateur.mes_livres2[isbn] = Utilisateur.mes_livres3[isbn][1]

            Utilisateur.mes_livres3.pop(isbn)

            return f"{nom_emprunteur} a bien retourné Le livre ayant pour ISBN = {isbn}."
                
        return f"Pas d'emprunt associé à l'ISBN, {isbn}."       
    

    def lister_livre(self):
        return dedent(f"""
                        Livres disponibles en papier : {Utilisateur.mes_livres1}\n
                        Livres disponibles en numérique : {Utilisateur.mes_livres2}\n""")           
    


class Bibliotheque:
    mon_dico = Utilisateur("Bibliothèque Docstring", "Direction")
    _instance = None


    def __new__(cls, nom):
        if not cls._instance:
           cls._instance = super(Bibliotheque, cls).__new__(cls) 

        return cls._instance
    

    def __init__(self, nom):
        self.nom = nom
    

    def ajouter_utilisateur(self, nom, statut):
        Utilisateur(nom, statut)
        Bibliotheque.mon_dico[nom] = statut
        return f"{nom} a été créé avec un statut d'{statut.capitalize()}."
           

    def supprimer_utilisateur(self, nom, nom_op):
        if nom in Bibliotheque.mon_dico and Bibliotheque.mon_dico.get(nom_op, "inconnu") == "admin":
            Bibliotheque.mon_dico.pop(nom)
            return f"{nom} a bien été supprimé de la liste des utilisateurs."
        return MESSAGE_08


    def statistiques(self, statut):
        if statut == "admin":       
            return dedent(f"""
                    Nombre total des utilisateurs : {len(Bibliotheque.mon_dico)} \n
                    Nombre total des livres disponibles : {len(Utilisateur.mes_livres)} \n
                    Nombre total des livres papiers disponibles : {len(Utilisateur.mes_livres1)} \n
                    Nombre total des livres numeriques disponibles : {len(Utilisateur.mes_livres2)} \n
                    Nombre total des livres empruntés : {len(Utilisateur.mes_livres3)}""")
        return MESSAGE_07
    

    def lister_utilisateur(self, nom, statut):
        if Utilisateur(nom, statut).statut != "admin":
            return MESSAGE_07
        
        return Bibliotheque.mon_dico
    

    def sauvegarder(self, nom, statut):
        if statut != "admin":
            return MESSAGE_07
        
        for i, nom in enumerate([Bibliotheque.mon_dico, Utilisateur.mes_livres, Utilisateur.mes_livres1, Utilisateur.mes_livres2, Utilisateur.mes_livres3]):
            indice = f"{i+1}"
            chemin = os.path.join(DOSSIER_DATA, f"{indice.zfill(2)}.json")

            if not os.path.exists(DOSSIER_DATA):
                os.makedirs(DOSSIER_DATA)

            with open(chemin, "w", encoding="utf-8") as f:
                json.dump(nom, f, indent=4, ensure_ascii=False)
        
        return "Les données ont été sauvegardées avec succès."
    

    def charger_donnees(self, mot_passe):
        if mot_passe != "admin":
            return MESSAGE_10
        
        for i, nom in enumerate([Bibliotheque.mon_dico, Utilisateur.mes_livres, Utilisateur.mes_livres1, Utilisateur.mes_livres2, Utilisateur.mes_livres3]):
            indice = f"{i+1}"
            chemin = os.path.join(DOSSIER_DATA, f"{indice.zfill(2)}.json")

            if os.path.exists(chemin) and nom == Bibliotheque.mon_dico:
                with open(chemin, "r", encoding="utf-8") as f:
                    Bibliotheque.mon_dico = json.load(f)
            
            elif os.path.exists(chemin) and nom == Utilisateur.mes_livres:
                with open(chemin, "r", encoding="utf-8") as f:
                    Utilisateur.mes_livres = json.load(f)
            
            elif os.path.exists(chemin) and nom == Utilisateur.mes_livres1:
                with open(chemin, "r", encoding="utf-8") as f:
                    Utilisateur.mes_livres1 = json.load(f)
            
            elif os.path.exists(chemin) and nom == Utilisateur.mes_livres2:
                with open(chemin, "r", encoding="utf-8") as f:
                    Utilisateur.mes_livres2 = json.load(f)

            elif os.path.exists(chemin) and nom == Utilisateur.mes_livres3:
                with open(chemin, "r", encoding="utf-8") as f:
                    Utilisateur.mes_livres3 = json.load(f)

            else:
                return "Aucune donnée dans le répertoire concerné."            

        return "Les données ont été chargées."


if __name__ == "__main__":
    Bibliotheque("Docstring").ajouter_utilisateur("NKOUARI Franck", "admin")
    print(Bibliotheque.mon_dico)
    print(Utilisateur("NKOUARI Simplicia", "usager").lister_livre()) 