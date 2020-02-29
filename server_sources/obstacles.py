# -*-coding:Utf-8 -*

""" classe qui definit la classe obstacle et les differents obstacles deriver de cette classe """

class Obstacle:
	""" classe qui definit des obstacles, destiner a etre la classe mere des differents obstacles du jeux"""
	nom = "obstacle"

	def __init__(self , i , j):
		self.i = i
		self.j = j

	def __repr__(self):
		return "<Obstacle:{nom}> x = {i}, y = {j}) ".format(nom = self.nom , i = self.i , j = self.j)

	def __str__(self):
		return "{nom} ({x}.{y})".format(nom=self.nom, x=self.x, y=self.y)


class Mur(Obstacle):
	""" classe qui defifnit un mur heriter de Obstacle"""

	nom = "mur"
	symbole = "O"
	peut_traverser = False


class Porte(Obstacle):
	""" classe qui defifnit une porte heriter de Obstacle"""

	nom = "porte"
	symbole = "."
	peut_traverser = True


class Sortie(Obstacle):
	""" classe qui defifnit la sortie heriter de Obstacle"""

	nom = "sortie"
	symbole = "U"
	peut_traverser = True


obstacles = {
	"O" : Mur,
	"." : Porte,
	"U" : Sortie
}