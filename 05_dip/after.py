"""
DIP - Dependency Inversion Principle (DEPOIS)
Cenário: Sistema de e-commerce inspirado na Amazon

Solução: ServicoDeCompra depende de ABSTRAÇÕES (interfaces),
não de implementações concretas. As dependências são INJETADAS
pelo construtor, permitindo trocar implementações facilmente.
"""

from abc import ABC, abstractmethod


# === ABSTRAÇÕES (interfaces) ===

class RepositorioProduto(ABC):
    """Interface para acesso a dados de produtos."""

    @abstractmethod
    def buscar_produto(self, produto_id: int) -> dict:
        ...

    @abstractmethod
    def atualizar_estoque(self, produto_id: int, quantidade: int) -> None:
        ...


class RepositorioPedido(ABC):
    """Interface para persistência de pedidos."""

    @abstractmethod
    def salvar_pedido(self, pedido: dict) -> int:
        ...


class ServicoFrete(ABC):
    """Interface para cálculo e envio de frete."""

    @abstractmethod
    def calcular_frete(self, cep: str, peso: float) -> float:
        ...

    @abstractmethod
    def criar_envio(self, endereco: str, pedido_id: int) -> str:
        ...


class GatewayPagamento(ABC):
    """Interface para processamento de pagamentos."""

    @abstractmethod
    def cobrar(self, valor: float, metodo: str) -> bool:
        ...


# === IMPLEMENTAÇÕES CONCRETAS ===

class RepositorioProdutoMySQL(RepositorioProduto):
    def buscar_produto(self, produto_id: int) -> dict:
        print(f"[MySQL] SELECT * FROM produtos WHERE id = {produto_id}")
        return {"id": produto_id, "nome": "Kindle Paperwhite", "preco": 499.90, "estoque": 10}

    def atualizar_estoque(self, produto_id: int, quantidade: int) -> None:
        print(f"[MySQL] UPDATE produtos SET estoque = estoque - {quantidade} WHERE id = {produto_id}")


class RepositorioPedidoMySQL(RepositorioPedido):
    def salvar_pedido(self, pedido: dict) -> int:
        pedido_id = 12345
        print(f"[MySQL] INSERT INTO pedidos VALUES ({pedido})")
        return pedido_id


class RepositorioProdutoPostgreSQL(RepositorioProduto):
    """Implementação alternativa — troca sem modificar ServicoDeCompra!"""

    def buscar_produto(self, produto_id: int) -> dict:
        print(f"[PostgreSQL] SELECT * FROM produtos WHERE id = {produto_id}")
        return {"id": produto_id, "nome": "Kindle Paperwhite", "preco": 499.90, "estoque": 10}

    def atualizar_estoque(self, produto_id: int, quantidade: int) -> None:
        print(f"[PostgreSQL] UPDATE produtos SET estoque = estoque - {quantidade}")


class RepositorioPedidoPostgreSQL(RepositorioPedido):
    def salvar_pedido(self, pedido: dict) -> int:
        pedido_id = 67890
        print(f"[PostgreSQL] INSERT INTO pedidos VALUES ({pedido})")
        return pedido_id


class ServicoCorreios(ServicoFrete):
    def calcular_frete(self, cep: str, peso: float) -> float:
        frete = 25.90
        print(f"[CORREIOS] Frete para CEP {cep}: R${frete:.2f}")
        return frete

    def criar_envio(self, endereco: str, pedido_id: int) -> str:
        codigo = "BR123456789CD"
        print(f"[CORREIOS] Rastreio: {codigo}")
        return codigo


class ServicoTransportadora(ServicoFrete):
    """Transportadora alternativa — troca sem modificar ServicoDeCompra!"""

    def calcular_frete(self, cep: str, peso: float) -> float:
        frete = 18.50
        print(f"[TRANSPORTADORA] Frete para CEP {cep}: R${frete:.2f}")
        return frete

    def criar_envio(self, endereco: str, pedido_id: int) -> str:
        codigo = "TRANS-2025-ABC"
        print(f"[TRANSPORTADORA] Rastreio: {codigo}")
        return codigo


