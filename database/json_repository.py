import json
import os
from typing import List, Optional
from models.funcionario import Funcionario
from models.ferias import Ferias, StatusFerias

class FuncionarioRepository:
    def __init__(self, file_path: str = "funcionarios.json"):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

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