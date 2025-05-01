import uuid
from datetime import date
from typing import List, Optional, Dict
from models.ferias import Ferias, StatusFerias
from database.json_repository import FeriasRepository
from services.rh_service import RHService


class FeriasService:
    def __init__(self):
        self.repo = FeriasRepository()
        self.rh_service = RHService()

    def _gerar_id(self) -> str:
        return str(uuid.uuid4())

    def agendar_ferias(
            self,
            matricula_funcionario: str,
            data_inicio: date,
            data_fim: date,
            observacoes: Optional[str] = None
    ) -> Ferias:
        """Agenda um novo período de férias para um funcionário."""

        # Validações básicas
        if data_inicio >= data_fim:
            raise ValueError("Data de início deve ser anterior à data de fim")

        if (data_fim - data_inicio).days > 30:
            raise ValueError("Período de férias não pode exceder 30 dias")

        # Verifica se funcionário existe
        funcionario = self.rh_service.buscar_por_matricula(matricula_funcionario)
        if not funcionario:
            raise ValueError("Funcionário não encontrado")

        # Verifica conflitos de agendamento
        ferias_existentes = self.repo.buscar_por_matricula(matricula_funcionario)
        for ferias in ferias_existentes:
            if (data_inicio <= ferias.data_fim and data_fim >= ferias.data_inicio and
                    ferias.status in [StatusFerias.AGENDADA, StatusFerias.APROVADA]):
                raise ValueError("Conflito com período de férias já agendado")

        # Cria o agendamento
        nova_ferias = Ferias(
            id=self._gerar_id(),
            matricula_funcionario=matricula_funcionario,
            data_inicio=data_inicio,
            data_fim=data_fim,
            status=StatusFerias.AGENDADA,
            observacoes=observacoes
        )

        self.repo.salvar_ferias(nova_ferias)
        return nova_ferias

    def listar_ferias_por_matricula(self, matricula: str) -> List[Ferias]:
        """Lista todas as férias agendadas para um funcionário."""
        return self.repo.buscar_por_matricula(matricula)

    def listar_todas_ferias(self, status: Optional[StatusFerias] = None) -> List[Ferias]:
        """Lista todas as férias cadastradas no sistema."""
        todas = self.repo.listar_todas()
        if status:
            return [f for f in todas if f.status == status]
        return todas

    def buscar_ferias_por_id(self, id: str) -> Optional[Ferias]:
        """Busca um agendamento de férias pelo ID."""
        return self.repo.buscar_por_id(id)

    def atualizar_ferias(self, id: str, dados_atualizados: Dict) -> Optional[Ferias]:
        """Atualiza os dados de um agendamento de férias."""
        ferias = self.repo.buscar_por_id(id)
        if not ferias:
            return None

        campos_permitidos = {'data_inicio', 'data_fim', 'status', 'observacoes'}

        for campo, valor in dados_atualizados.items():
            if campo in campos_permitidos:
                if campo == 'status':
                    valor = StatusFerias(valor)
                setattr(ferias, campo, valor)

        self.repo.salvar_ferias(ferias)
        return ferias

    def cancelar_ferias(self, id: str) -> bool:
        """Cancela um agendamento de férias."""
        ferias = self.repo.buscar_por_id(id)
        if ferias and ferias.status in [StatusFerias.AGENDADA, StatusFerias.APROVADA]:
            ferias.status = StatusFerias.CANCELADA
            self.repo.salvar_ferias(ferias)
            return True
        return False

    def aprovar_ferias(self, id: str) -> bool:
        """Aprova um agendamento de férias."""
        ferias = self.repo.buscar_por_id(id)
        if ferias and ferias.status == StatusFerias.AGENDADA:
            ferias.status = StatusFerias.APROVADA
            self.repo.salvar_ferias(ferias)
            return True
        return False

    def registrar_ferias_gozadas(self, id: str) -> bool:
        """Registra que as férias foram gozadas."""
        ferias = self.repo.buscar_por_id(id)
        if ferias and ferias.status == StatusFerias.APROVADA:
            ferias.status = StatusFerias.GOZADA
            self.repo.salvar_ferias(ferias)
            return True
        return False

    def remover_ferias(self, id: str) -> bool:
        """Remove permanentemente um agendamento de férias."""
        return self.repo.remover_ferias(id)