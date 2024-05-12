import socket
import threading


class Server:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 4444

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)

        print(f"Server đang lắng nghe trên {self.host}:{self.port}")

        self.clients = []

    def receive_data(self):
        while True:
            client, address = self.server_socket.accept()
            self.clients.append((client, address))
            print(f"Connected with {str(address)}")

            thread = threading.Thread(target=self.handle_client, args=(client, address))
            thread.start()

    def handle_client(self, cr_client, cr_address):
        if len(self.clients) == 2:
            for client, address in self.clients:
                if str(address) != str(cr_address):
                    client.send("Connected".encode())
                    client.send("X".encode())
                    print(str(address), "X")
                else:
                    client.send("Connected".encode())
                    client.send("O".encode())
                    print(str(address), "O")

        try:
            while True:
                data = cr_client.recv(1024).decode()
                print(data)
                if not data:
                    break
                for client, address in self.clients:
                    if str(address) != str(cr_address):
                        client.send(data.encode())
        except (ConnectionResetError, socket.error):
            print(f"{str(cr_address)} has disconnected")
            for client, address in self.clients:
                if str(address) != str(cr_address):
                    client.send("Disconnected".encode())
        finally:
            cr_client.close()
            self.clients.remove((cr_client, cr_address))


if __name__ == "__main__":
    server = Server()
    server.receive_data()
