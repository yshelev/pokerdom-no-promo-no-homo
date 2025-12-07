def extended_gcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def modinv(a: int, m: int) -> int:
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError('inverse does not exist')
    return x % m

def decrypt(c: int, k: int, p: int) -> int:
    k_inv = modinv(k, p - 1)
    return pow(c, k_inv, p)

def decrypt_message_with_key_list(message: int, key_list: list): 
    cur_mess = message
    for key_k, key_p in key_list: 
        cur_mess = decrypt(cur_mess, key_k, key_p)
    
    return cur_mess