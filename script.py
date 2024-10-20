"""
Ce programme est composé de quatre fichiers : le fichier principal script.py qui permet de lancer le programme
dans un terminal, le fichier fonction Fonctions.py qui contient toutes les fonctions utilisées dans le script,
le fichier Constantes.py qui contient toutes les constantes nécessaires au bon fonctionnement de ce script et 
enfin le fichiers Mes_classes.py où sont logées toutes les classes utilisées dans le script. 
Il n'est donc pas utile de rappeler que, pour que ce programme fonctionne, tous ces quatre fichiers doivent 
impérativement être mis dans le même dossier - pourquoi pas les laisser dans le repertoire d'actuel, Bibliothèque.

Lorsqu'on joue avec ce programme, quatorze tâches sont possibles et visibles dès le lancement du script, à partir
du fichier principal, script.py. 
Pour profiter pleinement du potentiel offert par ce programme, il est conseillé de commencer par charger des données 
en choisissant l'option '0' puis en utilisant le mot de passe 'admin'. Les données qui seront chargées sur la mémoire
de travail de votre ordinanteur sont de deux natures : d'une part des Administrateurs (admin) et des Usagers (usager) 
et d'autre part un ensembre de livres. 
Si en revanche, vous souhaitez créer vos propres utilisateurs, pensez bien à leur attribuer le nom et prénom - pour 
distinguer des utilisateurs ayant le même nom de famille - et un statut (admin ou usager). Le statut, c'est ce qui 
confère à l'utilisateur des autorisations pour réaliser ou non certaines tâches, ainsi un utilisateur avec le statut 
d'admin pourra ajouter des livres, tandis que celui avec le statut d'usager ne sera pas autorisé à effectuer cette tâche.

Une fois que les utilisateurs sont créés, si vous le souhaitez, vous pouvez ajouter vos propres livres.Il va donc falloir
renseigner pour chaque livre les paramètres suivant: l'ISBN, titre, auteur et la classe (livre papier ou numérique) à 
laquelle appartient le livre. Dans le programme le mot qui représente l'appartenance à la classe est "type_id".
Avant d'exécuter une tâche nécessitant une autorisation, comme par exemple supprimer un utilisateur,le programme 
va demander, par un message, de lui fournir le nom et prénom pour valider l'exécution de la tâche. Dans ce cas,
il faudra lui fournir le nom et le prénom d'un Administrateur. Pour le reste, l'exécution du programme reste assez 
lisible d'autant que celle-ci demande par message tout ce qu'elle a besoin.

Enfin, ce programme offre la possibilité de sauvegarder des données dans plusieurs fichiers json. Pour ce faire, 
il suffit simplement de choisir l'option 10 (sauvegarder les données) ; cinq fichiers seront ainsi automatiquement
créés:

01.json, contiendra un dictionnaire (clé = nom et prénom, valeur = type_id) contenant tous les utilisateurs qui ont 
été fournis au programme.

02.json, y figure un dictionnaire (clé = ISBN, valeur = {"titre": titre, "auteur": auteur, "type_id": type_id}) 
contenant tous les livres (papiers ou numériques) disponibles au moment de la sauvegarde.

03.json, quant à lui, va contenir un dictionnaire ne contenant que des livres papiers disponibles au moment de 
la sauvegarde.

04.json, à l'inverse du fichier 03.json, ne contiendra qu'un dictionnaire des livres numériques.

05.json, contrairement aux trois précédents fichiers, il contiendra bien un dictionnaire dans lequel la clé
sera l'ISBN du livre emprunté et la valeur, un tuple, composé du nom de l'emprunteur et de la valeur de la
clé ISBN tel qu'il figurait dans les précédents dictionnaires avant l'emprunt. Vous l'aurez compris,
ce dernier fichier json contiendra toutes les informations nécessires sur le livre emprunté et sur la personne 
ayant emprunté le livre.
"""

import sys

