from typing import Dict
from security.auth import Autenticador
from utils.logger import registrar_log

class UserService:
    """Serviço dedicado ao gerenciamento de usuários do sistema"""

    def __init__(self, auth: Autenticador, usuario_logado: Dict):
        self.auth = auth
        self.usuario = usuario_logado  # Usuário atualmente logado

    def adicionar_usuario(self, novo_user: str, senha: str, nivel: str) -> bool:
        """Adiciona um novo usuário (apenas para administradores)"""
        if self.usuario['nivel'] != 'admin':
            registrar_log("TENTATIVA DE ACESSO NÃO AUTORIZADO", self.usuario['username'], "Adicionar usuário")
            return False

        success = self.auth.adicionar_usuario(self.usuario, novo_user, senha, nivel)
        if success:
            registrar_log("USUÁRIO ADICIONADO", self.usuario['username'], f"Novo usuário: {novo_user}")
        return success

    def listar_usuarios(self) -> None:
        """Lista todos os usuários (apenas para administradores)"""
        if self.usuario['nivel'] != 'admin':
            registrar_log("TENTATIVA DE ACESSO NÃO AUTORIZADO", self.usuario['username'], "Listar usuários")
            print("❌ Acesso restrito a administradores!")
            return

        print("\n--- USUÁRIOS CADASTRADOS ---")
        for username, dados in self.auth.usuarios.items():
            print(f"Usuário: {username} | Nível: {dados['nivel']} | Nome: {dados['nome']}")

    def menu_gerenciamento(self):
        """Interface interativa para gerenciamento de usuários"""
        while True:
            print("\n--- GERENCIAMENTO DE USUÁRIOS ---")
            print("1. Adicionar usuário")
            print("2. Listar usuários")
            print("3. Voltar")

            opcao = input("Escolha: ").strip()

            if opcao == "1":
                novo_user = input("Novo usuário: ").strip()
                senha = input("Senha: ").strip()
                nivel = input("Nível (admin/user): ").strip().lower()

                if nivel not in ('admin', 'user'):
                    print("❌ Nível inválido! Use 'admin' ou 'user'")
                    continue

                if self.adicionar_usuario(novo_user, senha, nivel):
                    print("✅ Usuário adicionado com sucesso!")
                else:
                    print("❌ Falha ao adicionar usuário!")

            elif opcao == "2":
                self.listar_usuarios()

            elif opcao == "3":
                break

            else:
                print("❌ Opção inválida!")