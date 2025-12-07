import secrets
from sympy import isprime
from math import gcd
from encoder import encrypt
from decoder import decrypt_message_with_key_list
from encoder import encrypt_message_with_list_keys

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
    deck = [
        i * 10 + j 
        for i in range(14)
        for j in range(1, 5)
    ]
    
    p = generate_large_prime(512)  

    m = 142

    k1 = generate_key(p)
    k2 = generate_key(p)
    
    encrypted_cards = []
    encrypted_cards.extend(encrypt_message_with_list_keys(card, [k1, k2]) for card in deck)    

    
    print([decrypt_message_with_key_list(encrypted_card, [k2, k1]) for encrypted_card in encrypted_cards])
    