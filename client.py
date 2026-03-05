import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

# making socket and connecting to server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

nickname = input("Enter your nickname: ")
client.send(nickname.encode("utf-8"))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            print(message)
        except:
            print("Connection closed!")
            client.close()
            break

def send_messages():
    while True: 
        #sending a message
        message = input()
        client.send(message.encode("utf-8"))

        if message.lower() == "quit":
            #close connection
            client.close()
            break

print("\nConnected to server.")
print("Type your messages or quit to exit:\n")
#Start receive thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# start message send thread
send_messages()