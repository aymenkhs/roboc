# -*-coding:Utf-8 -*

""" classe qui definit plusieurs exeption"""

class DeplacementImpossible(Exception):
	""" class definissant une exeption lever si le deplacement est impossible """

	def __init__(self , message):
		self.message = message

	def __str__(self):
		return self.message

class MurerImpossible(Exception):
	""" class definissant une exeption lever si le deplacement est impossible """

	def __init__(self , message):
		self.message = message

	def __str__(self):
		return self.message


class PercerImpossible(Exception):
	""" class definissant une exeption lever si le deplacement est impossible """

	def __init__(self , message):
		self.message = message

	def __str__(self):
		return self.message