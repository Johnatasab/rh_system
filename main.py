import os
import sys
from datetime import datetime, date
from typing import Optional, Dict, List

# Importações dos nossos módulos
from models.funcionario import Funcionario
from services.rh_service import RHService
from services.cep_service import CEPService
from services.ferias_service import FeriasService, StatusFerias
from utils.matricula import gerar_matricula
from database.json_repository import FuncionarioRepository
from utils.validadores import ValidadorDocumentos, ValidadorEmail


class SistemaRH:
    def __init__(self):
        self.rh_service = RHService()
        self.ferias_service = FeriasService()

    def limpar_tela(self):
        """Limpa a tela do console."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_menu_principal(self):
        """Exibe o menu principal do sistema."""
        self.limpar_tela()
        print("=" * 50)
        print(f"{'SISTEMA DE RECURSOS HUMANOS':^50}")
        print("=" * 50)
        print("\nMENU PRINCIPAL:\n")
        print("1. Cadastrar novo funcionário")
        print("2. Consultar funcionário")
        print("3. Editar dados de funcionário")
        print("4. Remover funcionário")
        print("5. Gerenciar férias")
        print("9. Sair do sistema")
        print("\n" + "=" * 50)

    def aguardar_enter(self):
        """Pausa a execução até que o usuário pressione Enter."""
        input("\nPressione Enter para continuar...")

    def formatar_data(self, data: date) -> str:
        """Formata uma data para o padrão brasileiro."""
        return data.strftime("%d/%m/%Y")

    def ler_data(self, prompt: str) -> date:
        """Lê uma data do usuário no formato DD/MM/AAAA."""
        while True:
            try:
                data_str = input(prompt).strip()
                dia, mes, ano = map(int, data_str.split('/'))
                return date(ano, mes, dia)
            except (ValueError, AttributeError):
                print("Data inválida! Use o formato DD/MM/AAAA.")

    def cadastrar_funcionario(self):
        """Interface para cadastro de novo funcionário."""
        self.limpar_tela()
        print("=" * 50)
        print("CADASTRO DE NOVO FUNCIONÁRIO".center(50))
        print("=" * 50)

        try:
            # Dados pessoais
            print("\nDADOS PESSOAIS")
            nome = input("Nome completo: ").strip()

            while True:
                cpf = input("CPF (somente números): ").strip()
                try:
                    if ValidadorDocumentos.validar_cpf(cpf):
                        break
                    print("CPF inválido! Digite novamente.")
                except ValueError as e:
                    print(f"Erro {str(e)}")

            rg = input("RG: ").strip()

            print("\nData de nascimento (DD/MM/AAAA): ")
            dia = int(input("Dia: "))
            mes = int(input("Mês: "))
            ano = int(input("Ano: "))
            data_nascimento = date(ano, mes, dia)

            genero = input("Gênero: ").strip()
            estado_civil = input("Estado civil: ").strip()

            # Contatos
            print("\nDADOS DE CONTATO")
            while True:
                email = input("E-mail: ").strip()
                try:
                    if ValidadorEmail.validar_email(email):
                        break
                    print("E-mail inválido! Formato esperado: nome@dominio.com")
                except ValueError as e:
                    print(f"Erro {str(e)}")

            telefone = input("Telefone (opcional): ").strip() or None
            celular = input("Celular (opcional): ").strip() or None

            # Endereço
            print("\nENDEREÇO")
            while True:
                cep = input("CEP (digite 'sair' para pular): ").strip()
                if cep.lower() == 'sair':
                    break
                try:
                    dados_cep = CEPService.consultar_cep(cep)
                    if dados_cep:
                        print("\nEndereço encontrado:")
                        print(f"Logradouro: {dados_cep['logradouro']}")
                        print(f"Bairro: {dados_cep['bairro']}")
                        print(f"Cidade/UF: {dados_cep['localidade']}/{dados_cep['uf']}")

                        # Solicitar confirmação de endereço
                        confirmacao = input("\nUsar este endereço? (S/N): ").strip().upper()
                        if confirmacao == 'S':
                            endereco = dados_cep['logradouro']
                            bairro = dados_cep['bairro']
                            cidade = dados_cep['localidade']
                            estado = dados_cep['uf']
                            complemento = dados_cep.get('complemento', '')
                            print("Endereço auto-preenchido com sucesso!")
                            break
                        else:
                            print("CEP não encontrado. Preencha manualmente")
                            break
                except Exception as e:
                    print(f"Erro ao consultar CEP: {str(e)}")
                    continue

            # Se não encontrou CEP ou usuário escolheu plura, pede manualmente
            if not dados_cep or confirmacao != 'S':
                endereco = input("Endereço: ").strip()
                numero = input("Número: ").strip()
                complemento = input("Complemento (opcional): ").strip() or None
                bairro = input("Bairro: ").strip()
                cidade = input("Cidade: ").strip()
                estado = input("Estado (sigla): ").strip().upper()

            # Dados profissionais
            print("\nDADOS PROFISSIONAIS")
            cargo = input("Cargo: ").strip()
            departamento = input("Departamento: ").strip()

            print("\nData de admissão (DD/MM/AAAA): ")
            dia = int(input("Dia: "))
            mes = int(input("Mês: "))
            ano = int(input("Ano: "))
            data_admissao = date(ano, mes, dia)

            tipo_contrato = input("Tipo de contrato: ").strip()
            jornada_trabalho = input("Jornada de trabalho: ").strip()
            salario = float(input("Salário (R$): ").replace(",", "."))

            # Dados bancários
            print("\nDADOS BANCÁRIOS")
            banco = input("Banco: ").strip()
            agencia = input("Agência: ").strip()
            conta = input("Conta: ").strip()
            tipo_conta = input("Tipo de conta: ").strip()

            # Cadastra o funcionário
            novo_funcionario = self.rh_service.cadastrar_funcionario(
                nome=nome, cpf=cpf, rg=rg, data_nascimento=data_nascimento,
                genero=genero, estado_civil=estado_civil, email=email,
                telefone=telefone, celular=celular, cep=cep, endereco=endereco,
                numero=numero, complemento=complemento, bairro=bairro,
                cidade=cidade, estado=estado, cargo=cargo, departamento=departamento,
                data_admissao=data_admissao, tipo_contrato=tipo_contrato,
                jornada_trabalho=jornada_trabalho, salario=salario, banco=banco,
                agencia=agencia, conta=conta, tipo_conta=tipo_conta
            )

            print(f"\n✅ Funcionário cadastrado com sucesso! Matrícula: {novo_funcionario.matricula}")

        except ValueError as e:
            print(f"\n❌ Erro ao cadastrar: {str(e)}")
        except Exception as e:
            print("\n❌ Ocorreu um erro inesperado durante o cadastro")

        self.aguardar_enter()

    def consultar_funcionario(self):
        """Menu de consulta de funcionários."""
        while True:
            self.limpar_tela()
            print("=" * 50)
            print("CONSULTAR FUNCIONÁRIO".center(50))
            print("=" * 50)
            print("\nOPÇÕES DE CONSULTA:\n")
            print("1. Por matrícula")
            print("2. Por nome")
            print("3. Por CPF")
            print("4. Listar todos")
            print("9. Voltar ao menu principal")
            print("\n" + "=" * 50)

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                self.consultar_por_matricula()
            elif opcao == "2":
                self.consultar_por_nome()
            elif opcao == "3":
                self.consultar_por_cpf()
            elif opcao == "4":
                self.listar_todos_funcionarios()
            elif opcao == "9":
                break
            else:
                print("\n❌ Opção inválida!")

        print("\n❌ Ocorreu um erro durante a consulta")
        self.aguardar_enter()

    def consultar_por_matricula(self):
        """Consulta um funcionário por matrícula."""
        self.limpar_tela()
        print("=" * 50)
        print("CONSULTAR POR MATRÍCULA".center(50))
        print("=" * 50)

        matricula = input("\nDigite a matrícula: ").strip()
        funcionario = self.rh_service.buscar_por_matricula(matricula)

        if funcionario:
            self.exibir_detalhes_funcionario(funcionario)
        else:
            print("\n❌ Funcionário não encontrado!")

        self.aguardar_enter()

    def consultar_por_nome(self):
        """Consulta funcionários por parte do nome."""
        self.limpar_tela()
        print("=" * 50)
        print("CONSULTAR POR NOME".center(50))
        print("=" * 50)

        nome = input("\nDigite parte do nome: ").strip()
        funcionarios = self.rh_service.buscar_por_nome(nome)

        if funcionarios:
            print("\nRESULTADOS DA BUSCA:")
            for func in funcionarios:
                print(f"{func.matricula} - {func.nome} ({func.cargo})")

            print("\nDigite a matrícula para ver detalhes ou deixe em branco para voltar")
            matricula = input("Matrícula: ").strip()

            if matricula:
                funcionario = self.rh_service.buscar_por_matricula(matricula)
                if funcionario:
                    self.exibir_detalhes_funcionario(funcionario)
        else:
            print("\n❌ Nenhum funcionário encontrado!")

        self.aguardar_enter()

    def consultar_por_cpf(self):
        """Consulta funcionário por cpf."""
        self.limpar_tela()
        print("=" * 50)
        print("CONSULTA POR CPF".center(50))
        print("=" * 50)

        cpf = input("\nDigite o cpf (somente números): ").strip()
        funcionarios = self.rh_service.buscar_por_cpf(cpf)

        if funcionarios:
            print("\nRESULTADO DA BUSCA:")
            for func in funcionarios:
                print(f"{func.matricula} - {func.nome} ({func.cargo})")
            print("\nDigite a matrícula para ver detalhes ou deixe em branco para voltar")
            matricula = input("Matrícula: ").strip()

            if matricula:
                funcionario = self.rh_service.buscar_por_matricula(matricula)
                if funcionario:
                    self.exibir_detalhes_funcionario(funcionario)

        else:
            print("\n Nenhum funcionário encontrado!")

        self.aguardar_enter()

    def listar_todos_funcionarios(self):
        """Lista todos os funcionários ativos."""
        self.limpar_tela()
        print("=" * 50)
        print("LISTA DE FUNCIONÁRIOS".center(50))
        print("=" * 50)

        funcionarios = self.rh_service.listar_funcionarios()

        if not funcionarios:
            print("\nNenhum funcionário cadastrado.")
        else:
            print("\nMATRÍCULA - NOME (CARGO)")
            print("-" * 50)
            for func in funcionarios:
                print(f"{func.matricula} - {func.nome} ({func.cargo})")

        self.aguardar_enter()

    def exibir_detalhes_funcionario(self, funcionario: Funcionario):
        """Exibe todos os detalhes de um funcionário."""
        print("\nDETALHES DO FUNCIONÁRIO")
        print("-" * 50)
        print(f"Matrícula: {funcionario.matricula}")
        print(f"Nome: {funcionario.nome}")
        print(f"CPF: {funcionario.cpf}")
        print(f"RG: {funcionario.rg}")
        print(f"Data Nasc.: {self.formatar_data(funcionario.data_nascimento)}")
        print(f"Gênero: {funcionario.genero}")
        print(f"Estado Civil: {funcionario.estado_civil}")
        print(f"E-mail: {funcionario.email}")
        print(f"Telefone: {funcionario.telefone or 'Não informado'}")
        print(f"Celular: {funcionario.celular or 'Não informado'}")
        print(f"Endereço: {funcionario.endereco}, {funcionario.numero}")
        print(f"Complemento: {funcionario.complemento or 'Não informado'}")
        print(f"Bairro: {funcionario.bairro}")
        print(f"Cidade: {funcionario.cidade}/{funcionario.estado}")
        print(f"CEP: {funcionario.cep}")
        print(f"Cargo: {funcionario.cargo}")
        print(f"Departamento: {funcionario.departamento}")
        print(f"Admissão: {self.formatar_data(funcionario.data_admissao)}")
        print(f"Contrato: {funcionario.tipo_contrato}")
        print(f"Jornada: {funcionario.jornada_trabalho}")
        print(f"Salário: R$ {funcionario.salario:.2f}")
        print(f"Banco: {funcionario.banco}")
        print(f"Agência: {funcionario.agencia}")
        print(f"Conta: {funcionario.conta} ({funcionario.tipo_conta})")
        print(f"Status: {'Ativo' if funcionario.ativo else 'Inativo'}")
        print("-" * 50)

    def editar_funcionario(self):
        """Interface para edição de dados de funcionário."""
        self.limpar_tela()
        print("=" * 50)
        print("EDITAR DADOS DE FUNCIONÁRIO".center(50))
        print("=" * 50)

        matricula = input("\nDigite a matrícula do funcionário: ").strip()
        funcionario = self.rh_service.buscar_por_matricula(matricula)

        if not funcionario:
            print("\n❌ Funcionário não encontrado!")
            self.aguardar_enter()
            return

        self.exibir_detalhes_funcionario(funcionario)

        print("\nSelecione o que deseja editar:")
        print("1. Dados de contato")
        print("2. Endereço")
        print("3. Dados profissionais")
        print("4. Dados bancários")
        print("5. Cancelar")

        opcao = input("\nEscolha uma opção: ").strip()

        dados_atualizados = {}

        if opcao == "1":
            print("\nATUALIZAR DADOS DE CONTATO")
            dados_atualizados['email'] = input(f"E-mail [{funcionario.email}]: ").strip() or funcionario.email
            dados_atualizados['telefone'] = input(f"Telefone [{funcionario.telefone or ''}]: ").strip() or None
            dados_atualizados['celular'] = input(f"Celular [{funcionario.celular or ''}]: ").strip() or None
            dados_atualizados['estado_civil'] = input(
                f"Estado Civil [{funcionario.estado_civil}]: ").strip() or funcionario.estado_civil

        elif opcao == "2":
            print("\nATUALIZAR ENDEREÇO")
            dados_atualizados['cep'] = input(f"CEP [{funcionario.cep}]: ").strip() or funcionario.cep
            dados_atualizados['endereco'] = input(
                f"Endereço [{funcionario.endereco}]: ").strip() or funcionario.endereco
            dados_atualizados['numero'] = input(f"Número [{funcionario.numero}]: ").strip() or funcionario.numero
            dados_atualizados['complemento'] = input(f"Complemento [{funcionario.complemento or ''}]: ").strip() or None
            dados_atualizados['bairro'] = input(f"Bairro [{funcionario.bairro}]: ").strip() or funcionario.bairro
            dados_atualizados['cidade'] = input(f"Cidade [{funcionario.cidade}]: ").strip() or funcionario.cidade
            dados_atualizados['estado'] = input(f"Estado [{funcionario.estado}]: ").strip() or funcionario.estado

        elif opcao == "3":
            print("\nATUALIZAR DADOS PROFISSIONAIS")
            dados_atualizados['cargo'] = input(f"Cargo [{funcionario.cargo}]: ").strip() or funcionario.cargo
            dados_atualizados['departamento'] = input(
                f"Departamento [{funcionario.departamento}]: ").strip() or funcionario.departamento
            dados_atualizados['salario'] = float(
                input(f"Salário [R$ {funcionario.salario:.2f}]: ").strip() or str(funcionario.salario))
            dados_atualizados['tipo_contrato'] = input(
                f"Tipo de Contrato [{funcionario.tipo_contrato}]: ").strip() or funcionario.tipo_contrato
            dados_atualizados['jornada_trabalho'] = input(
                f"Jornada [{funcionario.jornada_trabalho}]: ").strip() or funcionario.jornada_trabalho

        elif opcao == "4":
            print("\nATUALIZAR DADOS BANCÁRIOS")
            dados_atualizados['banco'] = input(f"Banco [{funcionario.banco}]: ").strip() or funcionario.banco
            dados_atualizados['agencia'] = input(f"Agência [{funcionario.agencia}]: ").strip() or funcionario.agencia
            dados_atualizados['conta'] = input(f"Conta [{funcionario.conta}]: ").strip() or funcionario.conta
            dados_atualizados['tipo_conta'] = input(
                f"Tipo de Conta [{funcionario.tipo_conta}]: ").strip() or funcionario.tipo_conta

        elif opcao == "5":
            return
        else:
            print("\n❌ Opção inválida!")
            self.aguardar_enter()
            return

        try:
            funcionario_atualizado = self.rh_service.atualizar_funcionario(matricula, dados_atualizados)
            print("\n✅ Dados atualizados com sucesso!")
            self.exibir_detalhes_funcionario(funcionario_atualizado)
        except Exception as e:
            print(f"\n❌ Erro ao atualizar: {str(e)}")

        self.aguardar_enter()

    def remover_funcionario(self):
        """Interface para remoção de funcionário."""
        self.limpar_tela()
        print("=" * 50)
        print("REMOVER FUNCIONÁRIO".center(50))
        print("=" * 50)

        matricula = input("\nDigite a matrícula do funcionário: ").strip()

        # Verificar primeiro se o funcionário exixte
        funcionario = self.rh_service.buscar_por_matricula(matricula)
        if not funcionario:
            print("\n❌ Funcionário não encontrado!")
            self.aguardar_enter()
            return

        self.exibir_detalhes_funcionario(funcionario)

        # Confirmação de exclusão
        confirmacao = input("\nTem certeza que deseja REMOVER este funcionário? (S/N): ").strip().upper()

        if confirmacao == "S":
            if self.rh_service.remover_funcionario(matricula):
                print("\n✅ Funcionário removido com sucesso!")
            else:
                print("\n❌ Falha ao remover funcionário!")
        else:
            print("\nOperação cancelada.")

        self.aguardar_enter()

    def menu_ferias(self):
        """Menu de gerenciamento de férias."""
        while True:
            print("\nMENU DE FÉRIAS:\n")
            print("1. Agendar férias")
            print("2. Consultar férias por funcionário")
            print("3. Listar todas férias")
            print("4. Aprovar férias")
            print("5. Cancelar férias")
            print("6. Registrar férias gozadas")
            print("7. Remover agendamento")
            print("9. Voltar ao menu principal")
            print("\n" + "=" * 50)

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                self.agendar_ferias()
            elif opcao == "2":
                self.consultar_ferias_funcionario()
            elif opcao == "3":
                self.listar_todas_ferias()
            elif opcao == "4":
                self.aprovar_ferias()
            elif opcao == "5":
                self.cancelar_ferias()
            elif opcao == "6":
                self.registrar_ferias_gozadas()
            elif opcao == "7":
                self.remover_agendamento_ferias()
            elif opcao == "9":
                break
            else:
                print("\n❌ Ocorreu um erro no módulo de férias")
                self.aguardar_enter()

    def agendar_ferias(self):
        """Interface para agendamento de férias."""
        self.limpar_tela()
        print("=" * 50)
        print("AGENDAR FÉRIAS".center(50))
        print("=" * 50)
        matricula = input("\nMatrícula do funcionário: ").strip()
        funcionario = self.rh_service.buscar_por_matricula(matricula)

        if not funcionario:
            print("\n❌ Funcionário não encontrado!")
            self.aguardar_enter()
            return

        print(f"\nAgendando férias para: {funcionario.nome} ({funcionario.matricula})")

        print("\nData de início (DD/MM/AAAA):")
        data_inicio = self.ler_data("Data de início: ")

        print("\nData de término (DD/MM/AAAA):")
        data_fim = self.ler_data("Data de término: ")

        observacoes = input("\nObservações (opcional): ").strip() or None

        try:
            ferias = self.ferias_service.agendar_ferias(
                matricula_funcionario=matricula,
                data_inicio=data_inicio,
                data_fim=data_fim,
                observacoes=observacoes
            )
            print(f"\n✅ Férias agendadas com sucesso! ID: {ferias.id}")
        except ValueError as e:
            print(f"\n❌ Erro ao agendar férias: {str(e)}")

        self.aguardar_enter()

    def consultar_ferias_funcionario(self):
        """Consulta férias por matrícula de funcionário."""
        self.limpar_tela()
        print("=" * 50)
        print("CONSULTAR FÉRIAS POR FUNCIONÁRIO".center(50))
        print("=" * 50)

        matricula = input("\nMatrícula do funcionário: ").strip()
        funcionario = self.rh_service.buscar_por_matricula(matricula)

        if not funcionario:
            print("\n❌ Funcionário não encontrado!")
            self.aguardar_enter()
            return

        ferias_list = self.ferias_service.listar_ferias_por_matricula(matricula)

        if not ferias_list:
            print(f"\nNenhum período de férias encontrado para {funcionario.nome}")
        else:
            print(f"\nFÉRIAS DE {funcionario.nome.upper()} ({matricula}):\n")
            for ferias in ferias_list:
                print(f"ID: {ferias.id}")
                print(f"Período: {self.formatar_data(ferias.data_inicio)} a {self.formatar_data(ferias.data_fim)}")
                print(f"Dias: {ferias.dias_ferias} | Status: {ferias.status.value}")
                if ferias.observacoes:
                    print(f"Observações: {ferias.observacoes}")
                print("-" * 40)

        self.aguardar_enter()

    def listar_todas_ferias(self):
        """Lista todas as férias cadastradas."""
        self.limpar_tela()
        print("=" * 50)
        print("LISTA DE TODAS AS FÉRIAS".center(50))
        print("=" * 50)

        print("\nFiltrar por status:")
        print("1. Todas")
        print("2. Agendadas")
        print("3. Aprovadas")
        print("4. Canceladas")
        print("5. Gozadas")

        opcao = input("\nEscolha uma opção: ").strip()

        status_map = {
            "1": None,
            "2": StatusFerias.AGENDADA,
            "3": StatusFerias.APROVADA,
            "4": StatusFerias.CANCELADA,
            "5": StatusFerias.GOZADA
        }

        status = status_map.get(opcao)
        if status is None and opcao != "1":
            print("\n❌ Opção inválida!")
            self.aguardar_enter()
            return

        ferias_list = self.ferias_service.listar_todas_ferias(status)

        if not ferias_list:
            print("\nNenhum período de férias encontrado.")
        else:
            print("\nLISTA DE FÉRIAS:\n")
            for ferias in ferias_list:
                funcionario = self.rh_service.buscar_por_matricula(ferias.matricula_funcionario)
                nome_funcionario = funcionario.nome if funcionario else "Funcionário não encontrado"
                print(f"ID: {ferias.id}")
                print(f"Funcionário: {nome_funcionario} ({ferias.matricula_funcionario})")
                print(f"Período: {self.formatar_data(ferias.data_inicio)} a {self.formatar_data(ferias.data_fim)}")
                print(f"Dias: {ferias.dias_ferias} | Status: {ferias.status.value}")
                print("-" * 50)

        self.aguardar_enter()

    def aprovar_ferias(self):
        """Interface para aprovação de férias."""
        self.limpar_tela()
        print("=" * 50)
        print("APROVAR FÉRIAS".center(50))
        print("=" * 50)

        id_ferias = input("\nID do agendamento de férias: ").strip()
        ferias = self.ferias_service.buscar_ferias_por_id(id_ferias)

        if not ferias:
            print("\n❌ Agendamento não encontrado!")
            self.aguardar_enter()
            return

        funcionario = self.rh_service.buscar_por_matricula(ferias.matricula_funcionario)

        print("\nDETALHES DO AGENDAMENTO:")
        print(f"Funcionário: {funcionario.nome if funcionario else 'Não encontrado'}")
        print(f"Período: {self.formatar_data(ferias.data_inicio)} a {self.formatar_data(ferias.data_fim)}")
        print(f"Status atual: {ferias.status.value}")

        confirmacao = input("\nDeseja aprovar estas férias? (S/N): ").strip().upper()

        if confirmacao == "S":
            if self.ferias_service.aprovar_ferias(id_ferias):
                print("\n✅ Férias aprovadas com sucesso!")
            else:
                print("\n❌ Não foi possível aprovar estas férias (status inválido)")
        else:
            print("\nOperação cancelada.")

        self.aguardar_enter()

    def cancelar_ferias(self):
        """Interface para cancelamento de férias."""
        self.limpar_tela()
        print("=" * 50)
        print("CANCELAR FÉRIAS".center(50))
        print("=" * 50)

        id_ferias = input("\nID do agendamento de férias: ").strip()
        ferias = self.ferias_service.buscar_ferias_por_id(id_ferias)

        if not ferias:
            print("\n❌ Agendamento não encontrado!")
            self.aguardar_enter()
            return

        funcionario = self.rh_service.buscar_por_matricula(ferias.matricula_funcionario)

        print("\nDETALHES DO AGENDAMENTO:")
        print(f"Funcionário: {funcionario.nome if funcionario else 'Não encontrado'}")
        print(f"Período: {self.formatar_data(ferias.data_inicio)} a {self.formatar_data(ferias.data_fim)}")
        print(f"Status atual: {ferias.status.value}")

        confirmacao = input("\nDeseja cancelar estas férias? (S/N): ").strip().upper()

        if confirmacao == "S":
            if self.ferias_service.cancelar_ferias(id_ferias):
                print("\n✅ Férias canceladas com sucesso!")
            else:
                print("\n❌ Não foi possível cancelar estas férias (status inválido)")
        else:
            print("\nOperação cancelada.")

        self.aguardar_enter()

    def registrar_ferias_gozadas(self):
        """Interface para registrar férias gozadas."""
        self.limpar_tela()
        print("=" * 50)
        print("REGISTRAR FÉRIAS GOZADAS".center(50))
        print("=" * 50)

        id_ferias = input("\nID do agendamento de férias: ").strip()
        ferias = self.ferias_service.buscar_ferias_por_id(id_ferias)

        if not ferias:
            print("\n❌ Agendamento não encontrado!")
            self.aguardar_enter()
            return

        funcionario = self.rh_service.buscar_por_matricula(ferias.matricula_funcionario)

        print("\nDETALHES DO AGENDAMENTO:")
        print(f"Funcionário: {funcionario.nome if funcionario else 'Não encontrado'}")
        print(f"Período: {self.formatar_data(ferias.data_inicio)} a {self.formatar_data(ferias.data_fim)}")
        print(f"Status atual: {ferias.status.value}")

        confirmacao = input("\nDeseja registrar estas férias como gozadas? (S/N): ").strip().upper()

        if confirmacao == "S":
            if self.ferias_service.registrar_ferias_gozadas(id_ferias):
                print("\n✅ Férias registradas como gozadas com sucesso!")
            else:
                print("\n❌ Não foi possível registrar estas férias (status inválido)")
        else:
            print("\nOperação cancelada.")

        self.aguardar_enter()

    def remover_agendamento_ferias(self):
        """Interface para remoção de agendamento de férias."""
        self.limpar_tela()
        print("=" * 50)
        print("REMOVER AGENDAMENTO DE FÉRIAS".center(50))
        print("=" * 50)

        id_ferias = input("\nID do agendamento de férias: ").strip()
        ferias = self.ferias_service.buscar_ferias_por_id(id_ferias)

        if not ferias:
            print("\n❌ Agendamento não encontrado!")
            self.aguardar_enter()
            return

        funcionario = self.rh_service.buscar_por_matricula(ferias.matricula_funcionario)

        print("\nDETALHES DO AGENDAMENTO:")
        print(f"Funcionário: {funcionario.nome if funcionario else 'Não encontrado'}")
        print(f"Período: {self.formatar_data(ferias.data_inicio)} a {self.formatar_data(ferias.data_fim)}")
        print(f"Status: {ferias.status.value}")

        confirmacao = input("\nTem certeza que deseja REMOVER este agendamento? (S/N): ").strip().upper()

        if confirmacao == "S":
            if self.ferias_service.remover_ferias(id_ferias):
                print("\n✅ Agendamento removido com sucesso!")
            else:
                print("\n❌ Falha ao remover agendamento!")
        else:
            print("\nOperação cancelada.")

        self.aguardar_enter()

    def executar(self):
        """Loop principal do sistema."""
        while True:
            try:
                self.mostrar_menu_principal()
                opcao = input("\nEscolha uma opção: ").strip()

                if opcao == "1":
                    self.cadastrar_funcionario()
                elif opcao == "2":
                    self.consultar_funcionario()
                elif opcao == "3":
                    self.editar_funcionario()
                elif opcao == "4":
                    self.remover_funcionario()
                elif opcao == "5":
                    self.menu_ferias()
                elif opcao == "9":
                    print("\nSaindo do sistema...")
                    break
                else:
                    print("\n❌ Opção inválida!")
                    self.aguardar_enter()

            except KeyboardInterrupt:
                print("\nOperação cancelada pelo usuário")
                break
            except Exception as e:
                print("\n❌ Ocorreu um erro inesperado")
                self.aguardar_enter()


if __name__ == "__main__":
    sistema = SistemaRH()
    sistema.executar()