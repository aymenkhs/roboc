# -*-coding:Utf-8 -*

from client_sources import class_client
from client_sources import thread_envoyer , thread_recevoir

connexion = class_client.Client()
connexion.connexion()

print("connexion etablie avec ({} : {})\n".format(connexion.host , connexion.port))
print("bienvenue dans roboc, un jeu de labyrinthe au toure par toure ou vous controller un robot en multijoueur\n")

print(118 * "-" + "\n")

print("LES OBSTACLES")
print("les obstacles sont representer par des symbole dont voici la liste exhaustive")
print("mur : O \tporte : .\t sortie : U")
print("robot du joueur : X\t robot enemie : x\n")

print(118 * "-" + "\n")

print("LES COMMANDES")
print("vous controller le robot avec differntes commandes:\n")
print("*'c' pour commancer la partie et metre fin a l'attente d'autre joueur\n")
print("*'n' , 'o' , 's' , 'e' pour vous deplacer dans une des direction")
print("  'n' pour nord\n  'o' pour ouest\n  's' pour sud\n  'e' pour est")
print("  une direction peut etre suivie d'un nombre qui representera le nombre case qu'on veut parcourir (ex : n3)")
print("  par contre le deplacement se fait une seul fois par toure (si on entre n3 on se deplace vers le nord durant 3 toure)\n")
print("*'p' pour percer une porte dans un mur (doit etre suivie de la direction du mur a percer ex: po)")
print("*'m' pour murer une porte (doit etre suivie de la direction de la porte a murer ex: mn)\n")
print("*appuyer a tous moment sur 'q' pour abondonner et quiter la partie\n")

print(118 * "-" + "\n")

print("ATTENTE D'AUTRE JOUEURS\n")

a = thread_envoyer.Envoyer(connexion)
b = thread_recevoir.Recevoir(connexion)

a.start()
b.start()

a.join()
b.join()

connexion.deconnexion()