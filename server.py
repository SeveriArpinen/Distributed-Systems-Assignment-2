import socket
import threading

HOST = "127.0.0.1"
PORT= 5000
clients = {} # dict. for clients and nicknames client_socket: {nickname : channel}

#making a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP socket
server.bind((HOST,PORT))
server.listen()

print(f"Server running and listening on {HOST} : {PORT}")


# send message to clients, checks for the channel and that its not the sender
def message(message, channel, sender_socket=None):
    for client_socket, user in clients.items():
        if user['channel'] == channel and client_socket != sender_socket: # send to same channel, dont send message to sender
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

    while True:
        try:
            # get message
            msg = client_socket.recv(1024).decode("utf-8")

            if not msg or msg.lower() == "quit":
                break
            #check if client sends /join
            if msg.startswith("/join "):
                new_channel = msg.split(" ",1)[1].strip() # get new channel
                clients[client_socket]["channel"] = new_channel # change channel

                print(f"{nickname} joined {new_channel}")

            elif msg.startswith("/private "):
                splits = msg.split(" ", 2)
                if len(splits) >= 3:
                    private_name = splits[1]
                    private_msg = splits[2]

                    for sock, user in clients.items():
                        if user["nickname"] == private_name:
                            sock.send(f"[Private] {nickname}: {private_msg}\n".encode("utf-8"))
                            print(f"{nickname} -> {private_name}: {private_msg}")
                            break

            elif msg == "/users": # print users
                res = "Users online:\n"
                for user in clients.values():
                    res += f"{user['nickname']}\n"
                client_socket.send(res.encode("utf-8"))


            else:
                #normal message 
                current_channel = clients[client_socket]["channel"]
                print(f"[{current_channel}]{nickname}: {msg}")

                # send response to all clients 
                message(f"[{current_channel}] {nickname}: {msg}\n", current_channel, None)
        except:
            break

    # client disconnet
    print(f"{nickname} disconnected")
    del clients[client_socket]
    client_socket.close()

while True:
    client_socket, address = server.accept()

    #make a thread for a new client
    thread = threading.Thread(target=handle_client, args=(client_socket, address))
    thread.start() #run thread

    print(f"Active thread connections: {len(clients)+1}")