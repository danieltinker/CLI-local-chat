import socket
import threading
import time
from pytimedinput import timedInput


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg): #handle a client SEND MSG
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    #print(client.recv(2048).decode(FORMAT)) --- replaced with incoming() 


def incoming():   #thread - handle realtime incoming messages
    communicate =True
    try:
        while communicate:
            msgIN = client.recv(HEADER).decode(FORMAT)
            
            if msgIN==DISCONNECT_MESSAGE:
                communicate=False
                print("[HOST WARNING]SERVER DISCONNECTED.\n") #press ENTER to leave the program
                continue
            
            if msgIN:
                print(msgIN)
    except OSError:
        print("I\O was stopped\n.")#press ENTER to leave the program
        
                
try:
    incomingMsg = threading.Thread(target=incoming, args=())
    incomingMsg.start()
    timedOut=True
    while timedOut:
        pipeUsername,timedOut = timedInput("please enter username: ",15)
         #                          ^ pipeUsername= input(">") less reactive cleaner code and screen
    if incomingMsg.is_alive():
        send(pipeUsername)
        
    while incomingMsg.is_alive():
        time.sleep(0.05)
        pipeMsg,timedOut = timedInput("> ",15)
        #                           ^ pipeMsg= input(">") less reactive cleaner code and screen
        if incomingMsg.is_alive() and (not timedOut):
            send(pipeMsg)

except KeyboardInterrupt:
    print("Client has Left with CNTRL+C\n")

    
finally:
    if incomingMsg.is_alive():
        send(DISCONNECT_MESSAGE) 
    client.close()
    print("GOODBYE!")