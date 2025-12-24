from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64


def decrypt_aes(ciphertext_base64: str, key: str) -> str:
    key_bytes = key.encode("utf-8")
    cipher = AES.new(key_bytes, AES.MODE_ECB)

    encrypted_bytes = base64.b64decode(ciphertext_base64)
    decrypted_padded = cipher.decrypt(encrypted_bytes)

    return unpad(decrypted_padded, AES.block_size).decode("utf-8")


if __name__ == "__main__":
    ciphertext = "Cu6sAzCLvJdjc+3tEZoPDA=="
    key = "KaterynaVashchen"

    plaintext = decrypt_aes(ciphertext, key)

    print("Ciphertext:", ciphertext)
    print("Key       :", key)
    print("Decrypted :", plaintext)
