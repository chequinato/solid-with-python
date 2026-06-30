"""
SRP - Single Responsibility Principle (DEPOIS)
Cenário: Sistema de pedidos inspirado no iFood

Solução: Cada classe tem UMA única responsabilidade.
Se a regra de cálculo mudar, só mexemos em CalculadoraPedido.
Se o formato do e-mail mudar, só mexemos em NotificadorEmail.
"""

import json
from datetime import datetime


class Pedido:
    """Responsabilidade: representar os dados de um pedido."""

    def __init__(self, cliente: str, itens: list[dict]):
        self.cliente = cliente
        self.itens = itens
        self.data = datetime.now()
        self.status = "pendente"


class CalculadoraPedido:
    """Responsabilidade: calcular valores do pedido."""

    TAXA_ENTREGA = 5.99

    def calcular_total(self, pedido: Pedido) -> float:
        subtotal = sum(item["preco"] * item["qtd"] for item in pedido.itens)
        return subtotal + self.TAXA_ENTREGA

    def calcular_subtotal(self, pedido: Pedido) -> float:
        return sum(item["preco"] * item["qtd"] for item in pedido.itens)


class RepositorioPedido:
    """Responsabilidade: persistir o pedido no banco de dados."""

    def __init__(self, caminho_arquivo: str = "pedidos.json"):
        self.caminho_arquivo = caminho_arquivo

    def salvar(self, pedido: Pedido, total: float) -> None:
        dados = {
            "cliente": pedido.cliente,
            "itens": pedido.itens,
            "total": total,
            "data": pedido.data.isoformat(),
            "status": pedido.status,
        }
        with open(self.caminho_arquivo, "a") as f:
            f.write(json.dumps(dados) + "\n")
        print(f"[DB] Pedido de {pedido.cliente} salvo no banco de dados.")


class NotificadorEmail:
    """Responsabilidade: enviar notificações por e-mail."""

    def enviar_confirmacao(self, pedido: Pedido, total: float) -> None:
        print(f"[EMAIL] Para: {pedido.cliente}")
        print(f"[EMAIL] Assunto: Pedido confirmado!")
        print(f"[EMAIL] Corpo: Seu pedido de R${total:.2f} foi recebido.")
        print(f"[EMAIL] Status: {pedido.status}")


class GeradorNotaFiscal:
    """Responsabilidade: gerar nota fiscal."""

    def gerar(self, pedido: Pedido, total: float) -> str:
        nota = f"""
        ========= NOTA FISCAL =========
        Cliente: {pedido.cliente}
        Data: {pedido.data.strftime('%d/%m/%Y %H:%M')}
        --------------------------------
        """
        for item in pedido.itens:
            linha = f"        {item['nome']} x{item['qtd']} - R${item['preco'] * item['qtd']:.2f}"
            nota += linha + "\n"
        nota += f"""        --------------------------------
        Taxa de entrega: R$5.99
        TOTAL: R${total:.2f}
        ================================
        """
        print(nota)
        return nota


class ProcessadorPedido:
    """Responsabilidade: orquestrar o fluxo de processamento."""

    def __init__(self):
        self.calculadora = CalculadoraPedido()
        self.repositorio = RepositorioPedido()
        self.notificador = NotificadorEmail()
        self.gerador_nf = GeradorNotaFiscal()

    def processar(self, pedido: Pedido) -> None:
        pedido.status = "confirmado"
        total = self.calculadora.calcular_total(pedido)

        self.repositorio.salvar(pedido, total)
        self.notificador.enviar_confirmacao(pedido, total)
        self.gerador_nf.gerar(pedido, total)

        print(f"\nPedido de {pedido.cliente} processado com sucesso!")


if __name__ == "__main__":
    pedido = Pedido(
        cliente="João Silva",
        itens=[
            {"nome": "Pizza Margherita", "preco": 45.90, "qtd": 2},
            {"nome": "Refrigerante 2L", "preco": 12.00, "qtd": 1},
            {"nome": "Sobremesa Brownie", "preco": 18.50, "qtd": 1},
        ],
    )

    # Agora cada classe tem SUA responsabilidade
    processador = ProcessadorPedido()
    processador.processar(pedido)
