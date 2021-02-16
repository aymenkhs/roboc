this project is small game I've made when learning python the principle is simple you controle it's a multiplayer game when you controle a player in a maze

#How to run it
1. you need to run the server for that just running the file "serveur_roboc.py"
2. you'll need to select one of the maps available (from the terminal)
3. run one ore more clients by running the file "client_roboc.py", there's virtually no limitation for the number o clients you can run
4. once you have enough client one of them have just to start the game by typing "c" in the terminal
5. now you can enjoy the game

#How do the game work

The board is made of Walls, doors and empty squares, the player can only move though the empty spaces and doors, the purpose of the game is to arrive at a "destination" (there can be multiple destination in a map). At each turn a player can either move or do one of the following:
* drill an adjacent wall => the wall become a door
* wall an adjacent door => the door become a wall

in the beginning of the game the server assign a random position on the board to each player and send to them a version of the board, then turn by turn the clients send a message representing on of the following actions:
* moving east, west, south or north
* drill the wall in one of direction above
* wall a door in one of direction above
* quitting the game
and once one of the players arrives at destination the game ends and the player win

#How The Project was build

##Communication between the server and the clients
we're using python standard library "socket" to send and receive messages, on the server side we're using the "select" library to listen to multiple clients, and on the clients we're using threads to listen to the server and the client on the terminal simultaneously.

##Server Side
the server communicate with the client through the "Serveur" class that uses "socket" and "select" libraries, The "Labyrinthe" class is responsible for all the game mechanics and the "Carte" class for reading the map of a maze from the "cartes" folder.

##Client Side
we have 2 threads running in the client side, a receiving thread that listen to the server continuously, and another that listen to the user commands and send the to the server, the both communicate with sever through the "Client" class that uses sockets.

##Tests
we've written units test for 2 classes, The "Labyrinthe" class responsible for all the game mechanics and the "Carte" class responsible for reading the map of a maze from "cartes" folder.
