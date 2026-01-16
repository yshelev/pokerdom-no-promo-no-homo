from models.gameMessage import GameMessage
from models.actionType import ActionType
from models.GameStates.IState import IState

class PreflopState(IState):
    def __init__(
        self, 
        deck, 
        players,
        game_instance, 
    ):
        self.players = players
        self.game_instance = game_instance
        self.deck = deck
        
        self.players_num = len(self.players)
        
        self.index_of_player_to_get_card = -1
        self.current_player_index = -1
        
    async def _handle_message(self, player_id: str, message: GameMessage): 
        if self.current_player_index == self.index_of_player_to_get_card:
            if self.current_player_index != -1: 
                take_hand_message = GameMessage(
                    message.data, 
                    ActionType.TAKE_YOUR_HAND
                )
                
                player = self.players[self.index_of_player_to_get_card]
                await self.game_instance.send_message_to_player(
                    player, 
                    take_hand_message
                )
            
            self.index_of_player_to_get_card += 1
            self.current_player_index += 2
            self.current_player_index %= self.players_num
            
            if self.index_of_player_to_get_card >= self.players_num: 
                await self.game_instance.start_preflop_bet_round(self.players)
                return
            
            card_ask_message = GameMessage(
                [], 
                ActionType.GET_TWO_CARD
            )
            
            await self.game_instance.send_message_to_player(
                self.players[-1], 
                card_ask_message
            )
            return

        player_id_to_send = self.players[self.current_player_index]
        
        decode_message = GameMessage(
            message.data,
            ActionType.DECODE
        )
        
        await self.game_instance.send_message_to_player(
            player_id_to_send, 
            decode_message
        )
        
        self.current_player_index = (self.current_player_index + 1) % self.players_num