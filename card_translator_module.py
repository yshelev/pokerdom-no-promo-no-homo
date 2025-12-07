class CardToTextTranslator: 
    suit_int_to_str_map: dict[int: str] = {
        1: "♣", 
        2: "♠", 
        3: "♥", 
        4: "♦"
    }
    
    dignity_int_to_str_map: dict[int: str] = {
        11: "J", 
        12: "Q", 
        13: "K", 
        14: "A", 
    }
    
    def translate_int_card_to_str(self, card_value: int): 
        int_suit = card_value % 10
        int_card_dignity = card_value // 10
        
        str_suit = self.suit_int_to_str_map[int_suit]
        str_card_dignity = self.dignity_int_to_str_map.get(int_card_dignity, str(int_card_dignity))

        return f"{str_suit}{str_card_dignity}"