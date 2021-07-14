#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import question as q
import player as p
import json
import os 
import random as r

""" La funzione che segue accetta le connessioni  dei client in entrata."""
def accetta_connessioni_in_entrata():
    while not startGame:
        if startGame:
            break
        client, client_address = SERVER.accept()
        print("%s:%s si è collegato." % client_address)
        client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
        indirizzi[client] = client_address
        Thread(target=gestice_client, args=(client,)).start()

"""La funzione seguente gestisce la connessione di un singolo client."""
def gestice_client(client):  
    playerPresent = True
    while playerPresent:
        playerPresent = False
        name = client.recv(BUFSIZ).decode("utf8")
        for cur in players:
            if(cur.name == name):
                client.send(bytes('Nome già in uso! Scrivere un altro nome.', 'utf8'))
                playerPresent = True
                break
    
    clients[client] = name
    player = p.Player(name, roles[r.randrange(6)], 0)
    players.append(player)
    
    client.send(bytes('{welcome}', 'utf8'))
    client.send(bytes('Benvenuto %s! Il tuo ruolo è %s.\n' % (name, player.role), "utf8"))
    client.send(bytes('Per iniziare il gioco clicca sul pulsante Ready.\n', "utf8"))
    broadcast(bytes("%s si è unito alla chat!" % name, "utf8"))
    
    #controlli sul msg arrivato al server
    question = None    
    while True:
        msg = client.recv(BUFSIZ)
        if question != None:
            questions.remove(question)
            score_modifier = 2 if dictionary.get(player.role) == question.subject else 1
            if bytes(question.answer, "utf8").lower() == msg.lower():
                client.send(bytes("Risposta esatta!", "utf8"))
                player.score += score_modifier
            else:
                client.send(bytes("Risposta sbagliata!", "utf8"))
                if player.score > 0:
                    player.score -= score_modifier
            client.send(bytes("Adesso hai " + str(player.score) + (" punti." if player.score != 1 else " punto."), "utf8"))
            question = None
            #una volta entraton in questa if devo saltare tutto il resto del codice
            continue
        if msg == bytes("{start}", "utf8"):
            global ready
            ready = ready + 1
            print("ready:", ready)
            broadcast(bytes("%s è pronto a giocare . . ." % name, "utf8"))
            if(len(clients) > 1 and ready == len(clients)):
                global startGame
                startGame = True
                broadcast(bytes("{startgame}", "utf8"))
        elif msg == bytes("{quit}", "utf8"):
            players.remove(player)
            clients.pop(client)
            broadcast(bytes("%s ha abbandonato la Chat." % name, "utf8"))
            break
        elif msg == bytes("{question}", "utf8") :
            question = questions[r.randrange(len(questions))]
            client.send(bytes("{question}", "utf8"))
            client.send(bytes(question.question, "utf8"))
        elif msg == bytes("{gameover}", "utf8"):
            winner = getWinner()
            client.send(bytes("Tempo scaduto! Il vincitore è %s (punti = %d)!" % (winner.name, winner.score), "utf8"))
        else:
            broadcast(msg, name + ": ")
            

""" La funzione, che segue, invia un messaggio in broadcast a tutti i client."""
def broadcast(msg, prefix=""): 
    for u in clients:
        u.send(bytes(prefix, "utf8") + msg)
        
""" La funzione, che segue, ricava il giocatore con il punteggio più alto tra quelli correnti."""
def getWinner():
    winner = players[0]
    for cur in players:
        if cur.score > winner.score:
            winner = cur
    return winner

#variabili globali legate ai players
clients = {}

indirizzi = {}

startGame = False

ready = 0

players = []

roles = ["atleta","artista","geografo",
         "attore","scienziato","storico"]

dictionary = {"atleta": "sport",
              "artista": "arte",
              "geografo": "geografia",
              "attore": "spettacolo",
              "scienziato": "scienze",
              "storico": "storia"}

#variabili globali legate alla domanda
questions = []

with open(os.getcwd() + '\\questions.json') as f:
    data = json.load(f)

for value in data:
    questions.append(q.Question(value['materia'], value['domanda'], value['risposta']));

#variabili globali legate al server
HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accetta_connessioni_in_entrata)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
