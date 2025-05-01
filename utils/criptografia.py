import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Union


class CriptografiaService:
    def __init__(self, senha_mestre: bytes, salt: bytes = None):
        """Inicializa o serviço de criptografia com uma senha mestre
        Args:
            senha_mestre: Senha usada para derivar a chave de criptografia
            salt: Valor aleatório para fortalecer a criptografia (opcional)"""
        self.salt = salt or os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=480000,
        )
        self.chave = urlsafe_b64encode(kdf.derive(senha_mestre))
        self.fernet = Fernet(self.chave)

    def criptografar(self, dado: Union[str, int, float]) -> str:
        """Criptografa um dado sensível (texto ou número)
        Args:
            dado: Dado a ser criptografado (pode ser string, int ou float)
        Returns:
            String com o dado criptografado e codificado em base64"""
        dado_str = str(dado)
        dado_bytes = dado_str.encode('utf-8')
        return self.fernet.encrypt(dado_bytes).decode('utf-8')

    def descriptografar(self, dado_criptografado: str) -> str:
        """Descriptografa um dado previamente criptografado
        Args:
            dado_criptografado: Dado criptografado (string em base64)
        Returns:
            String com o dado descriptografado"""
        dado_bytes = dado_criptografado.encode('utf-8')
        return self.fernet.decrypt(dado_bytes).decode('utf-8')

    @staticmethod
    def gerar_senha_mestre() -> bytes:
        """Gera uma senha mestre aleatória segura"""
        return Fernet.generate_key()

# Instância global (deve ser configurada no startup do sistema)
criptografia_service = None

def configurar_criptografia(senha_mestre: bytes, salt: bytes = None):
    """Configura o serviço global de criptografia"""
    global criptografia_service
    criptografia_service = CriptografiaService(senha_mestre, salt)