class GatewayStripe(GatewayPagamento):
    def cobrar(self, valor: float, metodo: str) -> bool:
        print(f"[STRIPE] Cobrando R${valor:.2f} via {metodo} - Aprovado!")
        return True


class GatewayPagSeguro(GatewayPagamento):
    """Gateway alternativo — troca sem modificar ServicoDeCompra!"""

    def cobrar(self, valor: float, metodo: str) -> bool:
        print(f"[PAGSEGURO] Cobrando R${valor:.2f} via {metodo} - Aprovado!")
        return True


# === SERVIÇO DE COMPRA (depende de abstrações) ===

class ServicoDeCompra:
    """Depende APENAS de abstrações — as implementações são INJETADAS."""

    def __init__(
        self,
        repo_produto: RepositorioProduto,
        repo_pedido: RepositorioPedido,
        servico_frete: ServicoFrete,
        gateway_pagamento: GatewayPagamento,
    ):
        self.repo_produto = repo_produto
        self.repo_pedido = repo_pedido
        self.servico_frete = servico_frete
        self.gateway_pagamento = gateway_pagamento

    def realizar_compra(
        self,
        produto_id: int,
        quantidade: int,
        cep: str,
        metodo_pagamento: str,
    ) -> dict:
        produto = self.repo_produto.buscar_produto(produto_id)
        print(f"\nProduto: {produto['nome']} - R${produto['preco']:.2f}")

        if produto["estoque"] < quantidade:
            raise ValueError("Produto sem estoque!")

        subtotal = produto["preco"] * quantidade
        frete = self.servico_frete.calcular_frete(cep, peso=0.5)
        total = subtotal + frete

        print(f"\nSubtotal: R${subtotal:.2f} | Frete: R${frete:.2f} | Total: R${total:.2f}")

        sucesso = self.gateway_pagamento.cobrar(total, metodo_pagamento)
        if not sucesso:
            raise RuntimeError("Pagamento falhou!")

        pedido = {"produto": produto["nome"], "quantidade": quantidade, "total": total}
        pedido_id = self.repo_pedido.salvar_pedido(pedido)
        self.repo_produto.atualizar_estoque(produto_id, quantidade)

        codigo_rastreio = self.servico_frete.criar_envio(f"CEP: {cep}", pedido_id)

        return {"pedido_id": pedido_id, "total": total, "rastreio": codigo_rastreio}


if __name__ == "__main__":
    # Configuração 1: MySQL + Correios + Stripe
    print("=" * 50)
    print("COMPRA 1: MySQL + Correios + Stripe")
    print("=" * 50)

    servico_v1 = ServicoDeCompra(
        repo_produto=RepositorioProdutoMySQL(),
        repo_pedido=RepositorioPedidoMySQL(),
        servico_frete=ServicoCorreios(),
        gateway_pagamento=GatewayStripe(),
    )
    resultado1 = servico_v1.realizar_compra(1, 1, "01310-100", "cartao_credito")
    print(f"\nPedido #{resultado1['pedido_id']} | R${resultado1['total']:.2f} | {resultado1['rastreio']}")

    # Configuração 2: PostgreSQL + Transportadora + PagSeguro
    # ServicoDeCompra NÃO foi modificado! Só trocamos as dependências.
    print(f"\n{'=' * 50}")
    print("COMPRA 2: PostgreSQL + Transportadora + PagSeguro")
    print("=" * 50)

    servico_v2 = ServicoDeCompra(
        repo_produto=RepositorioProdutoPostgreSQL(),
        repo_pedido=RepositorioPedidoPostgreSQL(),
        servico_frete=ServicoTransportadora(),
        gateway_pagamento=GatewayPagSeguro(),
    )
    resultado2 = servico_v2.realizar_compra(1, 1, "04538-132", "pix")
    print(f"\nPedido #{resultado2['pedido_id']} | R${resultado2['total']:.2f} | {resultado2['rastreio']}")
