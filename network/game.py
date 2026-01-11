from network.server import Server
from models.gameMessage import GameMessage
from models.actionType import ActionType
from models.GameStates.IState import IState
from models.GameStates.InitialState import InitialState
from models.GameStates.PreflopState import PreflopState
from models.GameStates.FlopState import FlopState

class Game:
    server: Server 
    players: list[str] = []
    cards: list[int] = [
        i * 10 + j 
        for i in range(2, 15)
        for j in range(1, 5)
    ]
    
    _state: IState
    
    def __init__(
        self,
        host, 
        port
    ): 
        self.server = Server(
            host, 
            port, 
            self.start, 
            self.handle_message
        )
        
    async def start(self, players):
        self.players = players
        
        self._state = InitialState(
            self.players, 
            self
        )
        
        message = GameMessage(
            data=self.cards, 
            action=ActionType.ENCODE
        )
        
        await self.server.send_message_to_player(
            self.players[0], 
            message
        )  
    
            
    async def handle_message(self, player_id: str, message): 
        await self._state.handle_message(player_id, message)
    
    async def send_message_to_player(self, player_id: str, message): 
        await self.server.send_message_to_player(player_id, message)
        
    async def start_dealing_cards(self, deck: list[int], players: list[str]): 
        self._state = PreflopState(
            deck, 
            players, 
            self
        )
        
        message = GameMessage(
            deck,
            ActionType.SHUFFLE, 
            
        )
        
        await self.send_message_to_player(
            self.players[-1], 
            message
        )
        
    async def to_flop(self, players: list[str]): 
        self._state = FlopState(
            players, 
            self
        )
        
        message = GameMessage(
            [],
            ActionType.GET_THREE_CARD, 
        )
        
        await self.send_message_to_player(
            self.players[-1], 
            message
        )