class Encoder: 
    def encrypt(
        self,
        m: int,
        k: int,
        p: int
    ) -> int:
        return pow(m, k, p)

    def encrypt_message_with_list_keys(self, message: int, key_list: list):
        cur_mess = message
        for key_k, key_p in key_list: 
            cur_mess = self.encrypt(cur_mess, key_k, key_p)
            
        return cur_mess
    
    def encode_list_of_messages(
        self,
        messages: list[int], 
        secret_key: int, 
        public_key: int
    ) -> list[int]: 
        output = []
        
        for message in messages:
            output.append(self.encrypt(message, secret_key, public_key))
            
        return output