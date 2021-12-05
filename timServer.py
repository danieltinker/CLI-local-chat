# opens a Thread for client communication
# client first sending username (and room).
# then server gives chat history.
# then A loop listening to client.


#TODO:
# model the restful api
# build new server and client that use restful api
# add register mechanism.
# see about "user has seen your msg" option.
#build docker file/running model
import socket 
import threading
import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

connectionArr = []
history = ["[Dan] hi","[Tam] hi","[chen] hi","[zeev] bye"]

def recv_username(conn):
    username="not initialize"
    usr_length = conn.recv(HEADER).decode(FORMAT)
    if usr_length:
        usr_length = int(usr_length)
        username = conn.recv(usr_length).decode(FORMAT)
    return username
    
def client_chat_history(conn):
    if history:
        conn.send("*** CHAT HISTORY ***\n------------------------\n".encode(FORMAT)) #add getting history from mongo
        for msg in history: #show chat history to new client
            conn.send(msg.encode(FORMAT))
            time.sleep(0.01)
    else:
        conn.send("Chat History Is Empty...".encode(FORMAT))
        
    
def notify_connected(conn,addr,username):
    print(f"[NEW CONNECTION] {addr} connected.")
    for client in connectionArr:
                    client.send(f"[{username}]  Joined the room".encode(FORMAT))
    connectionArr.append(conn)


def handle_client(conn, addr):
    username = recv_username(conn)
    # password = recv_password()
    # room = recv_room()
    
    notify_connected(conn,addr,username)
    
    client_chat_history(conn) #will need to recive the msg history from mongo.
    
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
        except OSError:
            print(f"[{addr}] connection was closed")
            connected=False
            continue
        if msg_length:  # store msgs on mongo. {time,room,username,data}
            local_time = time.localtime()
            t = time.strftime('%d %b %Y,%a %H:%M:%S', local_time)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                connectionArr.remove(conn)
                print(f"{t},[{addr}] [{username}]disconnect")
                print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
            
                for client in connectionArr:
                    client.send(f"{t},  [{username}]  disconnect".encode(FORMAT))
            else:    
                print(f" [{addr}] [{t}] [{username}] {msg}") 
                for client in connectionArr:
                    client.send(f"{t},  [{username}] {msg}".encode(FORMAT))

    conn.close()
    
        
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
 
try:
    print("[STARTING] server is starting(CNTRL+C to kill)...")
    start()
except KeyboardInterrupt:
    print("keyboard interrupptted server is closing all connections")
    for conn in connectionArr:
        conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
        conn.close()
finally:
    server.close()
    