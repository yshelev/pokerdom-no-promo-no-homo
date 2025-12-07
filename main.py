import secrets
from sympy import isprime
from math import gcd
from encoder import encrypt
from decoder import decrypt_message_with_key_list
from encoder import encrypt_message_with_list_keys

import random
from printer import Printer

def generate_large_prime(bits: int = 1024) -> int:
    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1)) | 1  
        if isprime(candidate):
            return candidate

def generate_key(p: int) -> int:
    phi = p - 1
    while True:
        k = secrets.randbelow(phi - 2) + 2  
        if gcd(k, phi) == 1:
            return k, p

if __name__ == "__main__":
    printer = Printer()
    deck = [
        i * 10 + j 
        for i in range(2, 15)
        for j in range(1, 5)
    ]
    
    print("стандартная колода: ")
    printer.print_int_card_deck(deck)
    
    p = generate_large_prime(512)  

    m = 142

    k1 = generate_key(p)
    k2 = generate_key(p)
    k3 = generate_key(p)
    
    print("шифруем колоду тремя (вставить сюда количество игроков👌👌) ключами")
        
    encrypted_cards = [encrypt_message_with_list_keys(card, [k1, k2, k3]) for card in deck]
    
    random.shuffle(encrypted_cards)
    random.shuffle(encrypted_cards)
    random.shuffle(encrypted_cards)

    print("тусуем тремя людьми")
    
    print("как независимый наблюдатель попросим ключи у игроков, посмотрим колоду")
    
    decrypted_deck = [decrypt_message_with_key_list(card, [k1, k2, k3]) for card in encrypted_cards]
    
    printer.print_int_card_deck(decrypted_deck) 
    c = random.choice(encrypted_cards)
    encrypted_cards.remove(c)
    card1 = decrypt_message_with_key_list(c, [k2, k3])
    c = random.choice(encrypted_cards)
    encrypted_cards.remove(c)
    card2 = decrypt_message_with_key_list(c, [k2, k3])
    
    player_1_deck = [card1, card2]

    c = random.choice(encrypted_cards)
    encrypted_cards.remove(c)
    card1 = decrypt_message_with_key_list(c, [k1, k3])
    c = random.choice(encrypted_cards)
    encrypted_cards.remove(c)
    card2 = decrypt_message_with_key_list(c, [k1, k3])

    player_2_deck = [card1, card2]
    
    c = random.choice(encrypted_cards)
    encrypted_cards.remove(c)
    card1 = decrypt_message_with_key_list(c, [k1, k2])
    c = random.choice(encrypted_cards)
    encrypted_cards.remove(c)
    card2 = decrypt_message_with_key_list(c, [k1, k2])
    
    player_3_deck = [card1, card2]
    
    print("""зашифрованные колоды игроков (никакие игроки карты друг друга не видят, 
          однако каждый расшифровывал карты другого человека своим ключом)""")
    
    print("карты первого игрока: ")
    print(*player_1_deck)
    print("карты второго игрока: ")
    print(*player_2_deck)
    print("карты третьего игрока: ")
    print(*player_3_deck)
    
    decrypted_deck_player_1 = []
    for card in player_1_deck: 
        decrypted_deck_player_1.append(
            decrypt_message_with_key_list(card, [k1])
        )
        
    print("Игрок 1 расшифровал свои карты своим же ключом, посмотрел их: ")
    printer.print_int_card_deck(decrypted_deck_player_1)    
    
    decrypted_deck_player_2 = []
    for card in player_2_deck: 
        decrypted_deck_player_2.append(
            decrypt_message_with_key_list(card, [k2])
        )
    print("Игрок 2 расшифровал свои карты своим же ключом, посмотрел их: ")
    
    printer.print_int_card_deck(decrypted_deck_player_2)    
    
    decrypted_deck_player_3 = []
    for card in player_3_deck: 
        decrypted_deck_player_3.append(
            decrypt_message_with_key_list(card, [k3])
        )
        
    print("Игрок 3 расшифровал свои карты своим же ключом, посмотрел их: ")
    
    printer.print_int_card_deck(decrypted_deck_player_3)
    
    print("допустим, игроки поставили moneys, думаю не самая важная часть:)")
    
    print("раскидаем стол👿👿")
    
    c = random.choice(encrypted_cards)
    encrypted_cards.remove(c)
    table_card1 = decrypt_message_with_key_list(c, [k1, k2, k3])
    c = random.choice(encrypted_cards)
    encrypted_cards.remove(c)
    table_card2 = decrypt_message_with_key_list(c, [k1, k2, k3])
    c = random.choice(encrypted_cards)
    encrypted_cards.remove(c)
    table_card3 = decrypt_message_with_key_list(c, [k1, k2, k3])
    
    table_cards = [
        table_card1,
        table_card2,
        table_card3,
    ]
    
    print("как там, префлоп?:")
    
    printer.print_int_card_deck(table_cards)
    
    c = random.choice(encrypted_cards)
    encrypted_cards.remove(c)
    table_card4 = decrypt_message_with_key_list(c, [k1, k2, k3])
    
    table_cards.append(table_card4)
        
    print("как там, префлоп2?:")
    
    printer.print_int_card_deck(table_cards)
    
    
    c = random.choice(encrypted_cards)
    encrypted_cards.remove(c)
    table_card5 = decrypt_message_with_key_list(c, [k1, k2, k3])
    
    table_cards.append(table_card5)
    
            
    print("как там, префлоп3?:")
    
    printer.print_int_card_deck(table_cards)