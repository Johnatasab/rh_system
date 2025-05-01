from datetime import date
from typing import Optional, Union
from utils.validadores import ValidadorDocumentos, ValidadorEmail
from utils.criptografia import criptografia_service

class Funcionario:
    def __init__(
            self,
            # Dados básicos
            matricula: str,
            nome: str,
            cpf: str,
            rg: str,
            data_nascimento: date,
            genero: str,
            estado_civil: str,
            # Contatos
            email: str,
            telefone: Optional[str],
            celular: Optional[str],
            # Endereço
            cep: str,
            endereco: str,
            numero: str,
            complemento: Optional[str],
            bairro: str,
            cidade: str,
            estado: str,
            # Dados profissionais
            cargo: str,
            departamento: str,
            data_admissao: date,
            tipo_contrato: str,
            jornada_trabalho: str,
            salario: float,
            # Dados bancários
            banco: str,
            agencia: str,
            conta: str,
            tipo_conta: str,
            ativo: bool = True,
            **kwargs
    ):
        # Dados pessoais
        self.matricula = matricula
        self.nome = nome
        self._cpf = None
        self.cpf = kwargs.get('cpf')
        self.rg = rg
        self.data_nascimento = data_nascimento
        self.genero = genero
        self.estado_civil = estado_civil

        # Contatos
        self._email = None
        self.email = kwargs.get('email')
        self.telefone = telefone
        self.celular = celular

        # Endereço
        self._cep = None
        self.cep = kwargs.get('cep')
        self.endereco = endereco
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado

        # Dados profissionais
        self.cargo = cargo
        self.departamento = departamento
        self.data_admissao = data_admissao
        self.tipo_contrato = tipo_contrato
        self.jornada_trabalho = jornada_trabalho
        self._salario = None
        self._dados_bancarios = {
            'banco': None,
            'agencia': None,
            'conta': None,
            'tipo_conta': None
        }
        # Atribui usando os setters que fazem criptografia
        if 'salario' in kwargs:
            self.salario = kwargs['salario']
        if 'banco' in kwargs:
            self.banco = kwargs['banco']
        if 'agencia' in kwargs:
            self.agencia = kwargs['agencia']
        if 'conta' in kwargs:
            self.conta = kwargs['conta']
        if 'tipo_conta' in kwargs:
            self.tipo_conta = kwargs['tipo_conta']

        self.ativo = ativo

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, value: str):
        if not ValidadorDocumentos.validar_cpf(value):
            raise ValueError("CPF inválido")
        self._cpf = ValidadorDocumentos.formatar_cpf(value)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        email_normalizado = ValidadorEmail.normalizar_email(value)
        if not email_normalizado:
            raise ValueError("E-mail inválido")
        self._email = email_normalizado

    @property
    def cep(self) -> str:
        return self._cep

    @cep.setter
    def cep(self, value: str):
        cep_limpo = ''.join(filter(str.isdigit, str(value)))
        if len(cep_limpo) != 8:
            raise ValueError ("CEP deve conter 8 dígitos")
        self._cep = f"{cep_limpo[:5]}-{cep_limpo[5:]}"

    @property
    def salario(self) -> float:
        """Descriptografa o salário para acesso"""
        if self._salario is None:
            return None
        return float(criptografia_service.descriptografar(self._salario))

    @salario.setter
    def salario(self, value: Union[str, int, float]):
        """Criptografa o salário antes de armazenar"""
        if value is not None:
            self._salario = criptografia_service.criptografar(value)

    # Propriedades para dados bancários
    @property
    def banco(self) -> str:
        return self._get_dado_bancario('banco')
    @banco.setter
    def banco(self, value: str):
        self._set_dado_bancario('banco', value)

    # Agência
    @property
    def agencia(self, value: str):
        return self._get_dado_bancario('agencia')
    @banco.setter
    def agencia(self, value: str):
        self._set_dado_bancario('agencia', value)

    # Conta
    @property
    def conta(self, value: str):
        return self._get_dado_bancario('conta')
    @banco.setter
    def conta(self, value: str):
        self._set_dado_bancario('conta', value)

    # Tipo de conta
    @property
    def tipo_conta(self, value: str):
        return self._get_dado_bancario('tipo_conta')
    @banco.setter
    def tipo_conta(self, value: str):
        self._set_dado_bancario('tipo_conta', value)

    def _get_dado_bancario(self, campo: str) -> str:
        """Método auxiliar para descriptografar dados bancários"""
        valor = self._dados_bancarios.get(campo)
        return criptografia_service.descriptografar(valor) if valor else None

    def _set_dado_bancario(self, campo: str, value: str):
        """Método auxiliar para criptografar dados bancários"""
        self._dados_bancarios[campo] = criptografia_service.criptografar(value) if value else None

    def to_dict(self) -> dict:
        """Serializa o funcionário mantendo dados sensíveis criptografados"""
        dados = {
            # ... (outros campos)
            'salario': self._salario,
            'dados_bancarios': {
                'banco': self._dados_bancarios['banco'],
                'agencia': self._dados_bancarios['agencia'],
                'conta': self._dados_bancarios['conta'],
                'tipo_conta': self._dados_bancarios['tipo_conta']
            }
        }
        return dados

    def __str__(self):
        return f"{self.matricula} - {self.nome} ({self.cargo})"

    def to_dict(self):
        return {
            # Dados pessoais
            'matricula': self.matricula,
            'nome': self.nome,
            'cpf': self.cpf,
            'rg': self.rg,
            'data_nascimento': self.data_nascimento.isoformat(),
            'genero': self.genero,
            'estado_civil': self.estado_civil,
            # Contatos
            'email': self.email,
            'telefone': self.telefone,
            'celular': self.celular,
            # Endereço
            'cep': self.cep,
            'endereco': self.endereco,
            'numero': self.numero,
            'complemento': self.complemento,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado,
            # Dados profissionais
            'cargo': self.cargo,
            'departamento': self.departamento,
            'data_admissao': self.data_admissao.isoformat(),
            'tipo_contrato': self.tipo_contrato,
            'jornada_trabalho': self.jornada_trabalho,
            'salario': self.salario,
            # Dados bancários
            'banco': self.banco,
            'agencia': self.agencia,
            'conta': self.conta,
            'tipo_conta': self.tipo_conta,
            'ativo': self.ativo
        }

    @classmethod
    def from_dict(cls, data: dict):
        try:
            return cls(
                # Dados básicos
                matricula=data['matricula'],
                nome=data.get('nome', ''),
                cpf=data.get('cpf', ''),
                rg=data.get('rg', ''),
                data_nascimento=date.fromisoformat(data['data_nascimento']),
                genero=data['genero'],
                estado_civil=data['estado_civil'],
                # Contatos
                email=data['email'],
                telefone=data.get('telefone'),
                celular=data.get('celular'),
                # Endereço
                cep=data['cep'],
                endereco=data['endereco'],
                numero=data['numero'],
                complemento=data.get('complemento'),
                bairro=data['bairro'],
                cidade=data['cidade'],
                estado=data['estado'],
                # Dados profissionais
                cargo=data['cargo'],
                departamento=data['departamento'],
                data_admissao=date.fromisoformat(data['data_admissao']),
                tipo_contrato=data['tipo_contrato'],
                jornada_trabalho=data['jornada_trabalho'],
                salario=data['salario'],
                # Dados bancários
                banco=data['banco'],
                agencia=data['agencia'],
                conta=data['conta'],
                tipo_conta=data.get('tipo_conta', 'Corrente'),
                ativo=data.get('ativo', True)
            )
        except Exception as e:
            print(f"Erro ao criar funcionário: {e}")
            return None