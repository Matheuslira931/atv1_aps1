import random
from datetime import datetime, timedelta


# Classes de Usuário e Subclasses
class Usuario:
    def __init__(self, nome, email, papel):
        self.nome = nome
        self.email = email
        self.papel = papel


class Desenvolvedor(Usuario):
    def __init__(self, nome, email):
        super().__init__(nome, email, "Desenvolvedor")


class ScrumMaster(Usuario):
    def __init__(self, nome, email):
        super().__init__(nome, email, "Scrum Master")


class ProductOwner(Usuario):
    def __init__(self, nome, email):
        super().__init__(nome, email, "Product Owner")


# Classe Tarefa
class Tarefa:
    def __init__(self, descricao, estimativa_horas):
        self.descricao = descricao
        self.status = "Pendente"
        self.responsavel = None
        self.estimativa_horas = estimativa_horas  # Estimativa de horas para completar a tarefa
        self.horas_trabalhadas = 0  # Horas trabalhadas na tarefa

    def atribuir_responsavel(self, usuario):
        self.responsavel = usuario

    def atualizar_status(self, status):
        self.status = status

    def registrar_trabalho(self, horas):
        self.horas_trabalhadas += horas
        if self.horas_trabalhadas >= self.estimativa_horas:
            self.atualizar_status("Concluído")


# Classe Backlog
class Backlog:
    def __init__(self):
        self.tarefas = []

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    def remover_tarefa(self, tarefa):
        self.tarefas.remove(tarefa)

    def exibir_tarefas_pendentes(self):
        print("\nBacklog de Tarefas Pendente:")
        for tarefa in self.tarefas:
            if tarefa.status == "Pendente":
                print(f"Tarefa: {tarefa.descricao}, Estimativa: {tarefa.estimativa_horas}h")


# Classe Sprint
class Sprint:
    def __init__(self, numero, duracao_dias, scrum_master, product_owner):
        self.numero = numero
        self.tarefas = []
        self.scrum_master = scrum_master
        self.product_owner = product_owner
        self.data_inicio = datetime.now()
        self.data_fim = self.data_inicio + timedelta(days=duracao_dias)
        self.duracao_dias = duracao_dias

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    def tempo_restante(self):
        dias_restantes = (self.data_fim - datetime.now()).days
        return dias_restantes if dias_restantes > 0 else 0


# Classe Projeto
class Projeto:
    def __init__(self, nome):
        self.nome = nome
        self.sprints = []
        self.membros = []
        self.backlog = Backlog()

    def criar_sprint(self, numero, duracao_dias, scrum_master, product_owner):
        sprint = Sprint(numero, duracao_dias, scrum_master, product_owner)
        self.sprints.append(sprint)
        return sprint

    def adicionar_membro(self, usuario):
        self.membros.append(usuario)

    def gerar_relatorio_progresso(self):
        print(f"\nRelatório de Progresso do Projeto: {self.nome}")
        for sprint in self.sprints:
            print(f"\nSprint {sprint.numero} (Fim em {sprint.data_fim.strftime('%d/%m/%Y')}):")
            print(f"Scrum Master: {sprint.scrum_master.nome} | Product Owner: {sprint.product_owner.nome}")
            for tarefa in sprint.tarefas:
                status = f"{tarefa.status} (Responsável: {tarefa.responsavel.nome})" if tarefa.responsavel else "Não atribuído"
                print(
                    f"Tarefa: {tarefa.descricao} - Status: {status} - Horas trabalhadas: {tarefa.horas_trabalhadas}/{tarefa.estimativa_horas}")

        self.backlog.exibir_tarefas_pendentes()


# Função para distribuir tarefas e atualizar status
def distribuir_tarefas_e_atualizar_status(projeto, tarefas_por_sprint):
    membros_desenvolvedores = [m for m in projeto.membros if isinstance(m, Desenvolvedor)]

    for sprint in projeto.sprints:
        tarefas = tarefas_por_sprint[sprint.numero - 1]
        for tarefa in tarefas:
            # Atribuir uma tarefa a um desenvolvedor aleatório
            responsavel = random.choice(membros_desenvolvedores)
            tarefa.atribuir_responsavel(responsavel)

            # Distribuir status variado para as tarefas
            status_opcoes = ["Pendente", "Em progresso", "Concluído"]
            status_atualizado = random.choices(status_opcoes, weights=[2, 3, 1], k=1)[
                0]  # Mais chance de "Em progresso"
            tarefa.atualizar_status(status_atualizado)

            # Registrar horas aleatórias de trabalho, mas só para as tarefas em progresso ou concluídas
            if status_atualizado != "Pendente":
                horas_trabalhadas = random.randint(0, tarefa.estimativa_horas)
                tarefa.registrar_trabalho(horas_trabalhadas)


# Simulação do projeto
def simular_projeto_scrum():
    # Criar o projeto
    projeto = Projeto("Sistema de Gerenciamento de Projetos Ágeis")

    # Criar membros da equipe
    desenvolvedor1 = Desenvolvedor("Alice", "alice@empresa.com")
    desenvolvedor2 = Desenvolvedor("Bob", "bob@empresa.com")
    desenvolvedor3 = Desenvolvedor("Charlie", "charlie@empresa.com")
    scrum_master = ScrumMaster("Carlos", "carlos@empresa.com")
    product_owner = ProductOwner("Lucas", "lucas@empresa.com")

    # Adicionar membros ao projeto
    projeto.adicionar_membro(desenvolvedor1)
    projeto.adicionar_membro(desenvolvedor2)
    projeto.adicionar_membro(desenvolvedor3)
    projeto.adicionar_membro(scrum_master)
    projeto.adicionar_membro(product_owner)

    # Adicionar tarefas ao backlog
    todas_tarefas = [
        Tarefa(f"Desenvolver funcionalidade {i}", random.randint(5, 20)) for i in range(1, 21)
    ]
    for tarefa in todas_tarefas:
        projeto.backlog.adicionar_tarefa(tarefa)

    # Criar sprints e distribuir tarefas
    sprint1 = projeto.criar_sprint(1, 14, scrum_master, product_owner)  # Sprint de 14 dias
    sprint2 = projeto.criar_sprint(2, 14, scrum_master, product_owner)  # Sprint de 14 dias
    sprint3 = projeto.criar_sprint(3, 14, scrum_master, product_owner)  # Sprint de 14 dias

    # Distribuir tarefas entre os sprints
    tarefas_por_sprint = [
        todas_tarefas[0:7],  # Sprint 1: 7 tarefas
        todas_tarefas[7:14],  # Sprint 2: 7 tarefas
        todas_tarefas[14:20]  # Sprint 3: 6 tarefas
    ]

    # Remover tarefas do backlog ao serem adicionadas às sprints
    for sprint, tarefas in zip(projeto.sprints, tarefas_por_sprint):
        for tarefa in tarefas:
            sprint.adicionar_tarefa(tarefa)
            projeto.backlog.remover_tarefa(tarefa)

    # Distribuir tarefas e atualizar status com maior variação
    distribuir_tarefas_e_atualizar_status(projeto, tarefas_por_sprint)

    # Gerar relatório de progresso
    projeto.gerar_relatorio_progresso()


# Executar a simulação do projeto Scrum
simular_projeto_scrum()
