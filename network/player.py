from network.clientSocket import ClientSocket
from models.gameMessage import GameMessage
from models.actionType import ActionType
from services.encoder import Encoder
from services.decoder import Decoder
from services.generator import Generator
from services.printer import Printer
from services.cardCheckService import CardCheckService
import random
from aioconsole import ainput
import asyncio


class Player: 
    _socket: ClientSocket
    player_id: str
    deck: list[int]
    
    hand: list[int]
    table_cards: list[int] = []
    
    _encoder: Encoder = Encoder()
    _decoder: Decoder = Decoder()
    _printer: Printer = Printer()
    _deck_checker: CardCheckService = CardCheckService()
    _lock = asyncio.Lock()
    
    def __init__(
        self,
        player_id: str, 
        host: str, 
        port: int, 
        stack: int = 5000
    ):    
        self.stack = stack
             
        self._socket = ClientSocket(
            host, 
            port, 
            self.handle_message
        )
        self.player_id = player_id
                
        self._socket.start(player_id)
    
    async def handle_message(self, message: GameMessage): 
        async with self._lock: 
            await self._handle_message(message)
    
    async def _handle_message(self, message: GameMessage):
        await asyncio.sleep(.3)
        cards = message.data
        if message.action == ActionType.MAKE_BET: 
            bets = message.data
            
            print("Ваш ход, делайте ставку!")
            print()
            for username, bet in bets.items(): 
                print(f"Ставка игрока {username} - {bet}")
            print()
            print("Ваш стек: ")
            print(self.stack)
            print("Доступные действия: ")
            print("1. Показать (мои) карты")
            print("2. Поднять ставку (raise)")
            print("3. Подвердить ставку (call)")
            print("4. Сбросить карты (fold)")
            while player_action := await ainput("Какое действие вы хотите совершить?\n"):
                try: 
                    player_action = int(player_action)
                except Exception as e:
                    print("Введите число от 1 до 4") 
                    continue
                if player_action not in range(1, 5): 
                    print("Введите число от 1 до 4") 
                    continue
                
                if player_action == 1:
                    print("Ваша рука:")
                    self._printer.print_int_card_deck(self.hand)
                    print("Карты на столе:")
                    self._printer.print_int_card_deck(self.table_cards) 
                if player_action == 2: 
                    while player_bet := await ainput("Введите вашу ставку\n"): 
                        try:
                            player_bet = int(player_bet)
                            if self.stack < player_bet: 
                                print("Вы ввели ставку, превышающую ваш стек. ")
                            overall_bet = player_bet + bets.get(self.player_id, 0)
                            if overall_bet > max(bets.values()): 
                                self.stack -= player_bet
                                print(f"Ставка принята")
                                break
                            else: 
                                print("Введите ставку, превыщающую максимальную ставку за столом")
                        except Exception as e: 
                            print(e)
                            
                        
                    bet_message = GameMessage(
                        [player_bet], 
                        ActionType.RAISE
                    )
                    
                    player_bet = max(bets.values()) - bets.get(self.player_id, 0)
                    self.stack -= player_bet
                        
                    await self.send_message(bet_message)
                    break
                if player_action == 3: 
                    bet_message = GameMessage(
                        [], 
                        ActionType.CALL
                    )
                        
                    await self.send_message(bet_message)
                    break
                if player_action == 4: 
                    bet_message = GameMessage(
                        [], 
                        ActionType.FOLD
                    )
                        
                    await self.send_message(bet_message)
                    break
                
        if message.action == ActionType.ARE_YOU_READY: 
            print("Хост предлагает сыграть следующую раздачу. вы в игре?")
            while (ans := await ainput("Введите ваш ответ, да\нет\n")) not in ["да", "нет"]:
                pass
            
            answer = GameMessage(
                [], 
                ""
            )
            
            if ans == "да": 
                answer.action = ActionType.IS_READY
            else: 
                answer.action = ActionType.NOT_READY
            
            await self.send_message(answer)
            
        if message.action == ActionType.WINNER: 
            winner, bank = message.data
            if winner == self.player_id: 
                print("Вы победили эту раздачу, поздравляю!")
                print(f"Выигрыш составил: {bank} фишек")
                self.stack += bank
            else: 
                print(f"Вы проиграли, победитель: {winner}")
        
        if message.action == ActionType.GET_BEST_HAND: 
            self.my_combination = self.table_cards + self.hand
            
            cards = self._deck_checker.best_poker_hand(self.my_combination)[1]
            self._printer.print_int_card_deck(cards)
            
            answer = GameMessage(
                cards, 
                ActionType.GET_BEST_HAND
            )
            
            await self.send_message(answer)
        
        if message.action == ActionType.TAKE_TABLE_CARDS: 
            print("Карты на столе: ")
            self.table_cards += message.data
            self._printer.print_int_card_deck(self.table_cards)
            await asyncio.sleep(.15)
            print("Ваш ход скоро начнется, подождите. ")
        
        if message.action == ActionType.TAKE_YOUR_HAND: 
            self.hand = self._decoder.decrypt_list_messages(message.data, self.secret_key, self.public_key)
            print("Ваша рука: ")
            self._printer.print_int_card_deck(self.hand)
            await asyncio.sleep(.15)
            print("Ваш ход скоро начнется, подождите. ")
        if message.action == ActionType.GET_THREE_CARD:
            cards = []
            for _ in range(3): 
                c = random.choice(self.deck)
                self.deck.remove(c)
                cards.append(c)
            
            answer = GameMessage(
                cards, 
                ActionType.GET_THREE_CARD
            )
            
            await self.send_message(answer)
        if message.action == ActionType.GET_ONE_CARD:
            c = random.choice(self.deck)
            self.deck.remove(c)
            
            answer = GameMessage(
                [c], 
                ActionType.GET_ONE_CARD
            )
            
            await self.send_message(answer)
             
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