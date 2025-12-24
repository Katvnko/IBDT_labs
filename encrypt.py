from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt_aes(plaintext: str, key: str) -> str:
    key_bytes = key.encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)

    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)

    return base64.b64encode(encrypted).decode('utf-8')


def decrypt_aes(ciphertext_base64: str, key: str) -> str:
    key_bytes = key.encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)

    encrypted_bytes = base64.b64decode(ciphertext_base64)
    decrypted_padded = cipher.decrypt(encrypted_bytes)

    return unpad(decrypted_padded, AES.block_size).decode('utf-8')

if __name__ == "__main__":
    plaintext = "Try to do 1 lab"
    key = "KaterynaVashchen"  # 16 bytes = 128 bit

    ciphertext = encrypt_aes(plaintext, key)
    decrypted = decrypt_aes(ciphertext, key)

    print("Plaintext :", plaintext)
    print("Key       :", key)
    print("Ciphertext:", ciphertext)
    print("Decrypted :", decrypted)
