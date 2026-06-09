import rsa
import os

class RSACipher:
    def __init__(self):
        # Determine the directory where this script is located
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.keys_dir = os.path.join(self.base_dir, "keys")
        os.makedirs(self.keys_dir, exist_ok=True)
        self.pubkey_path = os.path.join(self.keys_dir, "publicKey.pem")
        self.privkey_path = os.path.join(self.keys_dir, "privateKey.pem")

    def generate_keys(self):
        (pubkey, privkey) = rsa.newkeys(1024)
        with open(self.pubkey_path, "wb") as f:
            f.write(pubkey.save_pkcs1())
        with open(self.privkey_path, "wb") as f:
            f.write(privkey.save_pkcs1())

    def load_keys(self):
        if not os.path.exists(self.pubkey_path) or not os.path.exists(self.privkey_path):
            self.generate_keys()
        with open(self.pubkey_path, "rb") as f:
            pubkey = rsa.PublicKey.load_pkcs1(f.read())
        with open(self.privkey_path, "rb") as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read())
        return privkey, pubkey

    def encrypt(self, message: str, key) -> bytes:
        return rsa.encrypt(message.encode('utf-8'), key)

    def decrypt(self, ciphertext: bytes, key) -> str:
        return rsa.decrypt(ciphertext, key).decode('utf-8')

    def sign(self, message: str, private_key) -> bytes:
        return rsa.sign(message.encode('utf-8'), private_key, 'SHA-256')

    def verify(self, message: str, signature: bytes, public_key) -> bool:
        try:
            rsa.verify(message.encode('utf-8'), signature, public_key)
            return True
        except rsa.VerificationError:
            return False
