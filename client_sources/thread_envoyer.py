# -*-coding:Utf-8 -*

from threading import Thread , RLock
import socket
import time

verrou = RLock()

# les differentes commandes dans un dictionnaire pour facilite l'acces et la modification du programme et le rendre plus lisible
# si on veut modifier une commande on le fait uniquement ici sans avoir a toucher le reste du programme
commandes = {
	"c" : "commencer la partie",
	"n" : "nord",
	"s" : "sud",
	"e" : "est",
	"o" : "ouest",
	"m" : "murer",
	"p" : "percer",
	"q" : "quiter"
}


class Envoyer(Thread):
	""" thread en charge de recevoir les commandes du client de les traiter et de les envoyer au serveur"""	
	def __init__(self , connexion):
		Thread.__init__(self)
		self.connexion = connexion 

		self.a_refaire = {
			"direction" : "aucune",
			"nombre" : 0
		}
		# a_refaire -> dictionnaire qui stock le nombre de fois ou il faut repeter un mouvement dans le cas ou par exemple
		# l'utilisateur entre la commande nord 3 on stock ces information et on renvoie la commande 'nord' au serveur a chaque tour du joueur (le nombre de fois qu'il a choisit ,ici 3) 
		# si le serveur se heurte a une erreur on reintialise le dictionnaire et on demande au joueur de ressaisir une commande
		

	def run(self):
		#le thread est en activite tant que la partie n'est pas fini pour le joueur
		while not self.connexion.fin:

			self.analyse() # la methode annalyse sert juste a verifier l'attribut de 'connexion' "action_rater"
			# si elle est a true elle vas se charger d'annuler les mouvement en cours de a_refaire (plus d'info dans la methode)

			
			if self.a_refaire["nombre"] > 0:
				# si il y as une action a refaire (par ex : le joueur a entrer n3 -> on doit refaire l'action 3 fois)
				if self.connexion.toure_du_joueur:
					# si il y as une action a refaire et que c'est le tour du joueur on l'envoie dirrectement au serveur
					
					self.connexion.envoie(self.a_refaire["direction"])
					
					self.a_refaire["nombre"] -= 1
					
					# vu qu'on a executer une action ce n'est plus le toure du joueur
					with verrou:
						self.toure_du_joueur = False

					time.sleep(0.1)
				
				else:
					# on arrete le progrm pour 1/2 seconde pour eviter que le progrme ne boucle trop souvant
					# sinon il continuera a boucler tant que ce ne sera pas le tour du joueur
					time.sleep(0.5)
			
			else: # si il n'y as pas d'action a refaire:
				
				# cette condition n'est pas vraiment importante elle affiche juste un message si la partie n'a pas commencer
				if not self.connexion.debut:
					self.afficher("saisisser la commande indiquer pour commencer la partie...")
				
				a_envoyer = input() # on attende que le joueur entre une commande
				self.afficher("\n") # purement estetique

				if a_envoyer == "":
					# on traite le cas ou le joueur ne saisit rien (on peut pas l'ingnorer sinon on se retrouve dans le cas ou on traite une chaine vide)
					self.afficher("veuiller entrer quelque choses")
					continue

				ma_commande = a_envoyer[0].lower() # la premiere letre uniquement nous interesse puisque toutes les commande sont sur une letre
				# dans le cas de comnades composer (direction + nombre de fois a faire) ou bien (percer ou murer + direction) on traiteras le reste plus tard

				if ma_commande not in commandes:
					# on traite le cas ou la commande saisit (la premeire letre) n'est pas dans la liste des commandes
					self.afficher("la commande selectionner est invalide")
					continue

				if commandes[ma_commande] == "quiter":
					# si le joueur quite la partie
					self.connexion.envoie(commandes[ma_commande])
					time.sleep(1)

					with verrou:
						self.connexion.fin = True
					
					continue

	
				if not self.connexion.debut:
					# si la partie n'a pas encore commancer la seul commande qu'on peut traiter (a part 'quiter' et 'help') qui sont plus haut
					# est la commnade pour commancer la partie (a savoir 'c')
					if commandes[ma_commande] == "commencer la partie":
						
						self.connexion.envoie(commandes[ma_commande])
						
						with verrou:
							self.connexion.debut = True					
					else:
						# si on entre une tous autre commande elle ne pouras pas etre traiter vu que la partien'as pas encore commancer
						self.afficher("la partie n'a pas encore commencer")				
				
				else: #dans se cas las partie a ddeja commencer

					if commandes[ma_commande] == "commencer la partie":
						# l'utilisateur ne peut plus entrer la commande de debut de partie si elle a deja commencer
						
						self.afficher("la partie a deja commencer")
						continue

					# si on arrive ici c'est que les seul commnse restantes sont les commandes de direction (n,s,o,e), murer(m) et percer(p)
					# maison verifie d'abord si c'est au toure du joueur de jouer
					
					if self.connexion.toure_du_joueur == True:
						# si c'est le cas

						if Envoyer.is_direction(ma_commande): # on verifie si c'est un deplacement que le joueur veut (n,s,e,o)
							#tous les deplacement se traite de la meme maniere inutile de traiter chaque commande separement
							
							self.connexion.envoie(commandes[ma_commande])
							
							# une action a etait faite cen'est plus le toure du joueur 
							with verrou:
								self.connexion.toure_du_joueur = False

							# on verifie si le joueur a a entrer le nombre de fois qu'il veut deplacer la piece (par defaut c'est 1)
							try:
								# on convertie l'entrer du joueur en entier puis on verifie que c'est bien superieur a '1' 
								# si c'est fait sans lever d'exeption on guarde le nombre sinon on mets '1' 
								n = int(a_envoyer[1:])
								assert n >= 1							
							except ValueError:
								n = 1
							except AssertionError:
								n = 1

							self.a_refaire["nombre"] = n-1 # le -1 est par ce que le mouvement a deja etait fait une fois juste plus haut
							self.a_refaire["direction"] = commandes[ma_commande]

						elif commandes[ma_commande] == "murer" or commandes[ma_commande] == "percer":
							# les commandes murer et percer ce traite de la meme manierre

							# l'utilisateur doit avoir entrer une direction a murer ou percer (n,o..)
							try:
								# si une exception est lever au court des 2 prochaine lignes c'est que soit:

								direction = a_envoyer[1]
								assert Envoyer.is_direction(direction)							
							except IndexError:
								# l'utilisateur n'a rien entrer donc on affiche un message d'erreur
								
								self.afficher("il vous faut selectionner la direction que vous voullez murer ou percer")						
							except AssertionError:
								# l'utilisateur a entrer quel que chose mais qui ne correspond pas a une direction
								# donc on affiche un message d'erreur

								self.afficher("il vous faut selectionner la direction que vous voullez murer ou percer")							
							else:
								# si y'a pas d'exeption la commande vas etre envoyer
								self.connexion.envoie(commandes[ma_commande])
								self.connexion.envoie(commandes[direction])
								
								# et bien sur on arrete le toure du joueur
								with verrou:
									self.connexion.toure_du_joueur = False
					
					else:
						self.afficher("ce n'est pas encore votre tour")


	def analyse(self):
		
		with verrou:

			if self.connexion.action_rater == True:
				
				self.connexion.action_rater = False
				self.a_refaire["nombre"] = 0
				self.a_refaire["direction"] = "aucune"

	
	def afficher(self, msg):
		with verrou:
			print(msg)


	def is_direction(direction):
		if commandes[direction] == "nord" or commandes[direction] == "ouest" or commandes[direction] == "est" or commandes[direction] == "sud":
			return True
		return False