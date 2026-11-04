import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_data(key: bytes, plaintext: str) -> bytes:
    if not plaintext:
        return b""
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, plaintext.encode('utf-8'), None)
    return nonce + ct

def decrypt_data(key: bytes, ciphertext: bytes) -> str:
    if not ciphertext:
        return ""
    nonce = ciphertext[:12]
    ct = ciphertext[12:]
    return AESGCM(key).decrypt(nonce, ct, None).decode('utf-8')