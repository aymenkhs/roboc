# -*-coding:Utf-8 -*


import socket
import select
import time

class Serveur:
	""" classe qui vas definir un serveur avec tous ce que sa implique comme action"""
	def __init__(self):

		self.host = "localhost"
		self.port = 12500
		self.client_connecter = []
		self.nombre_de_client = 0

	def demarrer(self):
		""" intialiser et demarrer le serveur """

		self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		self.socket.bind((self.host , self.port))
		self.socket.listen(5)

		print("serveur en ecoute sur {} : {} , attente des joueurs".format(self.host , self.port))


	def arreter(self , client_gagnant = -1):
		""" envoyer un signal aux client et metre un terme a toutes les connexions"""		
		self.envoie_msg_tous("La partie est fini")
		if client_gagnant != -1:
			self.envoie_msg_tous("le joueur n°{} a gangner".format(client_gagnant))
		else:
			self.envoie_msg_tous("connexion interompue par le serveur")
		
		time.sleep(2)
		self.socket.close()

	def  attente_clients(self , labyrinthe):
		""" attente de la connexion de clients jusqu'a ce que l'un d'entre eux envoie le signal de debut """

		attente_joueur = True #tant que cette attribut sera a true on continue d'accepter les clients

		while attente_joueur:
	
			connexion_dem , wlist, xlist = select.select([self.socket] , [] , [] , 0.05)
	
			for connexion in connexion_dem:
				conexion_avec_joueur , info_conex = self.socket.accept()
				self.client_connecter.append(conexion_avec_joueur)
				self.nombre_de_client += 1
				labyrinthe.cree_robot()

			a_lire = []
			try:
				a_lire , wlist , xlist = select.select(self.client_connecter ,[] , [] , 0.05)
			except select.error:
				pass
			else:
				for client in a_lire:
					msg_recu = client.recv(1024)
					if msg_recu.lower() == b"commencer la partie":
						attente_joueur = False

		# on envoie a tous les joueurs que la partie a commancer ensuite on leur envoie a chacun le labyrinthe
		self.envoie_msg_tous("debut")
		self.envoie_map(labyrinthe)


	def envoie_msg(self , client , message):
		""" envoie une chaine de caractere au client """
		if client >= self.nombre_de_client:
			raise ValueError("client non existant")

		connexion = self.client_connecter[client]
		connexion.send(message.encode())

	def envoie_msg_tous(self , message):
		""" envoie une chaine de caractere a tous les clients"""

		for conn in self.client_connecter:
			conn.send(message.encode())

	def envoie_map(self , labyrynthe):
		""" envoie le labyrinthe a tous les joueurs """
		
		for index , conn in enumerate(self.client_connecter):
			conn.send(b"lab")
			grille = labyrynthe.get_grille(index)
			conn.send(grille.encode())
			time.sleep(0.1)

	def reception_msg(self , client):
		""" attente de recption d'un message de la part d'un client """
		if client >= self.nombre_de_client:
			raise ValueError("client non existant")

		conn = self.client_connecter[client]
		message = conn.recv(1024).decode()
		return message


	def supp_client(self , client):
		""" suprimer un client qui veut quiter la partie"""

		if client >= self.nombre_de_client:
			raise ValueError("client non existant")

		conn = self.client_connecter[client]
		conn.close()

		del self.client_connecter[client]

		self.nombre_de_client -= 1

		self.envoie_msg_tous("un joueur en moin")
		self.envoie_msg_tous("le joueur n°{} a quiter la partie".format(client + 1))
