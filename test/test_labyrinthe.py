# -*-coding:Utf-8 -*

""" module comportant des tests unittaire sur les fonctionalite de la classe labyrinthe:

	- constitution d'un labyrinthe et creation de robot
	- convertion du labyrinthe en chaine
	- deplacement et autres actions (percer...) """

import unittest
import random

from server_sources.Labyrinthe import Labyrinthe
from server_sources.carte import Carte
from server_sources.robot import Robot
from server_sources.exceptions import *

class LabyrintheTest(unittest.TestCase):
	""" on test les fonctionalités du labyrinthe avec la carte facile"""
	def setUp(self):
		self.ma_carte = Carte("facile")
		self.mon_lab = Labyrinthe(self.ma_carte.creation_obstacles())

	def test_constitution(self):
		""" test que le labyrinthe est bien construit apres avoir appeler le constructeur du labyrinthe"""
		self.assertEqual(self.mon_lab.limite_x , 10)
		self.assertEqual(self.mon_lab.limite_y , 9)

		i = 0
		j = 0
		# on test les caracteres de la chaine (cree a partir du fichier) un par un et on verifie si il correspond bien au caractere dans la grille du labyrinthe  
		for caractere in self.ma_carte.chaine:
			if caractere == "\n":
				i += 1
				j = 0
				continue
			elif caractere == " ":
				pass
			else:
				self.assertEqual(caractere , self.mon_lab[i ,j].symbole)
			j+=1

	def test_creation_robot(self):
		""" test de la creation du robot :
			- qu'il est bien cree dans les limites du labyrinthe
			- qu'il n'est pas cree sur un obstacle qu'on ne peut pas traverser
			- qu'il n'est pas cree sur la sortie
		"""
		self.mon_lab.cree_robot()
		robot = self.mon_lab.robots[0]
		self.assertLessEqual(robot.i , self.mon_lab.limite_x)
		self.assertLessEqual(robot.j , self.mon_lab.limite_y)
		self.assertTrue( ((robot.i,robot.j) not in self.mon_lab) or (self.mon_lab[robot.i,robot.j].peut_traverser == True) and not (self.mon_lab[robot.i,robot.j].nom == "sortie"))

	def test_deplacement(self):
		""" test du deplacement du robot :
			- les cas ou le deplacement est impossible
			- que les coordones du robot change bien comme voulue apres un deplacement
			- que la partie se termine (l'attribut fin_partie est a True) apres qu'un robot arrive a une sortie 
		"""
		self.mon_lab.robots.append(Robot(3 , 8))
		
		# a l'est de la case (3,8) il y as un mur donc la methode doit levez une exeption
		self.assertRaises(DeplacementImpossible , self.mon_lab.deplacement , "est" , 0)
		# la methode doit levez une exeption si on entre une valleur eroné (veste dans notre cas)
		self.assertRaises(ValueError , self.mon_lab.deplacement , "veste" , 0)

		# on test que les coordoones du robot change bien comme on le souhaite apres un deplacement
		self.mon_lab.deplacement("nord" , 0)
		self.assertEqual(self.mon_lab.robots[0].i , 2)
		self.assertEqual(self.mon_lab.robots[0].j , 8)

		self.mon_lab.deplacement("ouest" , 0)
		self.assertEqual(self.mon_lab.robots[0].i , 2)
		self.assertEqual(self.mon_lab.robots[0].j , 7)

		self.mon_lab.deplacement("sud" , 0)
		self.assertEqual(self.mon_lab.robots[0].i , 3)
		self.assertEqual(self.mon_lab.robots[0].j , 7)

		# la methode doit levez une exeption vu qu'on ne peut pas se deplacer a une case ou il y as un robot
		self.mon_lab.robots.append(Robot(3 , 8))
		self.assertRaises(DeplacementImpossible , self.mon_lab.deplacement , "est" , 0)

		# on test l'attribut fin_partie si un robot arrive a une sortie
		self.mon_lab.robots.append(Robot(5 , 8))
		self.mon_lab.deplacement ("est" , 2)
		self.assertTrue(self.mon_lab.fin_partie)

	def test_percer(self):
		""" test de la methode percer :
			- les cas ou le percage est impossible
			- que la case a percer change bien comme voulue si c'est possible 
		"""
		self.mon_lab.robots.append(Robot(3 , 5))

		# la case a percer ne contient pas de mur donc on devrait avoir une exeption de lever
		self.assertRaises(PercerImpossible , self.mon_lab.percer , "est" , 0)
		# la methode doit levez une exeption si on entre une valleur eroné (teste dans notre cas)
		self.assertRaises(ValueError , self.mon_lab.percer , "teste" , 0)

		# apres avoir percer un mur la case en question devrait contenir une porte
		self.mon_lab.percer("ouest" , 0)
		self.assertEqual(self.mon_lab[3,4].nom , "porte")

	def test_murer(self):
		""" """
		self.mon_lab.robots.append(Robot(3 , 8))

		# la case a murer ne contient pas de porte donc on devrait avoir une exeption de lever		
		self.assertRaises(MurerImpossible , self.mon_lab.murer , "est" , 0)
		# la methode doit levez une exeption si on entre une valleur eroné (rf dans notre cas)
		self.assertRaises(ValueError , self.mon_lab.murer , "rf" , 0)

		# apres avoir murer une porte la case en question devrait contenir un mur
		self.mon_lab.murer("sud" , 0)
		self.assertEqual(self.mon_lab[4,8].nom , "mur")

		# dans le cas ou il y as un robot a la case qu'on veut murer une exeption doit etre lever
		self.mon_lab.robots.append(Robot(6 , 8))
		self.mon_lab.robots.append(Robot(5 , 8))
		self.assertRaises(MurerImpossible , self.mon_lab.murer , "sud" , 2)

	def test_grille(self):
		""" test de la methode get_grille """
		self.mon_lab.robots.append(Robot(3 , 8))
		self.mon_lab.robots.append(Robot(6 , 8))

		# apres avoir appeler la methode dans les condition actuelles on devrait avoir comme retour la chaine contenue dans 'carte' 
		chaine = self.mon_lab.get_grille(0)
		carte = "OOOOOOOOOO\nO O    O O\nO . OO   O\nO O O   XO\nO OOOO O.O\nO O O    U\nO OOOOOOxO\nO O      O\nO O OOOOOO\nO . O    O\nOOOOOOOOOO\n"
		self.assertEqual(chaine , carte)

if __name__ == "__main__":
	unittest.main()