import re
from typing import Optional

class ValidadorDocumentos:
    @staticmethod
    def limpar_documento(documento: str) -> str:
        """Remover caracteres não numéricos do documento"""
        return re.sub(r'[^0-9]', '', documento)

    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """Validar um CPF de acordo com as regrasda Receita Federal"""
        cpf = ValidadorDocumentos.limpar_documento(cpf)
        if len(cpf) != 11:
            return False
        # Verificar se todos os dígitos dão iguais
        if cpf == cpf[0] * 11:
            return False
        # Calcula o primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        # Calcular o segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        # Verificar se os dígitos calculados conferem com os informados
        return int(cpf[9]) == digito1 and int(cpf[10]) == digito2

    @staticmethod
    def validar_cnpj(cnpj: str) -> bool:
        """Valida um CNPJ de acordo com as regras da Receita Federal"""
        cnpj = ValidadorDocumentos.limpar_documento(cnpj)
        if len(cnpj) != 14:
            return False
        # Verifica se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return False
        # Cálculo do primeiro dígito verificador
        peso = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = 0
        for i in range(12):
            soma += int(cnpj[i]) * peso[i]
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        # Cálculo do segundo dígito verificador
        peso = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = 0
        for i in range(13):
            soma += int(cnpj[i]) * peso[i]
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        # Verifica se os dígitos calculados conferem com os informados
        return int(cnpj[12]) == digito1 and int(cnpj[13]) == digito2

    @staticmethod
    def formatar_cpf(cpf: str) -> str:
        """Formata um CPF no padrão 000.000.000-00"""
        cpf = ValidadorDocumentos.limpar_documento(cpf)
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

    @staticmethod
    def formatar_cnpj(cnpj: str) -> str:
        """Formatar um CNPJ no padrão 00.000.000/0000-00"""
        cnpj = ValidadorDocumentos.limpar_documento(cnpj)
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

class ValidadorEmail:
    @staticmethod
    def validar_email(email: str) -> bool:
        """
        Valida um endereço de e-mail conforme RFC 5322
        Retorna True se válido, False caso contrário
        """
        regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

        if re.fullmatch(regex, email, re.IGNORECASE):
            return True
        return False

    @staticmethod
    def normalizar_email(email: str) -> Optional[str]:
        """
        Normaliza o e-mail (minúsculas e remove espaços)
        Retorna None se inválido
        """
        email = email.strip().lower()
        if ValidadorEmail.validar_email(email):
            return email
        return None