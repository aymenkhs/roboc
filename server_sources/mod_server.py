# -*-coding:Utf-8 -*

""" ce module est composer defonctions dans le but d'alleger le code principal et de le rendre plus lisible"""

def choix(cartes_existantes):
	"""fonction qui retourne le choix de l'utilisateur des differantes cartes (j'en est fait une fonction juste pour simplifier le code principale) """
	
	# on affiche les differentes cartes disponibles 
	print("choisisser une des cartes")
	for i , nom_fichier in enumerate(cartes_existantes):
		print("{0}. {1}".format(i + 1 , nom_fichier))

	#l'utilisateur peut entrer un nombre (dans ce cas il sera traiter en fonction de son emplacement dans carts_existante) ou
	# carrement le nom du fichier dans ce cas on doit trouver sa position
	saisie = False
	while saisie == False:
		choix = input("...")
		if choix.isdigit(): # on verifie si l'utilisateur a entrer un nombre
			#si c'est le cas on verifie que le nombre entrer correspond bien a une carte 
			choix = int(choix)
			if choix <= len(cartes_existantes) and choix > 0:
				return cartes_existantes[choix - 1]
			else:
				print("vous avez entrer une valleur incorrecte")
		else:
			if cartes_existantes.count(choix) > 0:
				return choix
			else:
				print("vous avez entrer une valleur incorrecte")
