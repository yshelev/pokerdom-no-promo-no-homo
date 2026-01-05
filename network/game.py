from network.server import Server
from models.gameMessage import GameMessage
from models.gameMessageData import GameMessageData

class Game:
    server: Server 
    players: list[str] = []
    cards: list[int] = [
        i * 10 + j 
        for i in range(2, 15)
        for j in range(1, 5)
    ]
    def __init__(
        self,
        host, 
        port
    ): 
        self.server = Server(
            host, 
            port, 
            self.start
        )
        
    def start(self, players): 
        self.players = players
        
        
        
        self.server.send_message_to_player(
            self.players[0]
        )        