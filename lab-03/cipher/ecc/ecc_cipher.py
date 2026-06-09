import ecdsa
import os

class ECCCipher:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.keys_dir = os.path.join(self.base_dir, "keys")
        os.makedirs(self.keys_dir, exist_ok=True)
        self.pubkey_path = os.path.join(self.keys_dir, "publicKey.pem")
        self.privkey_path = os.path.join(self.keys_dir, "privateKey.pem")

    def generate_keys(self):
        sk = ecdsa.SigningKey.generate()
        vk = sk.get_verifying_key()
        
        with open(self.privkey_path, 'wb') as p:
            p.write(sk.to_pem())
            
        with open(self.pubkey_path, 'wb') as p:
            p.write(vk.to_pem())
            
    def load_keys(self):
        if not os.path.exists(self.pubkey_path) or not os.path.exists(self.privkey_path):
            self.generate_keys()
        with open(self.privkey_path, 'rb') as p:
            sk = ecdsa.SigningKey.from_pem(p.read())
            
        with open(self.pubkey_path, 'rb') as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())
            
        return sk, vk

    def sign(self, message, key):
        return key.sign(message.encode('ascii'))

    def verify(self, message, signature, key=None):
        if key is None:
            _, key = self.load_keys()
        try:
            return key.verify(signature, message.encode('ascii'))
        except ecdsa.BadSignatureError:
            return False
