import socket
import threading

HOST = "127.0.0.1"
PORT= 5000
clients = [] # list for clients

#making a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen(1)

print(f"Server running and listening on {HOST} : {PORT}")


# send message to all clients connected
def broadcast(message):
    for client in clients:
        client.send(message.encode("utf-8"))

def handle_client(client_socket, address): # handle single clients in separate threads
    while True:
        try:
            # get message
            message = client_socket.recv(1024).decode("utf-8")

            if message.lower() == "quit":
                break

            print(f"Received message from {address}: {message}")

            # send response
            broadcast(f"{address}: {message}")
        except:
            break

    # client disconnet
    print(f"Client disconnected: {address}")
    clients.remove(client_socket)
    client_socket.close()

while True:
    client_socket, address = server.accept()

    #add a new client connected
    clients.append(client_socket)

    #make a thread for a new client
    thread = threading.Thread(target=handle_client, args=(client_socket, address))
    thread.start() #run thread

    print(f"Active thread connections: {threading.active_count() - 1}")