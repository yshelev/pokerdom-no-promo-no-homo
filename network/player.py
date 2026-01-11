from network.clientSocket import ClientSocket
from models.gameMessage import GameMessage
from models.actionType import ActionType
from services.encoder import Encoder
from services.decoder import Decoder
from services.generator import Generator
from services.printer import Printer
import random


class Player: 
    _socket: ClientSocket
    player_id: str
    deck: list[int]
    
    hand: list[int]
    
    _encoder: Encoder = Encoder()
    _decoder: Decoder = Decoder()
    _printer: Printer = Printer()
    
    def __init__(
        self,
        player_id: str, 
        host: str, 
        port: int
    ):         
        self._socket = ClientSocket(
            host, 
            port, 
            self.handle_message
        )
        self.player_id = player_id
                
        self._socket.start(player_id)
        
    async def handle_message(self, message: GameMessage):
        cards = message.data
        if message.action == ActionType.TAKE_YOUR_HAND: 
            self.hand = self._decoder.decrypt_list_messages(message.data, self.secret_key, self.public_key)
            self._printer.print_int_card_deck(self.hand)
            
        if message.action == ActionType.GET_TWO_CARD: 
            output_cards = []
            for _ in range(2): 
                c = random.choice(self.deck)
                self.deck.remove(c)
                output_cards.append(c)
                  
            answer = GameMessage(
                output_cards, 
                ActionType.GET_TWO_CARD
            )
            
            await self.send_message(answer)
        
        if message.action == ActionType.SHUFFLE: 
            
            random.shuffle(cards)
            
            answer = GameMessage(
                cards, 
                ActionType.SHUFFLE
            )
            
            await self.send_message(answer)
        
        if message.action == ActionType.DECODE: 
            decoded_cards = self._decoder.decrypt_list_messages(cards, self.secret_key, self.public_key)
            
            answer = GameMessage(
                data=decoded_cards, 
                action=ActionType.DECODE
            )
            
            await self.send_message(answer)
            
        if message.action == ActionType.ENCODE: 
            encoded_cards = self._encoder.encode_list_of_messages(cards, self.secret_key, self.public_key)
            
            answer = GameMessage(
                data=encoded_cards, 
                action=ActionType.ENCODE
            )
            
            self.deck = encoded_cards
            
            await self.send_message(answer)
        
        if message.action == ActionType.ACKNOWLEDGMENT: 
            self.public_key = message.data[0]
            
            self.secret_key = Generator.generate_key(self.public_key)
        
    async def send_message(self, message: GameMessage): 
        await self._socket.send_message(message)