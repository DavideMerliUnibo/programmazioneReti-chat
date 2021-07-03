#!/usr/bin/env python3
"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter."""
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
            #quando viene chiamata la funzione receive, si mette in ascolto dei messaggi che
            #arrivano sul socket
            my_msg = client_socket.recv(BUFSIZ).decode("utf8")
            if my_msg == "{benvenuto}":
                btn_ready['state'] = 'normal'
            elif my_msg == "INIZIO GIOCO!":
                #inizio timer
                time = timer.Timer()
                timerLabel = tk.Label(text = time.converti(time.contatore))
                timerLabel.pack()
                timerThread = Thread(target = lambda: aggiornaTimer(timerLabel, time))
                timerThread.start()
                #creazione pulsanti e area di testo delle domande
                questionText.pack()
                answerField.pack()
                btn_answer.pack()
                chooseWrongButton()
            #e facciamo in modo che il cursore sia visibile al termine degli stessi
            elif my_msg == "{question}":
                chooseWrongButton()
            elif my_msg == "Risposta esatta!":
                messagebox.showinfo("Esito","Esattooo!!!")
                questionText['state'] = 'normal'
                questionText.delete('1.0', tk.END)
                questionText['state'] = 'disabled'
            elif my_msg =="Risposta sbagliata!":
                messagebox.showinfo("Esito","Sbagliato!!!")
                questionText['state'] = 'normal'
                questionText.delete('1.0', tk.END)
                questionText['state'] = 'disabled'
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
            # Nel caso di errore e' probabile che il client abbia abbandonato la chat.
        except OSError:  
            break

def question(gameFrame):
    global selectChat 
    selectChat = False
    answerField['state'] = 'normal'
    entryField['state'] = 'disabled'
    msg.set("{question}")
    send()
    gameFrame.destroy()
    
"""La funzione che segue gestisce l'invio dei messaggi."""
def send(event = None):
    my_msg = msg.get()
    msg.set("")
    # invia il messaggio sul socket
    client_socket.send(bytes(my_msg, "utf8"))
    if my_msg == "{quit}":
        client_socket.close()
        window.close()
        
def ready():
    msg.set("{start}")
    send()
    btn_ready['state'] = 'disabled'
    
def close(event = None):
    window.destroy()
    sys.exit()

"""La funzione che segue viene invocata quando viene chiusa la finestra della chat."""
def on_closing(event = None):
    msg.set("{quit}")
    send()
    window.destroy()
    
    
def sendAnswer():
    if not answerField.get():
        messagebox.showwarning("Attenzione","Inserire risposta!")
        return
    global selectChat
    selectChat = True
    entryField['state'] = 'normal'
    answerField['state']='disabled'
    questionText['state'] = 'normal'
    my_answer = answer.get()
    client_socket.send(bytes(my_answer, "utf8"))
    answer.set('')
    questionText['state'] = 'disabled'
    
def chooseWrongButton():
    gameFrame = tk.Frame(master = window)
    btn_A = tk.Button(master = gameFrame, text = "A")
    btn_B = tk.Button(master = gameFrame, text = "B")
    btn_C = tk.Button(master = gameFrame, text = "C")
    t = random.randint(1,3)
    if t==1:
        btn_A.config(command = close)
        btn_B.config(command = lambda: question(gameFrame))
        btn_C.config(command = lambda: question(gameFrame))
    elif t==2:  
        btn_B.config(command = close)
        btn_A.config(command = lambda: question(gameFrame))
        btn_C.config(command = lambda: question(gameFrame))
    else:
        btn_C.config(command = close)
        btn_A.config(command = lambda: question(gameFrame))
        btn_B.config(command = lambda: question(gameFrame))
    btn_A.pack(side = tk.LEFT)
    btn_B.pack(side = tk.LEFT)           
    btn_C.pack(side = tk.LEFT)
    gameFrame.pack()
    
def aggiornaTimer(timerLabel, time):
    while time.contatore > 0:
        timerLabel.config(text = time.countdown())
    client_socket.send(bytes("{gameover}", "utf8"))

selectChat = True
window = tk.Tk()
window.title("Chatgame")

text = tk.Text(height = 15, width = 50)
text['state'] = 'disabled'
text.pack()

label = tk.Label(text = "Write your messages here:")
label.pack()

msg = tk.StringVar()
entryField = tk.Entry(width = 25, textvariable = msg)
entryField.pack()

frame = tk.Frame(master = window)
btn_send = tk.Button(master = frame, text = "Send", command = send)
btn_ready = tk.Button(master = frame, text = "Ready", command = ready)
btn_quit = tk.Button(master = frame, text = "Quit", command = close)
btn_send.pack(side = tk.LEFT)
btn_ready.pack(side = tk.LEFT)
btn_quit.pack(side = tk.LEFT)
btn_ready['state'] = 'disabled'
frame.pack()

window.bind('<Return>', send)
window.bind('<Escape>', close)
window.protocol("WM_DELETE_WINDOW", close)






#ASPE
questionText = tk.Text(height = 5, width = 50)
questionText['state'] = 'disabled'
answer = tk.StringVar()
answerField = tk.Entry(width = 25, textvariable = answer)
btn_answer = tk.Button(text = 'Answer', command = sendAnswer)
#OK









#----Connessione al Server----
#HOST = input('Inserire il Server host: ')
#if not HOST:
HOST = '127.0.0.1'
#PORT = input('Inserire la porta del server host: ')
#if not PORT:
PORT = 53000
#else:
    #PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
# Avvia l'esecuzione della Finestra Chat.
tk.mainloop()