# -*-coding:Utf-8 -*

class Robot:
	""" classe qui definit un robot qui vas avancer dans le labyrinthe"""

	symbole_princ = "X"
	symbole_sec = "x"

	def __init__(self , i , j):
		self.i = i
		self.j = j

		