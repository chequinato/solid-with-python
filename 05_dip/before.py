"""
DIP - Dependency Inversion Principle (ANTES)
Cenário: Sistema de e-commerce inspirado na Amazon

Problema: A classe ServicoDeCompra depende DIRETAMENTE de implementações
concretas (RepositorioMySQL, ServicoCorreios, GatewayStripe).
Se quiser trocar o banco de dados ou o gateway de pagamento,
precisa MODIFICAR a classe ServicoDeCompra.
"""


class RepositorioMySQL:
    """Implementação concreta de banco de dados MySQL."""

    def salvar_pedido(self, pedido: dict) -> int:
        pedido_id = 12345
        print(f"[MySQL] INSERT INTO pedidos VALUES ({pedido})")
        print(f"[MySQL] Pedido #{pedido_id} salvo no MySQL.")
        return pedido_id

    def buscar_produto(self, produto_id: int) -> dict:
        print(f"[MySQL] SELECT * FROM produtos WHERE id = {produto_id}")
        return {"id": produto_id, "nome": "Kindle Paperwhite", "preco": 499.90, "estoque": 10}

    def atualizar_estoque(self, produto_id: int, quantidade: int) -> None:
        print(f"[MySQL] UPDATE produtos SET estoque = estoque - {quantidade} WHERE id = {produto_id}")


class ServicoCorreios:
    """Implementação concreta de envio pelos Correios."""

    def calcular_frete(self, cep: str, peso: float) -> float:
        frete = 25.90
        print(f"[CORREIOS] Calculando frete para CEP {cep}, peso {peso}kg")
        print(f"[CORREIOS] Frete: R${frete:.2f}")
        return frete

    def criar_envio(self, endereco: str, pedido_id: int) -> str:
        codigo = "BR123456789CD"
        print(f"[CORREIOS] Envio criado para {endereco}")
        print(f"[CORREIOS] Código de rastreio: {codigo}")
        return codigo


class GatewayStripe:
    """Implementação concreta do gateway Stripe."""

    def cobrar(self, valor: float, metodo: str) -> bool:
        print(f"[STRIPE] Cobrando R${valor:.2f} via {metodo}")
        print(f"[STRIPE] Pagamento aprovado!")
        return True


class ServicoDeCompra:
    """Depende DIRETAMENTE de implementações concretas — viola DIP!"""

    def __init__(self):
        # Dependências CONCRETAS criadas internamente
        self.repositorio = RepositorioMySQL()       # Acoplado ao MySQL
        self.frete = ServicoCorreios()               # Acoplado aos Correios
        self.pagamento = GatewayStripe()             # Acoplado ao Stripe

    def realizar_compra(
        self,
        produto_id: int,
        quantidade: int,
        cep: str,
        metodo_pagamento: str,
    ) -> dict:
        # Busca o produto (MySQL direto)
        produto = self.repositorio.buscar_produto(produto_id)
        print(f"\nProduto: {produto['nome']} - R${produto['preco']:.2f}")

        if produto["estoque"] < quantidade:
            raise ValueError("Produto sem estoque!")

        # Calcula o frete (Correios direto)
        subtotal = produto["preco"] * quantidade
        frete = self.frete.calcular_frete(cep, peso=0.5)
        total = subtotal + frete

        print(f"\nSubtotal: R${subtotal:.2f}")
        print(f"Frete: R${frete:.2f}")
        print(f"Total: R${total:.2f}")

        # Cobra o pagamento (Stripe direto)
        sucesso = self.pagamento.cobrar(total, metodo_pagamento)
        if not sucesso:
            raise RuntimeError("Pagamento falhou!")

        # Salva o pedido (MySQL direto)
        pedido = {
            "produto": produto["nome"],
            "quantidade": quantidade,
            "total": total,
        }
        pedido_id = self.repositorio.salvar_pedido(pedido)
        self.repositorio.atualizar_estoque(produto_id, quantidade)

        # Cria o envio (Correios direto)
        codigo_rastreio = self.frete.criar_envio(f"CEP: {cep}", pedido_id)

        return {
            "pedido_id": pedido_id,
            "total": total,
            "rastreio": codigo_rastreio,
        }


if __name__ == "__main__":
    servico = ServicoDeCompra()

    resultado = servico.realizar_compra(
        produto_id=1,
        quantidade=1,
        cep="01310-100",
        metodo_pagamento="cartao_credito",
    )

    print(f"\n=== Compra finalizada ===")
    print(f"Pedido: #{resultado['pedido_id']}")
    print(f"Total: R${resultado['total']:.2f}")
    print(f"Rastreio: {resultado['rastreio']}")

    # Problemas:
    # - Quer trocar MySQL por PostgreSQL? Modifica ServicoDeCompra
    # - Quer trocar Correios por transportadora? Modifica ServicoDeCompra
    # - Quer trocar Stripe por PagSeguro? Modifica ServicoDeCompra
    # - Quer testar sem banco real? Impossível sem mock complexo
