"""
License Management System
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

from datetime import datetime
from typing import Optional
import jwt
from cryptography.fernet import Fernet
import hashlib
import requests
from app.core.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)

class LicenseManager:
    def __init__(self):
        self.settings = get_settings()
        self._encryption_key = None
        self._hardware_id = None

    @property
    def hardware_id(self) -> str:
        """Generate unique hardware identifier"""
        if not self._hardware_id:
            import platform
            import uuid
            
            # Coleta informações do hardware
            system_info = platform.uname()
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                          for elements in range(0, 2*6, 2)][::-1])
            
            # Cria hash único
            hardware_string = f"{system_info.system}-{system_info.node}-{mac}"
            self._hardware_id = hashlib.sha256(hardware_string.encode()).hexdigest()
            
        return self._hardware_id

    def validate_license(self, license_key: str) -> bool:
        """Validate license key with server"""
        try:
            # Verifica com servidor de licenças
            response = requests.post(
                f"{self.settings.LICENSE_SERVER_URL}/validate",
                json={
                    "license_key": license_key,
                    "hardware_id": self.hardware_id,
                    "product_id": self.settings.PRODUCT_ID
                },
                headers={"X-API-Key": self.settings.LICENSE_API_KEY}
            )
            
            if response.status_code != 200:
                logger.error(f"License validation failed: {response.text}")
                return False
                
            license_data = response.json()
            
            # Verifica validade da licença
            if not self._verify_license_data(license_data):
                return False
                
            # Armazena informações da licença
            self._store_license_info(license_data)
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating license: {str(e)}")
            return False

    def _verify_license_data(self, license_data: dict) -> bool:
        """Verify license data integrity and validity"""
        try:
            # Decodifica token JWT
            decoded = jwt.decode(
                license_data["token"],
                self.settings.LICENSE_PUBLIC_KEY,
                algorithms=["RS256"]
            )
            
            # Verifica dados
            if decoded["hardware_id"] != self.hardware_id:
                logger.error("Hardware ID mismatch")
                return False
                
            if decoded["product_id"] != self.settings.PRODUCT_ID:
                logger.error("Product ID mismatch")
                return False
                
            expiry = datetime.fromtimestamp(decoded["exp"])
            if expiry < datetime.now():
                logger.error("License expired")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error verifying license data: {str(e)}")
            return False

    def _store_license_info(self, license_data: dict):
        """Store encrypted license information"""
        try:
            if not self._encryption_key:
                self._encryption_key = Fernet.generate_key()
                
            f = Fernet(self._encryption_key)
            encrypted_data = f.encrypt(str(license_data).encode())
            
            # Armazena dados criptografados
            with open(self.settings.LICENSE_FILE_PATH, "wb") as file:
                file.write(encrypted_data)
                
        except Exception as e:
            logger.error(f"Error storing license info: {str(e)}")

    def check_license_status(self) -> Optional[dict]:
        """Check current license status"""
        try:
            if not self._encryption_key:
                return None
                
            # Lê dados criptografados
            with open(self.settings.LICENSE_FILE_PATH, "rb") as file:
                encrypted_data = file.read()
                
            f = Fernet(self._encryption_key)
            decrypted_data = f.decrypt(encrypted_data)
            
            return eval(decrypted_data.decode())
            
        except Exception as e:
            logger.error(f"Error checking license status: {str(e)}")
            return None

    def revoke_license(self):
        """Revoke current license"""
        try:
            import os
            if os.path.exists(self.settings.LICENSE_FILE_PATH):
                os.remove(self.settings.LICENSE_FILE_PATH)
            self._encryption_key = None
        except Exception as e:
            logger.error(f"Error revoking license: {str(e)}")

license_manager = LicenseManager()
