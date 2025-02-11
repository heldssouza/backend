"""
Code Obfuscation System
Copyright (c) 2025 BControlTech Consultoria em Gestão e Tecnologia
All rights reserved.
"""

import base64
import zlib
import random
import string
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class CodeObfuscator:
    def __init__(self):
        self._key_map: Dict[str, str] = {}
        self._generate_key_map()

    def _generate_key_map(self):
        """Generate random key mapping"""
        chars = string.ascii_letters + string.digits
        for c in chars:
            self._key_map[c] = ''.join(random.choices(chars, k=3))

    def obfuscate(self, code: str) -> str:
        """Obfuscate code"""
        try:
            # Comprime o código
            compressed = zlib.compress(code.encode())
            
            # Codifica em base64
            encoded = base64.b85encode(compressed)
            
            # Aplica substituição de caracteres
            result = ''
            for c in encoded.decode():
                if c in self._key_map:
                    result += self._key_map[c]
                else:
                    result += c
                    
            return result
            
        except Exception as e:
            logger.error(f"Error obfuscating code: {str(e)}")
            return code

    def deobfuscate(self, obfuscated: str) -> str:
        """Deobfuscate code"""
        try:
            # Reverte substituição de caracteres
            reverse_map = {v: k for k, v in self._key_map.items()}
            decoded = ''
            i = 0
            while i < len(obfuscated):
                found = False
                for length in range(3, 0, -1):
                    chunk = obfuscated[i:i+length]
                    if chunk in reverse_map:
                        decoded += reverse_map[chunk]
                        i += length
                        found = True
                        break
                if not found:
                    decoded += obfuscated[i]
                    i += 1
                    
            # Decodifica base64
            decoded = base64.b85decode(decoded.encode())
            
            # Descomprime
            decompressed = zlib.decompress(decoded)
            
            return decompressed.decode()
            
        except Exception as e:
            logger.error(f"Error deobfuscating code: {str(e)}")
            return obfuscated

class CodeProtector:
    def __init__(self):
        self.obfuscator = CodeObfuscator()

    def protect_source(self, source_code: str) -> str:
        """Protect source code with obfuscation and anti-tampering"""
        try:
            # Adiciona verificações anti-tampering
            protected_code = f"""
import sys
import hashlib
import platform

def _verify_integrity():
    # Verifica ambiente de execução
    if hasattr(sys, '_MEIPASS'):
        # Detecta se está sendo executado via PyInstaller
        return False
        
    # Verifica debugger
    import os
    if 'PYTHONBREAKPOINT' in os.environ:
        return False
        
    # Verifica ambiente virtual
    if hasattr(sys, 'real_prefix') or sys.base_prefix != sys.prefix:
        # Está rodando em um ambiente virtual
        pass
        
    return True

if not _verify_integrity():
    raise RuntimeError("Integrity check failed")

{source_code}
"""
            # Ofusca o código
            return self.obfuscator.obfuscate(protected_code)
            
        except Exception as e:
            logger.error(f"Error protecting source: {str(e)}")
            return source_code

code_protector = CodeProtector()
