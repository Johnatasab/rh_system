import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class RHLogger:
    def __init__(self, name: str = 'rh_system', log_dir: str = 'logs'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Criar diretório de logs se não existir
        os.makedirs(log_dir, exist_ok=True)

        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Handler para arquivo (com rotação)
        log_file = os.path.join(log_dir, f'rh_system_{datetime.now().strftime("%d%m%Y")}.log')
        file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)

        # Adiciona handler ao logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message, exc_info=True)

    def critical(self, message: str):
        self.logger.critical(message, exc_info=True)

# Instância global do logger
logger = RHLogger()