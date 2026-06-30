"""
SRP - Single Responsibility Principle (ANTES)
Cenário: Sistema de pedidos inspirado no iFood

Problema: A classe Pedido faz TUDO — calcula total, salva no banco,
envia e-mail e gera nota fiscal. Se qualquer uma dessas coisas mudar,
a classe inteira precisa ser alterada.
"""

import json
from datetime import datetime


class Pedido:
    def __init__(self, cliente: str, itens: list[dict]):
        self.cliente = cliente
        self.itens = itens  # [{"nome": "Pizza", "preco": 45.90, "qtd": 2}]
        self.data = datetime.now()
        self.status = "pendente"

    def calcular_total(self) -> float:
        """Calcula o total do pedido com taxa de entrega."""
        subtotal = sum(item["preco"] * item["qtd"] for item in self.itens)
        taxa_entrega = 5.99
        return subtotal + taxa_entrega

    def salvar_no_banco(self) -> None:
        """Salva o pedido no banco de dados (simulado com arquivo JSON)."""
        dados = {
            "cliente": self.cliente,
            "itens": self.itens,
            "total": self.calcular_total(),
            "data": self.data.isoformat(),
            "status": self.status,
        }
        with open("pedidos.json", "a") as f:
            f.write(json.dumps(dados) + "\n")
        print(f"[DB] Pedido de {self.cliente} salvo no banco de dados.")

    def enviar_email_confirmacao(self) -> None:
        """Envia e-mail de confirmação para o cliente."""
        total = self.calcular_total()
        print(f"[EMAIL] Para: {self.cliente}")
        print(f"[EMAIL] Assunto: Pedido confirmado!")
        print(f"[EMAIL] Corpo: Seu pedido de R${total:.2f} foi recebido.")
        print(f"[EMAIL] Status: {self.status}")

    def gerar_nota_fiscal(self) -> str:
        """Gera a nota fiscal do pedido."""
        total = self.calcular_total()
        nota = f"""
        ========= NOTA FISCAL =========
        Cliente: {self.cliente}
        Data: {self.data.strftime('%d/%m/%Y %H:%M')}
        --------------------------------
        """
        for item in self.itens:
            linha = f"        {item['nome']} x{item['qtd']} - R${item['preco'] * item['qtd']:.2f}"
            nota += linha + "\n"
        nota += f"""        --------------------------------
        Taxa de entrega: R$5.99
        TOTAL: R${total:.2f}
        ================================
        """
        print(nota)
        return nota

    def processar_pedido(self) -> None:
        """Processa o pedido completo — faz tudo em um lugar só."""
        self.status = "confirmado"
        self.salvar_no_banco()
        self.enviar_email_confirmacao()
        self.gerar_nota_fiscal()
        print(f"\nPedido de {self.cliente} processado com sucesso!")


if __name__ == "__main__":
    pedido = Pedido(
        cliente="João Silva",
        itens=[
            {"nome": "Pizza Margherita", "preco": 45.90, "qtd": 2},
            {"nome": "Refrigerante 2L", "preco": 12.00, "qtd": 1},
            {"nome": "Sobremesa Brownie", "preco": 18.50, "qtd": 1},
        ],
    )

    # A classe Pedido faz TUDO — isso viola o SRP
    pedido.processar_pedido()
