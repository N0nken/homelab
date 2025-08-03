import socket
import threading
import time
import json

class Client:
    def __init__(self, user, sock):
        self.user = user
        self.socket = sock

host = "localhost"
port = 12345
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))
clients = []

savedUsersLoginInfoFile = open("users.json", "r")
savedUsersLoginInfo = json.loads(savedUsersLoginInfoFile.read())
savedUsersLoginInfoFile.close()

def accepter_thread():
    while True:
        client, addr = serverSocket.accept()
        content = client.recv(1024).decode('utf-8')
        content = json.loads(content)
        if content["type"] == "login":
            username = content["username"]
            if username not in savedUsersLoginInfo["usernames"]:
                client.send(json.dumps({"type":"error", "code":100}).encode('utf-8'))
                client.close()
            elif savedUsersLoginInfo["users"][username]["password"] != content["password"]:
                client.send(json.dumps({"type":"error", "code":101}).encode('utf-8'))
                client.close()
            else:
                accept_client(username, client)
        elif content["type"] == "register":
            username = content["username"]
            if username in savedUsersLoginInfo["usernames"]:
                client.send(json.dumps({"type":"error", "code":110}).encode('utf-8'))
                client.close()
            elif content["password"] == "" or username == "":
                client.send(json.dumps({"type":"error", "code":111}).encode('utf-8'))
                client.close()
            else:
                client.send(json.dumps({"type":"success"}).encode('utf-8'))
                savedUsersLoginInfo["usernames"].append(username)
                savedUsersLoginInfo["users"][username] = {
                    "password": content["password"],
                    "email": content["email"]
                }
                with open("users.json", "w") as f:
                    json.dump(savedUsersLoginInfo, f)
                accept_client(username, client)
        elif content["type"] == "logout":
            pass
        elif content["type"] == "message":
            pass

def accept_client(user, sock):
    client = Client(user, sock)
    clients.append(client)
    print(f"User {user} connected.")

def sender_thread():
    while True:
        pass



accepterThread = threading.Thread(target=accepter_thread)
senderThread = threading.Thread(target=sender_thread)

accepterThread.start()
senderThread.start()