from Constantes import MESSAGE_ACCUEIL, CHOIX_POSSIBLES, MESSAGE_01, MESSAGE_02, MESSAGE_03, MESSAGE_04, MESSAGE_05, MESSAGE_06, MESSAGE_09, MESSAGE_12
from Mes_Classes import Bibliotheque, Utilisateur, LivrePapier, LivreNumerique
from Fonctions import statut_utilisateur, validation, parametres, donnees


print(MESSAGE_ACCUEIL)

while True:
    choix = input(MESSAGE_01)

    if choix not in CHOIX_POSSIBLES:
        print(MESSAGE_02)

    if choix == "0":
        mot_passe = input(MESSAGE_09)
        print(Bibliotheque("La Bibliothèque de Docstring").charger_donnees(mot_passe))


    elif choix == "1":
        nom = input(MESSAGE_04).lower()
        statut = input("Statut : usager ou admin ? ")
        print(Bibliotheque("La Bibliothèque de Docstring").ajouter_utilisateur(nom, statut))
    

    elif choix == "2":
        isbn, titre, auteur, type_id = donnees()
        nom = input(MESSAGE_06).lower()
        statut = statut_utilisateur(nom)
        print(Utilisateur(nom, statut).ajouter_livre(isbn, titre, auteur, type_id))

    elif choix == "3":
        isbn = input(MESSAGE_12)
        nom = input(MESSAGE_06).lower()
        statut = statut_utilisateur(nom)
        print(Utilisateur(nom, statut).supprimer_livre(isbn))

    elif choix == "4":
        mot = input("Mot-clé (ISBN, Titre ou Auteur) : ")
        nom = input(MESSAGE_04).lower()
        statut = statut_utilisateur(nom)
        print(Utilisateur(nom, statut).rechercher_livre(mot))

    elif choix == "5":
        while True:
            isbn = input("ISBN, un nombre à treize chiffre : ")
            nom_emprunteur = input("Nom et prénom de l'emprunteur : ").lower()
            nom = input(MESSAGE_06)       
            if nom_emprunteur in Bibliotheque.mon_dico and nom in Bibliotheque.mon_dico:
                statut = Bibliotheque.mon_dico.get(nom)
                break
            print(f"{nom_emprunteur} n'est pas connu du système.")

        print(Utilisateur(nom, statut).emprunter_livre(isbn, nom_emprunteur))
    
    elif choix == "6":
        while True:
            isbn = input("ISBN : ? ")
            nom_emprunteur = (input("Nom et prénom de l'emprunteur, exemple : Leduc Tom ? ")).lower()
            nom = input(MESSAGE_06).lower()
            statut = statut_utilisateur(nom)

            if statut == "inconu":
                print(f"{nom} n'est pas habilité à effectuer cette opération.")
            elif statut != "inconnu":
                break
            
        print(Utilisateur(nom, statut).retourner_livre(isbn, nom_emprunteur))

    elif choix == "7":
        nom, statut = validation()
        print(Utilisateur(nom, statut).lister_livre())

    elif choix == "8":
        nom, statut = parametres()
        print(Bibliotheque("La Bibliothèque de Docstring").statistiques(statut))
    
    elif choix == "9":
        nom, statut = parametres()
        print(Bibliotheque("Docstring").lister_utilisateur(nom, statut))
    
    elif choix == "10":
        nom, statut = parametres()
        print(Bibliotheque("La Bibliothèque de Docstring").sauvegarder(nom, statut))
    
    elif choix == "11":
        nom = input(MESSAGE_05).lower()
        nom_op = input(MESSAGE_06).lower()
        print(Bibliotheque("La Bibliothèque de Docstring").supprimer_utilisateur(nom, nom_op))

    elif choix == "12":
        isbn, titre, auteur, type_id, isbn_n, titre_n, auteur_n, type_id_n = donnees()
        if type_id == "papier":
            print(LivrePapier(isbn, titre, auteur, type_id="papier").modifier(isbn_n, titre_n, auteur_n, type_id_n="papier"))
        elif type_id == "numerique":
            print(LivreNumerique(isbn, titre, auteur, type_id="numerique").modifier(isbn_n, titre_n, auteur_n, type_id_n="numerique"))            
    
    elif choix == '13':
        print(MESSAGE_03)
        sys.exit()
        