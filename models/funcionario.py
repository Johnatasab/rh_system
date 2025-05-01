from datetime import date
from typing import Optional
from utils.validadores import ValidadorDocumentos, ValidadorEmail

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
        self.salario = salario

        # Dados bancários
        self.banco = banco
        self.agencia = agencia
        self.conta = conta
        self.tipo_conta = tipo_conta

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