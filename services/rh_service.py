from datetime import date
from typing import Optional, List, Dict
from database.json_repository import FuncionarioRepository
from models.funcionario import Funcionario
from utils.matricula import gerar_matricula

class RHService:
    def __init__(self):
        self.repo = FuncionarioRepository()

    def cadastrar_funcionario(
            self,
            # Dados pessoais
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
            tipo_conta: str
    ) -> Funcionario:
        """Cadastra um novo funcionário no sistema."""

        # Verifica se CPF já está cadastrado
        if self.buscar_por_cpf(cpf):
            raise ValueError("CPF já cadastrado no sistema")

        # Gera matrícula automática
        matricula = gerar_matricula()

        # Cria o objeto Funcionario
        funcionario = Funcionario(
            matricula=matricula,
            nome=nome,
            cpf=cpf,
            rg=rg,
            data_nascimento=data_nascimento,
            genero=genero,
            estado_civil=estado_civil,
            email=email,
            telefone=telefone,
            celular=celular,
            cep=cep,
            endereco=endereco,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            cargo=cargo,
            departamento=departamento,
            data_admissao=data_admissao,
            tipo_contrato=tipo_contrato,
            jornada_trabalho=jornada_trabalho,
            salario=salario,
            banco=banco,
            agencia=agencia,
            conta=conta,
            tipo_conta=tipo_conta
        )

        self.repo.salvar_funcionario(funcionario)
        return funcionario

    def buscar_por_matricula(self, matricula: str) -> Optional[Funcionario]:
        """Busca um funcionário por matrícula."""
        return self.repo.buscar_por_matricula(matricula)

    def buscar_por_cpf(self, cpf: str) -> Optional[Funcionario]:
        """Busca um funcionário por CPF."""
        funcionarios = self.repo.listar_funcionarios()
        for func in funcionarios:
            if func.cpf == cpf:
                return func
        return None

    def listar_funcionarios(self) -> List[Funcionario]:
        """Retorna todos os funcionários cadastrados."""
        return self.repo.listar_funcionarios()

    def atualizar_funcionario(self, matricula: str, dados_atualizados: Dict) -> Optional[Funcionario]:
        """Atualiza os dados de um funcionário."""
        funcionario = self.buscar_por_matricula(matricula)
        if not funcionario:
            return None

        # Atualiza os campos permitidos
        campos_permitidos = {
            'nome', 'email', 'telefone', 'celular', 'cep', 'endereco', 'numero',
            'complemento', 'bairro', 'cidade', 'estado', 'cargo', 'departamento',
            'tipo_contrato', 'jornada_trabalho', 'salario', 'banco', 'agencia',
            'conta', 'tipo_conta', 'estado_civil'
        }

        for campo, valor in dados_atualizados.items():
            if campo in campos_permitidos and hasattr(funcionario, campo):
                setattr(funcionario, campo, valor)

        self.repo.salvar_funcionario(funcionario)
        return funcionario

    def desativar_funcionario(self, matricula: str) -> bool:
        """Desativa um funcionário no sistema."""
        funcionario = self.buscar_por_matricula(matricula)
        if funcionario:
            funcionario.ativo = False
            self.repo.salvar_funcionario(funcionario)
            return True
        return False

    def listar_funcionarios_ativos(self) -> List[Funcionario]:
        """Retorna apenas os funcionários ativos."""
        return [f for f in self.listar_funcionarios() if f.ativo]

    def buscar_por_nome(self, nome: str) -> List[Funcionario]:
        """Busca funcionários por parte do nome (case insensitive)."""
        nome = nome.lower()
        return [f for f in self.listar_funcionarios() if nome in f.nome.lower()]

    def apagar_funcionario(self, matricula: str) -> bool:
        """Remove permanentemente um funcionário do sistema."""
        return self.repo.remover_funcionario(matricula)