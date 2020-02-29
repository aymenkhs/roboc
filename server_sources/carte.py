# -*-coding:Utf-8 -*
import os

from server_sources.obstacles import *

class Carte:
	""" classe de transition entre le fichier est le labyrinthe """

	def __init__(self , carte_choisit):
		self.nom = carte_choisit
		self.chaine = "" 
		self._lire_fichier()
	
	def _lire_fichier(self):
		""" methode qui se charge de la lecture du fichier et qui retourne le contenu du fichier sous forme de chaine"""
		chemin = os.path.join("cartes", self.nom + ".txt")
		with open(chemin , "r") as fichier:
			self.chaine = fichier.read()

	def creation_obstacles(self):
		""" methode qui vas transformer le contenue du fichier en une liste d'obstacle qui vas servir cree le labyrinthe """
		j = 0
		i = 0
		list_obstacles = []

		# on parcourt la chaine que contenait le fichier caractere par caractere
		# les obstacles sont des objets qui prennent la ligne et la colone dans laquel ils se trouvent comme parametres
		# i represente les ligne et j les colones

		for caractere in self.chaine:
			# si le caractere est un saut a la ligne on saute une ligne et on remets les colones a 0 et on continue (pour contourner le 'j+=1')
			if caractere == "\n":
				j = 0
				i+=1
				continue
			elif caractere in obstacles: # si le caractere est dans le dict 'obstacles' on cree un objet de cet obstacle
				
				# on utilise directement la classe du dictionnaire 'obstacles' qui a comme clee le caractere donne
				# (je vous renvoie vers la variable 'obstacles' a la fin du module obstacles si vous voyer pas dequoi je parle)
				classe_obstacle = obstacles[caractere]
				list_obstacles.append(classe_obstacle(i , j))
			elif caractere == " ": # si le caractere est un espace on ne fait rien
				pass
			else:
				# on leve une exeption si le caractere n'est ni un espace ou un saut a la ligne ni un obstacle connue 
				raise ValueError("le caractere a la position ({},{}) dans la carte selectionner <{}> n'est pas prix en charge".format(i,j,self.nom))
			j+=1
		return list_obstacles
