#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import sys
import random
import timer

"""La funzione che segue ha il compito di gestire la ricezione dei messaggi."""
def receive():
    while True:
        try:
            my_msg = client_socket.recv(BUFSIZ).decode("utf8")
            # controllo sul msg ricevuto
            if my_msg == "{welcome}":
                btn_ready['state'] = 'normal'
            elif my_msg == "{startgame}":
                time.timerLabel.pack()
                timerThread.start()
                gameFrame.pack()
                chooseWrongButton()
                text['state'] = 'normal'
                text.insert(tk.END, "INIZIO GIOCO!")
                text.insert(tk.END, '\n\n')
                text['state'] = 'disabled'
            elif my_msg == "{question}":
                chooseWrongButton()
            elif my_msg == "Risposta esatta!":
                messagebox.showinfo("Esito","Esattooo!!!")
                questionText['state'] = 'normal'
                questionText.delete('1.0', tk.END)
                questionText['state'] = 'disabled'
            elif my_msg == "Risposta sbagliata!":
                messagebox.showinfo("Esito","Sbagliato!!!")
                questionText['state'] = 'normal'
                questionText.delete('1.0', tk.END)
                questionText['state'] = 'disabled'
            elif my_msg == "{timestop}":
                time.running = False   
                time.timerLabel.destroy()
                gameFrame.destroy()
                text['state'] = 'normal'
                text.insert(tk.END, "Gli altri giocatori hanno abbandonato, hai vinto!!")
                text.insert(tk.END, '\n')
                text['state'] = 'disabled'
            elif my_msg == "{questionstop}":
                global selectChat
                entryField['state'] = 'normal'
                selectChat = True
            else:
                if selectChat:
                    text['state'] = 'normal'
                    text.insert(tk.END, my_msg)
                    text.insert(tk.END, '\n')
                    text['state'] = 'disabled'
                else :
                    questionText['state'] = 'normal'
                    questionText.insert(tk.END, my_msg)
                    questionText.insert(tk.END, '\n')
                    questionText['state'] = 'disabled'
        except OSError:  
            break

"""La funzione mette il client in attesa di una domanda."""
def question(buttonFrame):
    global selectChat 
    selectChat = False
    answerField['state'] = 'normal'
    entryField['state'] = 'disabled'
    btn_answer['state'] = 'normal'
    msg.set("{question}")
    send()
    buttonFrame.destroy()
    
"""La funzione che segue gestisce l'invio dei messaggi."""
def send(event = None):
    my_msg = msg.get()
    msg.set("")
    # invia il messaggio sul socket
    client_socket.send(bytes(my_msg, "utf8"))
    if my_msg == "{quit}":
        client_socket.close()
        window.close()
    
"""La funzione che segue segnala al server che il giocatore corrente è pronto."""
def ready():
    client_socket.send(bytes("{ready}", "utf8"))
    btn_ready['state'] = 'disabled'

"""La funzione che segue chuide la schermata del client"""
def close(event = None):
    client_socket.send(bytes("{quit}", "utf8"))
    time.running = False
    window.destroy()
    sys.exit()
    
"""La funzione che segue invia la risposta alla domanda al server."""
def sendAnswer():
    if not answerField.get():
        messagebox.showwarning("Attenzione","Inserire risposta!")
        return
    global selectChat
    selectChat = True
    entryField['state'] = 'normal'
    answerField['state']='disabled'
    btn_answer['state']='disabled'
    questionText['state'] = 'normal'
    my_answer = answer.get()
    client_socket.send(bytes(my_answer, "utf8"))
    answer.set('')
    questionText['state'] = 'disabled'

"""La funzione che segue crea tre pulsanti e ne sceglie uno sbagliato in modo randomico."""
def chooseWrongButton():
    buttonFrame = tk.Frame(master = gameFrame)
    btn_A = tk.Button(master = buttonFrame, text = "A")
    btn_B = tk.Button(master = buttonFrame, text = "B")
    btn_C = tk.Button(master = buttonFrame, text = "C")
    t = random.randint(1,3)
    if t==1:
        btn_A.config(command = close)
        btn_B.config(command = lambda: question(buttonFrame))
        btn_C.config(command = lambda: question(buttonFrame))
    elif t==2:  
        btn_B.config(command = close)
        btn_A.config(command = lambda: question(buttonFrame))
        btn_C.config(command = lambda: question(buttonFrame))
    else:
        btn_C.config(command = close)
        btn_A.config(command = lambda: question(buttonFrame))
        btn_B.config(command = lambda: question(buttonFrame))
    inner_label.pack()
    btn_A.pack(side = tk.LEFT)
    btn_B.pack(side = tk.LEFT)           
    btn_C.pack(side = tk.LEFT)
    inner_label.pack()
    buttonFrame.pack()
    
"""La funzione che segue tiene traccia del tempo di gioco"""
def aggiornaTimer(time):
    # inizia il conto alla rovescia
    time.countdown()
    # quando è finito il tempo distruggo la schermata di gioco e avviso il server
    client_socket.send(bytes("{gameover}", "utf8"))
    time.timerLabel.destroy()
    gameFrame.destroy()


selectChat = True

#creazione prima parte gui(chat)
window = tk.Tk()
window.title("Chatgame")
text = tk.Text(height = 15, width = 50)
text['state'] = 'disabled'
text.pack()
label = tk.Label(text = "Scrivi qui i tuoi messaggi:")
label.pack()
msg = tk.StringVar()
entryField = tk.Entry(width = 25, textvariable = msg)
entryField.pack()
frame = tk.Frame(master = window)
btn_send = tk.Button(master = frame, text = "Invia", command = send)
btn_ready = tk.Button(master = frame, text = "Pronto", command = ready)
btn_quit = tk.Button(master = frame, text = "Esci", command = close)
btn_send.pack(side = tk.LEFT)
btn_ready.pack(side = tk.LEFT)
btn_quit.pack(side = tk.LEFT)
btn_ready['state'] = 'disabled'
frame.pack()
window.bind('<Return>', send)
window.bind('<Escape>', close)
window.protocol("WM_DELETE_WINDOW", close)

#creazione seconda parte gui(gioco)
gameFrame = tk.Frame(master = window)
questionText = tk.Text(height = 5, width = 50, master = gameFrame)
questionText.pack()
questionText['state'] = 'disabled'
answer = tk.StringVar()
answerField = tk.Entry(width = 25, textvariable = answer, master = gameFrame)
answerField.pack()
btn_answer = tk.Button(text = 'Rispondi', command = sendAnswer, master = gameFrame)
btn_answer['state'] = 'disabled'
btn_answer.pack()
inner_label = tk.Label(master = gameFrame, text = "Scegli uno dei tre pulsanti per rispondere ad una domanda:")
inner_label.pack()

# Inizializzazione timer globale
time = timer.Timer()
timerThread = Thread(target = lambda: aggiornaTimer(time))

#----Connessione al Server----
HOST = '127.0.0.1'
PORT = 53000

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
receive_thread = Thread(target=receive)
receive_thread.start()
tk.mainloop()