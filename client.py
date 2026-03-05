import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

# making socket and connecting to server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            print(f"\n{message}")
            print("You: ", end="", flush=True)
        except:
            print("\nConnection closed!")
            break

def send_messages():
    while True: 
        #sending a message
        message = input("You: ")
        client.send(message.encode("utf-8"))

        if message.lower() == "quit":
            #close connection
            client.close()
            break

print("Connected to server. Send messages or type quit to exit: ")
#Start receive thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# start message send thread
send_messages()