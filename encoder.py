def encrypt(m: int, k: int, p: int) -> int:
    return pow(m, k, p)

def encrypt_message_with_list_keys(message: int, key_list: list):
    cur_mess = message
    for key_k, key_p in key_list: 
        cur_mess = encrypt(cur_mess, key_k, key_p)
        
    return cur_mess
    