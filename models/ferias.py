from datetime import date
from typing import Optional
from enum import Enum

class StatusFerias(Enum):
    """Enumeração para status de férias"""
    AGENDADA = "Agendada"
    APROVADA = "Aprovada"
    CANCELADA = "Cancelada"
    GOZADA = "Gozada"

class Ferias:
    def __init__(
        self,
        id: str,
        matricula_funcionario: str,
        data_inicio: date,
        data_fim: date,
        status: StatusFerias = StatusFerias.AGENDADA,
        observacoes: Optional[str] = None
    ):
        self.id = id
        self.matricula_funcionario = matricula_funcionario
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.status = status
        self.observacoes = observacoes
        self.dias_ferias = (data_fim - data_inicio).days + 1

    def __str__(self):
        return (f"Férias [{self.id}] - Funcionário: {self.matricula_funcionario} | "
                f"Período: {self.data_inicio} a {self.data_fim} | "
                f"Status: {self.status.value}")

    def to_dict(self):
        return {
            "id": self.id,
            "matricula_funcionario": self.matricula_funcionario,
            "data_inicio": self.data_inicio.isoformat(),
            "data_fim": self.data_fim.isoformat(),
            "status": self.status.value,
            "observacao": self.observacoes,
            "dias_ferias": self.dias_ferias
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            matricula_funcionario=data["matricula_funcionario"],
            data_inicio=date.fromisoformat(data["data_inicio"]),
            data_fim=date.fromisoformat(data["data_fim"]),
            status=StatusFerias(data["status"]),
            observacoes=data.get("observacoes")
        )