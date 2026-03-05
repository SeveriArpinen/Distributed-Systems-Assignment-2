import socket
import threading

HOST = "127.0.0.1"
PORT= 5000
clients = {} # dict. for clients and nicknames client_socket: {nickname : channel}

#making a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen(1)

print(f"Server running and listening on {HOST} : {PORT}")


# send message to all clients connected
def broadcast(message, channel, sender_socket=None):
    for client_socket, info in clients.items():
        if info['channel'] == channel and client_socket != sender_socket: # dont send message to sender
            try:
                client_socket.send(message.encode("utf-8"))
            except:
                pass


def handle_client(client_socket, address): # handle single clients in separate threads
    print(f"New connection from {address}")
    #first message is nickname
    nickname = client_socket.recv(1024).decode("utf-8") # get nickname
    clients[client_socket] = {"nickname": nickname, "channel": "general"} #set name and general channel

    print(f"{nickname} joined general chat")
    broadcast(f"{nickname} joined general chat\n", "general")
    client_socket.send("You are currently in general channel. /join to join different channels\n".encode("utf-8"))

    while True:
        try:
            # get message
            message = client_socket.recv(1024).decode("utf-8")

            if message.lower() == "quit":
                break
            #check if client sends /join
            if message.startswith("/join"):
                new_channel = message.split(" ",1)[1].strip() # get new channel
                clients[client_socket]["channel"] = new_channel # change channel

                # broadcast join to everyone
                print(f"{nickname} joined {new_channel}")
                broadcast(f"{nickname} joined {channel}\n", new_channel)
                client_socket.send(f"You joined the channel {new_channel}\n".encode("utf-8"))

            else:
                #normal message 
                #print message
                current_channel = clients[client_socket]["channel"]
                print(f"[{current_channel}]{nickname}: {message}")

                # send response to all clients 
                broadcast(f"[{current_channel}] {nickname}: {message}\n", current_channel, client_socket)
        except:
            break

    # client disconnet
    channel = clients[client_socket]["channel"]
    print(f"{nickname} left the chat")
    broadcast(f"{nickname} left the chat\n", channel)
    del clients[client_socket]
    client_socket.close()

while True:
    client_socket, address = server.accept()

    #make a thread for a new client
    thread = threading.Thread(target=handle_client, args=(client_socket, address))
    thread.start() #run thread

    print(f"Active thread connections: {len(clients)+1}")