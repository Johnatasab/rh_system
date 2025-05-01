import pytest
from utils.validadores import ValidadorDocumentos

class TestValidadorDocumentos:
    @pytest.mark.parametrize("cpf,valido", [
        ("529.982.247-25", True),     # Válido
        ("52998224725", True),        # Válido sem formatação
        ("111.111.111-11", False),    # Inválido (dígitos iguais)
        ("123.456.789-00", False),    # Inválido
        ("", False),                  # Vazio
        ("123", False)                # Tamanho inválido
    ])
    def test_validar_cpf(self, cpf, valido):
        assert ValidadorDocumentos.validar_cpf(cpf) == valido

    @pytest.mark.parametrize("cnpj,valido", [
        ("33.119.307/0001-73", True),    # Válido
        ("33119307000173", True),        # Válido sem formatação
        ("11.111.111/1111-11", False),   # Inválido (dígitos iguais)
        ("12.345.678/0001-00", False),   # Inválido
        ("", False),                     # Vazio
        ("123", False)                   # Tamanho inválido
    ])
    def test_validar_cnpj(self, cnpj, valido):
        assert ValidadorDocumentos.validar_cnpj(cnpj) == valido