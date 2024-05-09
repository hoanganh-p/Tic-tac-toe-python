import socket
import threading

class Server:
    def __init__(self):
        self.host = 'localhost'
        self.port = 4444  

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print(f"Server đang lắng nghe trên {self.host}:{self.port}")

        self.clients = [] 

    def receive_data(self):
        while True:
            cr_client, cr_address = self.server_socket.accept()
            self.clients.append(cr_client)
            print(f'Connected with {str(cr_address)}')

            thread = threading.Thread(target=self.handle_client, args=(cr_client, ))
            thread.start()

    def handle_client(self, cr_client):
        if len(self.clients) % 2 == 0:
            cr_client.send("O".encode())
        else:
            cr_client.send("X".encode())
    
        while True:
            data = cr_client.recv(1024)#.decode('utf-8')
            print(data)
            for client in self.clients:
                if client.getpeername() != cr_client.getpeername():
                    client.send(data) 

if __name__ == '__main__':
    server = Server()
    server.receive_data()