from datetime import datetime, time, timedelta, date
from typing import List, Optional
from enum import Enum

class TipoMarcacao(Enum):
    ENTRADA = "Entrada"
    SAIDA = "Saída"
    INICIO_INTERVALO = "Início Intervalo"
    FIM_INTERVALO = "Fim Intervalo"

class MarcacaoPonto:
    def __init__(self, matricula: str, tipo: TipoMarcacao, data_hora: datetime = None, observacao: str = None):
        self.matricula = matricula
        self.tipo = tipo
        self.data_hora = data_hora or datetime.now()
        self.observacao = observacao

class DiaTrabalho:
    def __init__(self, matricula: str, data: date):
        self.matricula = matricula
        self.data = data
        self.marcacoes: List[MarcacaoPonto] = []  # Correção aqui
        self.horas_trabalhadas: Optional[timedelta] = None  # Correção aqui
        self.horas_extras: Optional[timedelta] = None  # Correção aqui
        self.horas_faltantes: Optional[timedelta] = None  # Correção aqui
        self.saldo_dia: Optional[timedelta] = None  # Correção aqui

    def adicionar_marcacao(self, marcacao: MarcacaoPonto):
        """Adiciona uma marcação e recalcula as horas"""
        if not isinstance(marcacao, MarcacaoPonto):  # Verificação de tipo
            raise ValueError("Deve ser uma instância de MarcacaoPonto")

        # Garante que marcacoes é uma lista mutável
        if not hasattr(self, 'marcacoes'):
            self.marcacoes = []

        self.marcacoes.append(marcacao)
        self.calcular_horas()

    def calcular_horas(self):
        """Calcula horas trabalhadas e saldo"""
        if not self.marcacoes or len(self.marcacoes) < 2:
            self.horas_trabalhadas = timedelta(0)
            self.saldo_dia = timedelta(0)
            return

        # Ordena por horário
        self.marcacoes.sort(key=lambda m: m.data_hora)

        entrada = self.marcacoes[0].data_hora
        saida = self.marcacoes[-1].data_hora
        self.horas_trabalhadas = saida - entrada

        # Considera jornada padrão de 8 horas
        jornada_padrao = timedelta(hours=8)
        self.saldo_dia = self.horas_trabalhadas - jornada_padrao

        if self.saldo_dia > timedelta(0):
            self.horas_extras = self.saldo_dia
            self.horas_faltantes = timedelta(0)
        else:
            self.horas_extras = timedelta(0)
            self.horas_faltantes = -self.saldo_dia