import socket
import threading

class Server:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 4444  

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)

        print(f"Server đang lắng nghe trên {self.host}:{self.port}")

        self.clients = [] 

    def receive_data(self):
        while True:
            cr_client, cr_address = self.server_socket.accept()
            self.clients.append((cr_client, cr_address))
            print(f'Connected with {str(cr_address)}')

            thread = threading.Thread(target=self.handle_client, args=(cr_client, cr_address))
            thread.start()

    def handle_client(self, cr_client, cr_address):
        if len(self.clients) == 2:
            cr_client.send("O".encode())
        else:
            cr_client.send("X".encode())
    
        while True:
            data = cr_client.recv(1024).decode()
            print(data)
            for client, address in self.clients:
                if str(address) != str(cr_address): 
                    client.send(data.encode()) 

if __name__ == '__main__':
    server = Server()
    server.receive_data()