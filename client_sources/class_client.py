# -*-coding:Utf-8 -*

import socket

class Client:
	""" classe qui definit un client"""
	def __init__(self):
		self.host = "localhost"
		self.port = 12500

		self.fin = False # atribut qui marque la fin du programme qui se mets a True quand un joueur gagne la partie
		# ou que le joueur quitte la partie

		self.debut = False # attribut qui est a False tant qu'aucun joueur n'a lancer la partie

		self.toure_du_joueur = False # attribut qui se mets a True quand c'est au tour du joueur et qui se remet a False apres avoir envoyer une commande
		# si la commande n'est pas accepter par le serveur un message d'erreur sera envoyer et l'atribut sera remis a True

		self.action_rater = False # attribut qui se mets a True quand une action est refuser par le serveur et se remets a false apres un traitement

	def connexion(self):
		""" methode appeler pour connecter le client au serveur"""

		self.connexion = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.connexion.connect((self.host, self.port))


	def deconnexion(self):
		""" methode appeler a la deconnexion du client """

		print("Fermeture de la connexion")
		self.connexion.close()


	def envoie(self , msg):
		""" envoie un message"""
		
		self.connexion.send(msg.encode())

	def reception(self):
		""" recois un message du serveur et le retourne """

		return self.connexion.recv(1024).decode()

