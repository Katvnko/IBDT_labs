from dataclasses import dataclass
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


@dataclass
class KeyPair:
    private_key_pem: bytes
    public_key_pem: bytes

    @staticmethod
    def gen() -> "KeyPair":
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return KeyPair(private_key_pem=private_pem, public_key_pem=public_pem)


class Signature:
    @staticmethod
    def sign(private_key_pem: bytes, message: bytes) -> bytes:
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        return private_key.sign(
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )

    @staticmethod
    def verify(public_key_pem: bytes, message: bytes, signature: bytes) -> bool:
        public_key = serialization.load_pem_public_key(public_key_pem)
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256(),
            )
            return True
        except Exception:
            return False
