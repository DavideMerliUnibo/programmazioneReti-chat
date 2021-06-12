#!/usr/bin/env python3
"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
import sys

"""La funzione che segue ha il compito di gestire la ricezione dei messaggi."""
def receive():
    while True:
        try:
            print("Inizio receive")
            #quando viene chiamata la funzione receive, si mette in ascolto dei messaggi che
            #arrivano sul socket
            my_msg = client_socket.recv(BUFSIZ).decode("utf8")
            #visualizziamo l'elenco dei messaggi sullo schermo
            #e facciamo in modo che il cursore sia visibile al termine degli stessi
            text['state'] = 'normal'
            text.insert(tk.END, my_msg)
            text.insert(tk.END, '\n')
            text['state'] = 'disabled'
            # Nel caso di errore e' probabile che il client abbia abbandonato la chat.
            print("Fine receive")
        except OSError:  
            break

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
def on_closing(event=None):
    msg.set("{quit}")
    send()

#finestra = tkt.Tk()
#finestra.title("Chatgame")

#creiamo il Frame per contenere i messaggi
#messages_frame = tkt.Frame(finestra)
#creiamo una variabile di tipo stringa per i messaggi da inviare.
#my_msg = tkt.StringVar()
#indichiamo all'utente dove deve scrivere i suoi messaggi
#my_msg.set("Scrivi qui i tuoi messaggi.")
#creiamo una scrollbar per navigare tra i messaggi precedenti.
#scrollbar = tkt.Scrollbar(messages_frame)

# La parte seguente contiene i messaggi.
#msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
#scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
#msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
#msg_list.pack()
#messages_frame.pack()

#Creiamo il campo di input e lo associamo alla variabile stringa
#entry_field = tkt.Entry(finestra, textvariable=my_msg)
# leghiamo la funzione send al tasto Return
#entry_field.bind("<Return>", send)

#entry_field.pack()
#creiamo il tasto invio e lo associamo alla funzione send
#send_button = tkt.Button(finestra, text="Invio", command=send)
#integriamo il tasto nel pacchetto
#send_button.pack()

#finestra.protocol("WM_DELETE_WINDOW", on_closing)


window = tk.Tk()
window.title("Chatgame")

text = tk.Text(height = 20, width = 50)
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
window.protocol("WM_DELETE_WINDOW", on_closing)

#----Connessione al Server----
HOST = input('Inserire il Server host: ')
if not HOST:
    HOST = '127.0.0.1'
PORT = input('Inserire la porta del server host: ')
if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
# Avvia l'esecuzione della Finestra Chat.
tk.mainloop()
