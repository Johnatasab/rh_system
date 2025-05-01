from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from models.ponto import MarcacaoPonto, DiaTrabalho, TipoMarcacao
from database.json_repository import PontoRepository


class PontoService:
    def __init__(self):
        self.repo = PontoRepository()

    def registrar_marcacao(self, matricula: str, tipo: TipoMarcacao, data_hora: datetime = None, observacao: str = None) -> MarcacaoPonto:
        """Registra uma nova marcação de ponto com tratamento de erros"""
        try:
            marcacao = MarcacaoPonto(
                matricula=matricula,
                tipo=tipo,
                data_hora=data_hora or datetime.now(),
                observacao=observacao
            )

            dia = self.obter_dia_trabalho(matricula, marcacao.data_hora.date())

            if not isinstance(dia, DiaTrabalho):  # Verificação adicional
                raise ValueError("Dia de trabalho inválido")

            dia.adicionar_marcacao(marcacao)
            self.repo.salvar_dia_trabalho(dia)

            return marcacao

        except Exception as e:
            # Log detalhado do erro
            print(f"Erro detalhado: {str(e)}")
            raise ValueError("Falha ao registrar ponto") from e

    def obter_dia_trabalho(self, matricula: str, data: date) -> DiaTrabalho:
        """Obtém o dia de trabalho, criando se não existir"""
        dia = self.repo.obter_dia_trabalho(matricula, data)
        if not dia:
            dia = DiaTrabalho(matricula=matricula, data=data)
        return dia

    def calcular_banco_horas(self, matricula: str,
                             data_inicio: date, data_fim: date) -> Dict:
        """Calcula o banco de horas no período"""
        dias = self.repo.listar_dias_trabalho(matricula, data_inicio, data_fim)

        total_extras = timedelta(0)
        total_faltantes = timedelta(0)

        for dia in dias:
            if dia.horas_extras:
                total_extras += dia.horas_extras
            if dia.horas_faltantes:
                total_faltantes += dia.horas_faltantes

        saldo_total = total_extras - total_faltantes

        return {
            'periodo': {'inicio': data_inicio, 'fim': data_fim},
            'total_extras': total_extras,
            'total_faltantes': total_faltantes,
            'saldo_total': saldo_total,
            'dias_trabalhados': len(dias)
        }

    def gerar_relatorio_mensal(self, matricula: str, mes: int, ano: int) -> Dict:
        """Gera relatório mensal de horas trabalhadas"""
        data_inicio = date(ano, mes, 1)
        data_fim = date(ano, mes + 1, 1) - timedelta(days=1)

        dias = self.repo.listar_dias_trabalho(matricula, data_inicio, data_fim)
        banco_horas = self.calcular_banco_horas(matricula, data_inicio, data_fim)

        return {
            'matricula': matricula,
            'mes': mes,
            'ano': ano,
            'dias_trabalhados': [
                {
                    'data': dia.data,
                    'marcacoes': [
                        {
                            'tipo': marcacao.tipo.value,
                            'hora': marcacao.data_hora.time(),
                            'observacao': marcacao.observacao
                        } for marcacao in dia.marcacoes
                    ],
                    'horas_trabalhadas': str(dia.horas_trabalhadas),
                    'saldo_dia': str(dia.saldo_dia)
                } for dia in dias
            ],
            'resumo': banco_horas
        }