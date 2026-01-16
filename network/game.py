from network.server import Server
from models.gameMessage import GameMessage
from models.actionType import ActionType
from models.GameStates.IState import IState
from models.GameStates.InitialState import InitialState
from models.GameStates.PreflopState import PreflopState
from models.GameStates.FlopState import FlopState
from models.GameStates.RiverState import RiverState
from models.GameStates.TurnState import TurnState
from models.GameStates.EndGameState import EndGameState
from models.GameStates.BetRoundState import BetRoundState
from models.GameStates.PostGameState import PostGameState

class Game:
    _server: Server 
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
        self._server = Server(
            host, 
            port, 
            self.start, 
            self.handle_message
        )
        
    async def start(self, players):
        self.players = players
        
        self._state = InitialState(
            self.players.copy(), 
            self
        )
        
        message = GameMessage(
            data=self.cards, 
            action=ActionType.ENCODE
        )
        
        await self._server.send_message_to_player(
            self.players[0], 
            message
        )  
            
    async def handle_message(self, player_id: str, message): 
        await self._state.handle_message(player_id, message)
    
    async def send_message_to_player(self, player_id: str, message): 
        await self._server.send_message_to_player(player_id, message)
        
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
    async def start_preflop_bet_round(self, players):
        print("start preflop bet round") 
        await self.start_bet_round(players, self.to_flop)
    
    async def start_flop_bet_round(self, players):
        print("start flop bet round") 
        await self.start_bet_round(players, self.to_turn)
    
    async def start_turn_bet_round(self, players):
        print("start turn bet round") 
        await self.start_bet_round(players, self.to_river)
    
    async def start_river_bet_round(self, players):
        print("start river bet round") 
        await self.start_bet_round(players, self.to_end_game)
        
    async def start_bet_round(self, players, callback): 
        self._state = BetRoundState(
            players, 
            callback, 
            self
        )
        
        message = GameMessage(
            {player: 0 for player in players}, 
            ActionType.MAKE_BET
        )
        
        await self.send_message_to_player(
            players[0], 
            message
        )
        
    async def to_end_game(self, players): 
        self._state = EndGameState(
            players, 
            self
        )
        
        for player in players: 
            message = GameMessage(
                [], 
                ActionType.GET_BEST_HAND
            )
            await self.send_message_to_player(player, message)
            
    async def to_post_game(self): 
        self._state = PostGameState(
            self.players, 
            self
        )    
        
        message = GameMessage(
            [], 
            ActionType.ARE_YOU_READY
        )

        await self.send_message_to_player(
            self.players[0], 
            message
        )
        
    async def to_turn(self, players):
        self._state = TurnState(
            players, 
            self
        )
        
        message = GameMessage(
            [],
            ActionType.GET_ONE_CARD, 
        )
        
        await self.send_message_to_player(
            self.players[-1], 
            message
        )
    async def to_river(self, players: list[str]): 
        self._state = RiverState(
            players, 
            self
        )
        
        message = GameMessage(
            [],
            ActionType.GET_ONE_CARD, 
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
        
    async def remove_disconnected_players(self, disconnected):
        print("removing")
        await self._server.remove_disconnected_players(disconnected)