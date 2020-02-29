# -*-coding:Utf-8 -*

from threading import Thread , RLock
import socket

verrou = RLock()

class Recevoir(Thread):
	"""thread en charge de recevoir les message du serveur et les traiter"""
	def __init__(self , connexion):
		Thread.__init__(self)
		self.connexion = connexion

	def run(self):
		# on definit message comme variable global (qui est definit dans le module mod_client)

		while not self.connexion.fin:
			
			msg_recu = self.connexion.reception()
			
			if msg_recu == "debut":
				
				if not self.connexion.debut:
					with verrou:
						self.connexion.debut = True
						print("la partie vas commencer")
			
			elif msg_recu == "c'est a vous de jouer":
		
				with verrou:
					self.connexion.toure_du_joueur = True
					print(msg_recu)
					print("saisisser la commande souhaiter...")	

			elif msg_recu == "action impossible":
				
				arecpt = self.connexion.reception()
				with verrou:
					self.connexion.toure_du_joueur = True
					self.connexion.action_rater = True
					print(arecpt)	
					print("veuiller réesayer")
					
			elif msg_recu == "un joueur en moin":
				
				arecpt = self.connexion.reception()
				with verrou:				
					print(arecpt)	
							
			elif msg_recu == "La partie est fini":
			
				arecpt = self.connexion.reception()
				with verrou:
					self.connexion.fin = True				
					print(arecpt)
				
			elif msg_recu == "lab":			
				arecpt = self.connexion.reception()
				with verrou:
					print("voici l'etat actuelle du labyrinthe\n\n")
					print(arecpt)	
