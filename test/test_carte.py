# -*-coding:Utf-8 -*

""" module comportant des tests unittaire sur la creation d'une carte (la classe de transition entre un fichier et un labyrinthe) """

import unittest
import random
import os

from server_sources.carte import Carte

class CreationCarteTest(unittest.TestCase):
	""" classe contenant 2 test un sur la creation d'une carte et l'autre sur le dictionnaire d'obstacles"""

	def setUp(self):
		# on initialise notre carte en selectionnant aleatoirement une carte parmis celle disponible dans le dossier 'carte'
		self.cartes_existantes = []
		for nom_fichier in os.listdir("cartes"):
			if nom_fichier.endswith(".txt"):
				self.cartes_existantes.append(nom_fichier[:len(nom_fichier) - 4])

		self.ma_carte = Carte(random.choice(self.cartes_existantes))

	def test_creation_carte(self):
		""" test que la chaine contient bien que les caracteres prix en charge"""
		for caractere in self.ma_carte.chaine:
			self.assertIn(caractere , ["O" , "U" , "." , " " , "\n"])

	def test_creation_obstacles(self):
		""" test la creation d'obstacles """
		list_obstacles = self.ma_carte.creation_obstacles()
		
		# pour chaque caractere du fichier on verifie les obstacles un par un 
		i = 0
		for caractere in self.ma_carte.chaine:
			if caractere != '\n' and caractere != ' ':
				obs = list_obstacles[i]
				i+=1
				self.assertEqual(obs.symbole , caractere)

		# la methode doit lever une exception de type ValueError si un caractere du fichier n'est pas reconnue
		# (n'est pas un obstacle ni un espace ou un saut a la ligne)
		# on doit donc tester si cette exception est bien lever
		autre_carte = Carte(random.choice(self.cartes_existantes))
		autre_carte.chaine += "Z"
		self.assertRaises(ValueError , autre_carte.creation_obstacles)

class FichierTest(unittest.TestCase):
	""" classe qui contient un test qui verifient la constitution des fichiers 
		'pas de caractere non prix en charge' """

	def test_fichier(self):
		""" test de la constitution de tous les fichiers prensents dans 'cartes' """
		
		#on parcourt l'integralite des fichiers
		for nom_fichier in os.listdir("cartes"):
			# on ouvre et lit le fichier dans la variable chaine	
			chemin = os.path.join("cartes", nom_fichier)
			with open(chemin , "r") as fichier:
				chaine = fichier.read()

			# et enfin on verifie un par un les caractere du fichier
			for caractere in chaine:
				self.assertIn(caractere , ["O" , "U" , "." , " " , "\n"])


if __name__ == "__main__":
	unittest.main()