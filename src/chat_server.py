#!/usr/bin/env python3
"""Script Python per la realizzazione di un Server multithread
per connessioni CHAT asincrone.
Corso di Programmazione di Reti - Università di Bologna"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import domanda as d
import giocatore as g
import json
import os 
import random as r


""" La funzione che segue accetta le connessioni  dei client in entrata."""
def accetta_connessioni_in_entrata():
    while not startGame:
        client, client_address = SERVER.accept()
        print("%s:%s si è collegato." % client_address)
        #al client che si connette per la prima volta fornisce alcune indicazioni di utilizzo
        client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
        # ci serviamo di un dizionario per registrare i client
        indirizzi[client] = client_address
        #diamo inizio all'attività del Thread - uno per ciascun client
        Thread(target=gestice_client, args=(client,)).start()
        

"""La funzione seguente gestisce la connessione di un singolo client."""
def gestice_client(client):  # Prende il socket del client come argomento della funzione.
    #nome = client.recv(BUFSIZ).decode("utf8")
    giocatorePresente = True
    while giocatorePresente:
        giocatorePresente = False
        nome = client.recv(BUFSIZ).decode("utf8")
        for p in players:
            if(p.nome == nome):
                client.send(bytes('Nome già in uso! Scrivere un altro nome.', 'utf8'))
                giocatorePresente = True
                break
    
    #aggiorna il dizionario clients creato all'inizio
    clients[client] = nome
    player = g.Giocatore(nome, ruoli[r.randrange(6)], 0)
    players.append(player)
    
    #da il benvenuto al client e gli indica come fare per uscire dalla chat quando ha terminato
    client.send(bytes('{benvenuto}', 'utf8'))
    benvenuto = 'Benvenuto %s! Il tuo ruolo è %s.\n' % (nome, player.ruolo)
    client.send(bytes(benvenuto, "utf8"))
    #client.send(bytes('Se vuoi lasciare la Chat, scrivi {quit}.', "utf8"))
    client.send(bytes('Quando sei pronto a giocare scrivi {start}.', "utf8"))
    msg = "%s si è unito alla chat!" % nome
    #messaggio in broadcast con cui vengono avvisati tutti i client connessi che l'utente x è entrato
    broadcast(bytes(msg, "utf8"))
    
    print("players:", len(clients))
    
#si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
    domanda = None    
    while True:
        msg = client.recv(BUFSIZ)
        if domanda != None:
            if bytes(domanda.risposta, "utf8").lower() == msg.lower():
                client.send(bytes("Risposta esatta!", "utf8"))
                player.punteggio = player.punteggio + 1
            else:
                client.send(bytes("Risposta sbagliata!", "utf8"))
                player.punteggio = player.punteggio - 1
            client.send(bytes("Adesso hai " + str(player.punteggio) + (" punti." if player.punteggio != 1 else " punto."), "utf8"))
            domanda = None

            continue
        if msg == bytes("{start}", "utf8"):
            global ready
            ready = ready + 1
            print("ready:", ready)
            broadcast(bytes("%s è pronto a giocare . . .\n" % nome, "utf8"))
            if(len(clients) > 1 and ready == len(clients)):
                global startGame
                startGame = True
                broadcast(bytes("INIZIO GIOCO!", "utf8"))
        elif msg == bytes("{quit}", "utf8"):
            broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf8"))
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            break
        elif msg == bytes("{question}", "utf8") :
            domanda = domande[r.randrange(len(domande))]
            client.send(bytes("{question}", "utf8"))
            client.send(bytes(domanda.domanda, "utf8"))
        else:
            broadcast(msg, nome + ": ")
            
            

""" La funzione, che segue, invia un messaggio in broadcast a tutti i client."""
def broadcast(msg, prefisso=""):  # il prefisso è usato per l'identificazione del nome.
    for utente in clients:
        utente.send(bytes(prefisso, "utf8") + msg)

        
clients = {}
indirizzi = {}
startGame = False
ready = 0
players = []
ruoli = ["atleta","artista","geografo",
         "attore","scienziato","storico"]
domande = []
with open(os.getcwd() + '\\domande.json') as f:
    data = json.load(f)
for valore in data:
    domande.append(d.Domanda(valore['materia'], valore['domanda'], valore['risposta']));

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
