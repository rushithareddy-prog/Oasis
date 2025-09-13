import socket
import threading

class ChatServer:
    def __init__(self, ip='127.0.0.1', port=12345):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # Map: client socket -> username

    def run(self):
        self.sock.bind((self.ip, self.port))
        self.sock.listen()
        print(f"Server started at {self.ip}:{self.port}. Waiting for clients...")

        while True:
            conn, addr = self.sock.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=self.client_handler, args=(conn,), daemon=True).start()

    def broadcast(self, message, sender=None):
        for client in list(self.clients):
            if client != sender:
                try:
                    client.send(message.encode())
                except:
                    client.close()
                    del self.clients[client]

    def client_handler(self, conn):
        try:
            conn.send("NICK".encode())  # Ask for nickname
            nickname = conn.recv(1024).decode().strip()
            self.clients[conn] = nickname
            self.broadcast(f"*** {nickname} joined the chat ***", conn)
            conn.send("Connected to server! Type messages and hit Enter.\n".encode())

            while True:
                message = conn.recv(1024).decode()
                if not message or message.lower() == 'exit':
                    break
                full_message = f"{nickname}: {message}"
                print(full_message)
                self.broadcast(full_message, conn)
        except:
            pass
        finally:
            nickname = self.clients.get(conn, "A user")
            print(f"{nickname} disconnected.")
            self.broadcast(f"*** {nickname} left the chat ***", conn)
            if conn in self.clients:
                del self.clients[conn]
            conn.close()

if __name__ == "__main__":
    server = ChatServer()
    server.run()
