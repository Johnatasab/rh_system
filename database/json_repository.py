import json
import os
from typing import List, Optional, Dict
from models.funcionario import Funcionario
from models.ferias import Ferias, StatusFerias
from models.ponto import DiaTrabalho, MarcacaoPonto,TipoMarcacao
from datetime import date, datetime, timedelta


class FuncionarioRepository:
    def __init__(self, file_path: str = "funcionarios.json"):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

    def _serialize_funcionario(self, funcionario: Funcionario) -> Dict:
        """Usa to_dict() que já retorna dados criptografados"""
        return funcionario.to_dict()

    def _deserialize_funcionario(self, data: Dict) -> Funcionario:
        """Os dados já vem criptografados, são descriptografados nas propriedades"""
        return Funcionario(**data)

    def carregar_dados(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return [] # Retornar lsita vazia se arquivo não existe ou está vazio

    def salvar_dados(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.funcionarios, f, indent=4)

    def salvar_funcionario(self, funcionario: Funcionario) -> None:
        funcionarios = self.listar_funcionarios()
        # Verificar se já existe um funcionário coma mesma matrícula
        funcionarios = [f for f in funcionarios if f.matricula != funcionario.matricula]
        funcionarios.append(funcionario)
        self._salvar_todos(funcionarios)

    def buscar_por_matricula(self, matricula: str) -> Optional[Funcionario]:
        funcionarios = self.listar_funcionarios()
        for func in funcionarios:
            if func.matricula == matricula:
                return func
        return None

    def listar_funcionarios(self) -> List[Funcionario]:
        """Carrega funcionários do JSON com tratamento de erros"""
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                funcionarios = []
                for item in data:
                    func = Funcionario.from_dict(item)
                    if func:  # Só adiciona se foi criado com sucesso
                        funcionarios.append(func)
                return funcionarios
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Erro: Arquivo JSON inválido")
            return []

    def _salvar_todos(self, funcionarios: List[Funcionario]) -> None:
        with open(self.file_path, 'w') as f:
            json.dump([func.to_dict() for func in funcionarios], f, indent=2)

    def remover_funcionario(self, matricula: str) -> bool:
        # Carrega os dados atualizados
        self.funcionarios = self.carregar_dados()

        # Procura o funcionário
        for i, func in enumerate(self.funcionarios):
            if str(func['matricula']) == str(matricula):  # Compara como string
                del self.funcionarios[i]
                self.salvar_dados()  # Persiste a alteração
                return True

        return False

class FeriasRepository:
    # Iniciar objeto
    def __init__(self, file_path: str = "ferias.json"):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

    def _salvar_todos(self, ferias_list: list) -> None:
        with open(self.file_path, 'w') as f:
            json.dump([f.to_dict() for f in ferias_list], f, indent=2)

    def salvar_ferias(self, ferias: Ferias) -> None:
        ferias_list = self.listar_todos()
        # Remove se já existir com o mesmo ID
        ferias_list = [f for f in ferias_list if f.id != ferias.id]
        ferias_list.append(ferias)
        self._salvar_todos(ferias_list)

    def listar_todos(self) -> list[Ferias]:
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return [Ferias.from_dict(item) for item in data]

    def buscar_por_id(self, id: str) -> Optional[Ferias]:
        ferias_list = self.listar_todos()
        for ferias in ferias_list:
            if ferias.id == id:
                return ferias
        return None

    def buscar_por_matricula(self, matricula: str) -> list[Ferias]:
        ferias_list = self.listar_todos()
        return [f for f in ferias_list if f.matricula_funcionario == matricula]

    def remover_ferias(self, id: str) -> bool:
        ferias_list = self.listar_todos()
        novas_ferias = [f for f in ferias_list if f.id != id]
        if len(novas_ferias) < len(ferias_list):
            self._salvar_todos(novas_ferias)
            return True
        return False

class PontoRepository:
    def __init__(self, file_path: str = "ponto.json"):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

    def _serialize_dia_trabalho(self, dia: DiaTrabalho) -> Dict:
        return {
            'matricula': dia.matricula,
            'data': dia.data.isoformat(),
            'marcacoes': [
                {
                    'tipo': marcacao.tipo.value,
                    'data_hora': marcacao.data_hora.isoformat(),
                    'observacao': marcacao.observacao
                } for marcacao in dia.marcacoes
            ],
            'horas_trabalhadas': str(dia.horas_trabalhadas) if dia.horas_trabalhadas else None,
            'saldo_dia': str(dia.saldo_dia) if dia.saldo_dia else None
        }

    def _deserialize_dia_trabalho(self, data: Dict, minutes=None) -> DiaTrabalho:
        dia = DiaTrabalho(
            matricula=data['matricula'],
            data=date.fromisoformat(data['data'])
        )

        for marcacao_data in data['marcacoes']:
            marcacao = MarcacaoPonto(
                matricula=data['matricula'],
                tipo=TipoMarcacao(marcacao_data['tipo']),
                data_hora=datetime.fromisoformat(marcacao_data['data_hora']),
                observacao=marcacao_data.get('observacao')
            )
            dia.marcacoes.append(marcacao)

        # Restaura cálculos
        if data.get('horas_trabalhadas'):
            horas, minutos, _ = map(int, data['horas_trabalhadas'].split(':'))
            dia.horas_trabalhadas = timedelta(hours=horas, minutes=minutes)

        if data.get('saldo_dia'):
            horas, minutos, _ = map(int, data['saldo_dia'].split(':'))
            dia.saldo_dia = timedelta(hours=horas, minutes=minutes)

        return dia

    def salvar_dia_trabalho(self, dia: DiaTrabalho) -> None:
        dias = self.listar_todos_dias()

        # Remove dia existente se houver
        dias = [d for d in dias if not (
                d.matricula == dia.matricula and d.data == dia.data
        )]

        dias.append(dia)
        self._salvar_todos(dias)

    def obter_dia_trabalho(self, matricula: str, data: date) -> Optional[DiaTrabalho]:
        dias = self.listar_todos_dias()
        for dia in dias:
            if dia.matricula == matricula and dia.data == data:
                return dia
        return None

    def listar_dias_trabalho(self, matricula: str,
                             data_inicio: date, data_fim: date) -> List[DiaTrabalho]:
        dias = self.listar_todos_dias()
        return [
            dia for dia in dias
            if dia.matricula == matricula
               and data_inicio <= dia.data <= data_fim
        ]

    def listar_todos_dias(self) -> List[DiaTrabalho]:
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return [self._deserialize_dia_trabalho(item) for item in data]

    def _salvar_todos(self, dias: List[DiaTrabalho]) -> None:
        with open(self.file_path, 'w') as f:
            json.dump([self._serialize_dia_trabalho(dia) for dia in dias], f, indent=2)