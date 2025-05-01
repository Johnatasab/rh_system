from utils.validadores import ValidadorDocumentos

class Fornecedor:
    def __init__(self, **kwargs):
        self._cnpj = None
        self._cnpj = kwargs.get('cnpj')

    @property
    def cnpj(self) -> str:
        return self._cnpj

    @cnpj.setter
    def cnpj(self, value: str):
        if not ValidadorDocumentos.validar_cnpj(value):
            raise ValueError("CNPJ inválido")
        self._cnpj = ValidadorDocumentos.formatar_cnpj(value)