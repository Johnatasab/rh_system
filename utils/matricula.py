from datetime import datetime
from database.json_repository import FuncionarioRepository

def gerar_matricula() -> str:
    """Gera uma matrícula no formato AAAAXXXX onde: - AAAA é o ano atual - XXXX é uma sequencia com base no último de funcionário"""
    ano_atual = datetime.now().year
    repo = FuncionarioRepository()

    # Busca a última matrícula cadastrada
    funcionarios = repo.listar_funcionarios()
    ultima_matricula = None

    for func in funcionarios:
        if func.matricula.startswith(str(ano_atual)):
            ultima_matricula = func.matricula

    if ultima_matricula:
        sequencial = int(ultima_matricula[4:]) + 1
    else:
        sequencial = 1
    return f"{ano_atual}{sequencial:04d}"