import socket

from config import ServerConfig
from client_structure import Client

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ServerConfig.address, ServerConfig.port)) 
server.listen(ServerConfig.num_of_listening_clients)

client, address = server.accept()

data = client.recv(1024).decode('utf-8')


client.close()
server.close()


class ServerSocket: 
    _socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _server_config: ServerConfig = ServerConfig()
    _clients: list = []
    
    def __init__(self):
        pass
    
    def open_connection(self): 
        self._socket.bind((
            self._server_config.address,
            self._server_config.port
        ))
        self._socket.listen(self._server_config.num_of_listening_clients)
        
    def accept_clients(self): 
        for _ in range(self._server_config.num_of_listening_clients): 
            client, address = self._socket.accept()
            self._clients.append(Client(client, address))
        
    def release(self): 
        self._socket.close()
        
    def send_str_message_to_client(self, client_index: int, message: str): 
        try: 
            client: Client = self._clients[client_index]
        except IndexError: 
            return

        client.socket_.send(message.encode())
        client.socket_.send(b"OK")
        
    def send_int_list_message_to_client(self, client_index: int, message: list[int]): 
        try: 
            client: Client = self._clients[client_index]
        except IndexError: 
            return

        
        for message_chank in message:
            client.socket_.send(str(message_chank).encode())
            
        client.socket_.send(b"OK")