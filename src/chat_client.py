#!/usr/bin/env python3
"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
import sys
import random

"""La funzione che segue ha il compito di gestire la ricezione dei messaggi."""
def receive():
    while True:
        try:
            #quando viene chiamata la funzione receive, si mette in ascolto dei messaggi che
            #arrivano sul socket
            my_msg = client_socket.recv(BUFSIZ).decode("utf8")
            if my_msg == "INIZIO GIOCO!":
                questionText.pack()
                answerField.pack()
                btn_answer.pack()
<<<<<<< HEAD
                t=1
                #t=random.randint(1,3)
=======
                t = random.randint(1,3)
>>>>>>> 1bf92132cd1cc136a68f99e23ad36493f4430e26
                gameFrame= tk.Frame(master = window)
                if t==1:
                    btn_A = tk.Button(master = gameFrame, text = "A", command = close)
                    btn_B = tk.Button(master = gameFrame, text = "B", command = question)
                    btn_C = tk.Button(master = gameFrame, text = "C", command = question)
                elif t==2:  
                    btn_B = tk.Button(master = gameFrame, text = "B", command = close)
                    btn_A = tk.Button(master = gameFrame, text = "A", command = question)
                    btn_C = tk.Button(master = gameFrame, text = "C", command = question)
                else:
                     btn_C = tk.Button(master = gameFrame, text = "C", command = close)
                     btn_B = tk.Button(master = gameFrame, text = "B", command = question)
                     btn_A = tk.Button(master = gameFrame, text = "A", command = question)
              
                btn_A.pack(side = tk.LEFT)
                btn_B.pack(side = tk.LEFT)           
                btn_C.pack(side = tk.LEFT)
                gameFrame.pack()
            #e facciamo in modo che il cursore sia visibile al termine degli stessi
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

def question():
    global selectChat 
    selectChat = False
    entryField['state'] = 'disabled'
    msg.set("{question}")
    send()
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
    
def sendAnswer():
    global selectChat 
    selectChat = True
    entryField['state'] = 'normal'
    questionText['state'] = 'normal'
    my_answer = answer.get()
    client_socket.send(bytes(my_answer, "utf8"))
    answer.set('')
    questionText['state'] = 'disabled'

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
frame.pack()

window.bind('<Return>', send)
window.bind('<Escape>', close)
window.protocol("WM_DELETE_WINDOW", close)






#ASPE
questionText = tk.Text(height = 3, width = 50)
questionText.insert(tk.END, "Domanda:\n")
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