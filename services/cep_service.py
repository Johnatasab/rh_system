from http.client import responses

import requests
from typing import Dict, Optional
from utils.logger import logger

class CEPService:
    BASE_URL = "https://viacep.com.br/ws/{cep}/json/"

    @classmethod
    def consultar_cep(cls, cep: str) -> Optional[Dict[str, str]]:
        try:
            # Remove caracteres não numéricos
            cep_limpo = ''.join(filter(str.isdigit, cep))
            if len(cep_limpo) != 8:
                raise ValueError("CEP deve conter 8 dígitos")

            url = cls.BASE_URL.format(cep=cep_limpo)
            response = requests.get(url)
            response.raise_for_status()

            dados = response.json()
            if 'erro' in dados:
                return None

            return {
                'cep': dados.get('cep', ''),
                'logradouro': dados.get('logradouro', ''),
                'complemento': dados.get('complemento', ''),
                'bairro': dados.get('bairro', ''),
                'localidade': dados.get('localidade', ''),
                'uf': dados.get('uf', ''),
                'ibge': dados.get('ibge', ''),
                'gia': dados.get('gia', ''),
                'ddd': dados.get('ddd', ''),
                'siafi': dados.get('siafi', '')
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao consultar CEP {cep}: {str(e)}")
            return None
        except ValueError as e:
            logger.warning(f"CEP inválido {cep}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao consultar CEP {cep}: {str(e)}")
            return None