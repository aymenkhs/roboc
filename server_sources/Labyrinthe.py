# -*-coding:Utf-8 -*

import random

from server_sources.obstacles import *
from server_sources.robot import Robot
from server_sources.exceptions import *

class Labyrinthe:
	""" classe representant un labyrinthe """

	def __init__(self , list_obstacles):
		self.robots = [] # une liste contenant les diff robots du jeux
		self._grille = {} # dictionnaire de coordoones (tuples) qui contient les differents obstacles du jeux
		for obstacle in list_obstacles:
			self._grille[obstacle.i, obstacle.j] = obstacle

		self.fin_partie = False
		self.limite_x , self.limite_y = self._limites() #les limites du labyrinthe en labyrinthe en largeur et longeur
	
	def __getitem__(self , index):
		"""pour simplifier l'utilisation de l'objet  """
		return self._grille[index]

	def __setitem__(self , index , val):
		"""pour simplifier l'utilisation de l'objet  """
		self._grille[index] = val

	def __contains__(self , index):
		"""pour simplifier l'utilisation de l'objet  """
		return index in self._grille

	def __delitem__(self , index):
		"""pour simplifier l'utilisation de l'objet  """
		del self._grille[index]

	def _limites(self):
		""" renvoie les limites (la taille) du labyrinthe en largeur et longueur """

		# on parcourt simplement le dictionnaire et on prend les coordonnes les plus grandes
		maxi = 0
		maxj = 0
		for key in self._grille:
			if maxi < key[0]:
				maxi = key[0]
			if maxj < key[1]:
				maxj = key[1]
		return (maxi, maxj)

	def cree_robot(self):
		"""methode charger de la generation de la postion du robot et de sa creation"""
		# tant que le robot n'est pas cree on refait...
		cree = False
		while not cree:
			# on genere une posotion aleatoire comprise entre 0 et les limites du labyrinthe
			i = random.randint(0 , self.limite_x)
			j = random.randint(0 , self.limite_y)
			# on verifie si on peut placer notre robot a cette position (abscence de mur , autre robot...)
			if self.placement_possible(i , j):
				# si c'est le cas (on peut le placer) on le cree et on met la variable cree a vrai histoire d'arreter la boucle
				self.robots.append(Robot(i,j))
				cree = True

	def _robot_a_la_position(self , i , j):
		""" methode qui test si il y a un robot a la position envoyer """
		for robot in self.robots:
			if (robot.i , robot.j) == (i ,j):
				return True
		return False
	

	def get_grille(self , joueur):
		"""retourner le labyrinthe sous forme de chaine pour l'envoyer aux client en fonction du joueur passer en parametre
			(il auras son robot en majiscule)
		"""
		grille = ""

		#on parcourt le labyrinthe de long en large et on se limite a constituer une chaine a partire des symbole donner dans la classe de chaque obstale 
		i = 0
		while i <= self.limite_x:
			j = 0
			while j <= self.limite_y:
				if self._robot_a_la_position(i ,j): #test la position des differrents robots
					if (i,j) == (self.robots[joueur].i , self.robots[joueur].j):
						# si il s'agit du client a qui on envoie la grille on lui mets le symbole_princ du robot
						# (X majiscule actuellement)
						grille += Robot.symbole_princ
					else:
						# sinon on mets le symbole_sec
						grille += Robot.symbole_sec						
				elif (i , j) in self:
					grille += self[i , j].symbole
				else:
					grille += " "

				j += 1
			grille += "\n"
			i += 1

		return grille


	def placement_possible(self , i , j):
		""" methode qui test si le robot peut etre placer a la case selectionner """

		if i <= self.limite_x and j <= self.limite_y and ((i,j) not in self or self[i,j].peut_traverser == True) and not self._robot_a_la_position(i,j):
			# on test dabord si notre deplacement est bien dans la grille
			# puis la cases ou on veut se deplacer doit soit etre vide ou avoir un obstacle qu'on peut traverser
			# et enfin on verifie qu'il y as pas de robot a cette position
			return True

		return False


	def deplacement(self , direction , num_robot):
		"""methode qui gere le deplacement du robot
		leve une exeption 'DeplacementImpossible' si on peut pas ce deplacer a la cases donner
		pour n'importe quel raison (il y a un obstacle infranchisable, un autre robot.....) """

		robot = self.robots[num_robot]
		i = robot.i 
		j = robot.j

		#on verifie la direction pour aller virtuelement a la case selectionner
		if direction.lower() == "ouest":
			j-=1
		elif direction.lower() == "est":
			j+=1
		elif direction.lower() == "nord":
			i-=1
		elif direction.lower() == "sud":
			i+=1
		else: #si la valleur envoyer est differentes c'est qu'il y as une erreur
			raise ValueError("error in direction value")

		# avant de deplacer on verifie juste que le deplacement est possible (pas de mur , autre robot...) sinon on aura une exeption de lever 
		if self.placement_possible(i , j):
			robot.i = i
			robot.j = j
			# et on verifie si le robot avec ce deplacement a ateint la sortie si c'est les cas on initialise l'attribut fin_partie
			if (robot.i , robot.j) in self and self[robot.i , robot.j].nom == "sortie":
				self.fin_partie = True
		else:
			raise DeplacementImpossible("impossible de se rendre a la case ({},{})".format(i,j))

	def murer(self , direction, num_robot):
		""" methode qui permet d'emmurer une porte 
		leve une exeption 'MurerImpossible' si il n'y as pas de porte a la cases donner ou si un robot est a cet position"""

		robot = self.robots[num_robot]
		i = robot.i 
		j = robot.j

		#on verifie la direction pour aller virtuelement a la case selectionner
		if direction.lower() == "ouest":
			j-=1
		elif direction.lower() == "est":
			j+=1
		elif direction.lower() == "nord":
			i-=1
		elif direction.lower() == "sud":
			i+=1
		else: #si la valleur envoyer est differentes c'est qu'il y as une erreur
			raise ValueError("error in direction value")

		# on verifie dabord que case n'est pas vide puis on verifie que la case est bien une porte
		# on veriifie ensuite qu'il n'y as pas de robot a cette position (vu que les robots peuvent franchir les porte)
		# avouer que ca serait bete d'avoir un robot coincer dans un mur
		# bref si une des conditions n'est pas remplit on leve une jolie exeption
		if (i,j) in self and self[i,j].nom == "porte":
			if not self._robot_a_la_position(i,j):
				del self[i,j]
				self[i,j] = Mur(i , j) 
			else: 
				raise MurerImpossible("impossible de murer la porte selectionner car il y as un autre robot a cette position ({},{})".format(i,j))
		else:
			raise MurerImpossible("il n'y a pas de porte a la case ({},{})".format(i,j))

	def percer(self , direction, num_robot):
		""" methode qui permet de percer une porte dans un mur 
		leve une exeption 'PercerImpossible' si il n'y as pas de mur a la cases donner"""

		robot = self.robots[num_robot] 
		i = robot.i 
		j = robot.j

		#on verifie la direction pour aller virtuelement a la case selectionner
		if direction.lower() == "ouest":
			j-=1
		elif direction.lower() == "est":
			j+=1
		elif direction.lower() == "nord":
			i-=1
		elif direction.lower() == "sud":
			i+=1
		else: #si la valleur envoyer est differentes c'est qu'il y as une erreur
			raise ValueError("error in direction value")

		# on verifie dabord que case n'est pas vide (histoire de ne pas avoir une erreur) puis
		# on verifie que la case est bien un mur  
		if (i,j) in self and self[i,j].nom == "mur":
			# si on arrive la alors la cases est un mur donc on supprime l'objet et on cree une porte a la place		
			del self[i,j]
			self[i,j] = Porte(i , j) 
		else:
			# la case n'est pas un mur (ou n'existe pas) on leve donc une exeption (ouais falait pas jouer avec ca)
			raise PercerImpossible("il n'y a pas de mur a la case ({},{})".format(i,j))
