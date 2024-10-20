from Constantes import MESSAGE_01, MESSAGE_02, MESSAGE_04, MESSAGE_06, MESSAGE_11, CHOIX_POSSIBLES, CHOIX_TYPES
from Mes_Classes import Bibliotheque


def choix_utilisateur():
    while True:
        choix = input(MESSAGE_01)

        if choix not in CHOIX_POSSIBLES:
            print(MESSAGE_02)
        
        else: 
            return choix


def statut_utilisateur(nom):
    return Bibliotheque.mon_dico.get(nom, "inconnu")


def parametres():
    nom = input(MESSAGE_06).lower()
    statut = statut_utilisateur(nom)
    return (nom, statut)


def validation():
    while True:
            nom = input(MESSAGE_04).lower()
            statut = statut_utilisateur(nom)
            if statut == "inconnu":
                return MESSAGE_11
            elif statut != "inconnu":
                break
    
    return [nom, statut]

def donnees():
    titre = (input("Ancien titre : ")).lower()
    titre_n = (input("Nouveau titre : ")).lower()
    auteur = (input("Anciens nom et prénom de l'auteur : ")).lower()
    auteur_n = (input("Nouveau nom et prénom de l'auteur : ")).lower()

    while True:
        isbn = input("Ancien ISBN, un nombre de treize chiffres : ")
        isbn_n = input("Nouveau ISBN, un nombre de treize chiffres : ")
        if isbn.isdigit() and len(isbn) == 13:
            break

    while True:
        type_id = (input("Ancien type : papier ou numerique ? : ")).lower()
        type_id_n = (input("Nouveau type : papier ou numerique ? : ")).lower()
        if type_id in CHOIX_TYPES:
            break
    
    return (isbn, titre, auteur, type_id, isbn_n, titre_n, auteur_n, type_id_n)