class Decoder: 
    def extended_gcd(self, a: int, b: int):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def modinv(self, a: int, m: int) -> int:
        g, x, y = self.extended_gcd(a, m)
        if g != 1:
            raise ValueError('inverse does not exist')
        return x % m

    def decrypt(self, c: int, k_inv: int, p: int) -> int:
        return pow(c, k_inv, p)
    
    def decrypt_list_messages(self, c: list[int], k, p): 
        output = []
        k_inv = self.modinv(k, p - 1)
        for message in c: 
            output.append(self.decrypt(message, k_inv, p))
            
        return output
    
    def decrypt_message_with_key_list(self, message: int, key_list: list): 
        cur_mess = message
        for key_k, key_p in key_list: 
            cur_mess = self.decrypt(cur_mess, key_k, key_p)
        
        return cur_mess