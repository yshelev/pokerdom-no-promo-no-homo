from services.cardTranslatorModule import CardToTextTranslator

class Printer: 
    translator: CardToTextTranslator = CardToTextTranslator()
    
    def print_int_card_deck(self, card_deck: list[int]): 
        for card in card_deck: 
            str_card = self.translator.translate_int_card_to_str(card)
            print(str_card, end=" ")
        print()
            
    def print_table_cards(self, card_deck: list[int]): 
        for card in card_deck: 
            str_card = self.translator.translate_int_card_to_str(card)
            print(str_card, end=" ")
        print()
            