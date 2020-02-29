# -*-coding:Utf-8 -*

import os

from server_sources.mod_server import *
from server_sources.class_server import Serveur
from server_sources.Labyrinthe import Labyrinthe
from server_sources.carte import Carte
from server_sources.exceptions import *

host = ""
port = 12500

# on commence par lire les nom des fichier contenue dans le dossier 'cartes' et on les stocke pour permetres a l'utilisateur de choisir
cartes_existantes = []

for nom_fichier in os.listdir("cartes"):
	if nom_fichier.endswith(".txt"):
		cartes_existantes.append(nom_fichier[:len(nom_fichier) - 4])

#on demande a l'utilisateur de choisir une des carte via la fonction choix qui se charge d'afficher les cartes
#puis de renvoyer le choix de l'utilisateur
carte_choisit = choix(cartes_existantes)

# on intialise nos objets carte ,labyrinthe puis serveur
ma_carte = Carte(carte_choisit)
mon_labyrinthe = Labyrinthe(ma_carte.creation_obstacles())

serveur = Serveur()
serveur.demarrer()

# on attent la connexion de client via la methode de serveur
serveur.attente_clients(mon_labyrinthe)

toure = 0
print("fin de l'attente debut de la partie")
print("nous avons {} joueurs".format(serveur.nombre_de_client))

while not mon_labyrinthe.fin_partie:

	#on envoie un message au joueur dont c'est le toure et on attent sa reponse
	serveur.envoie_msg(toure , "c'est a vous de jouer")
	commande = serveur.reception_msg(toure)
	
	if commande == "quiter":
		#on fait quiter le joueur de la partie avec tous ce que ca implique
		
		print("le joueur n°{} a quiter la partie".format(toure + 1))		
		
		serveur.supp_client(toure)
		del mon_labyrinthe.robots[toure]
		
		if serveur.nombre_de_client == 0: # si c'est le dernier client qui as quiter la partie elle est finit
			mon_labyrinthe.fin_partie = True
		continue

	elif commande == "murer":
		# si la commande est 'murer' on attent que le client envoie la direction 

		direction = serveur.reception_msg(toure)
		
		try:
			# si il est impossible de faire l'action une exception sera lever 
			mon_labyrinthe.murer(direction , toure)		
		except MurerImpossible as message:
			serveur.envoie_msg(toure , "action impossible")
			serveur.envoie_msg(toure , str(message))
			continue
		else:
			serveur.envoie_msg(toure , "action reussi")
			print("le joueur n°{} a murer la porte '{}'".format(toure + 1 , direction))

	elif commande == "percer":

		direction = serveur.reception_msg(toure)

		try:
			# si il est impossible de faire l'action une exception sera lever
			mon_labyrinthe.percer(direction , toure)
		except PercerImpossible as message:
			serveur.envoie_msg(toure , "action impossible")
			serveur.envoie_msg(toure , str(message))
			continue
		else:
			serveur.envoie_msg(toure , "action reussi")
			print("le joueur n°{} a percer le mur '{}'".format(toure + 1 , direction))
	
	else:
		
		try:
			# si il est impossible de faire l'action une exception sera lever
			mon_labyrinthe.deplacement(commande , toure)
		except DeplacementImpossible as message:
			serveur.envoie_msg(toure , "action impossible")
			serveur.envoie_msg(toure , str(message))
			continue
		else:
			serveur.envoie_msg(toure , "action reussi")
			print("le joueur n°{} c'est deplacer '{}'".format(toure + 1 , commande))

	# on envoie le labyrinthe a tous les joueurs
	serveur.envoie_map(mon_labyrinthe)

	toure += 1
	if toure >= serveur.nombre_de_client:
		toure = 0

if toure == 0:
	toure = serveur.nombre_de_client

print("FELICITATION ,le joueur {} a ganger la partie".format(toure))

serveur.arreter(toure)