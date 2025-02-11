from cryptography.fernet import Fernet
from app.core.config.settings import get_settings
from base64 import b64encode, b64decode

settings = get_settings()

class FieldEncryption:
    def __init__(self):
        self._fernet = Fernet(settings.ENCRYPTION_KEY.encode())
    
    def encrypt(self, data: str) -> str:
        if not data:
            return data
        return b64encode(
            self._fernet.encrypt(data.encode())
        ).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        if not encrypted_data:
            return encrypted_data
        return self._fernet.decrypt(
            b64decode(encrypted_data.encode())
        ).decode()

field_encryptor = FieldEncryption()
