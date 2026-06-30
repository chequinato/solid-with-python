"""
OCP - Open/Closed Principle (DEPOIS)
Cenário: Gateway de pagamento inspirado no Stripe

Solução: Usamos uma classe abstrata MetodoPagamento. Para adicionar
um novo meio de pagamento, basta criar uma nova classe — sem modificar
nenhum código existente.
"""

from abc import ABC, abstractmethod


class MetodoPagamento(ABC):
    """Classe abstrata que define o contrato para meios de pagamento."""

    @abstractmethod
    def processar(self, valor: float, dados: dict) -> None:
        """Processa o pagamento."""
        ...

    @abstractmethod
    def nome(self) -> str:
        """Retorna o nome do meio de pagamento."""
        ...


class PagamentoCartaoCredito(MetodoPagamento):
    def nome(self) -> str:
        return "Cartão de Crédito"

    def processar(self, valor: float, dados: dict) -> None:
        numero = dados.get("numero", "****")
        parcelas = dados.get("parcelas", 1)
        valor_parcela = valor / parcelas
        print(f"[CARTAO] Cobrando R${valor:.2f} no cartão {numero[-4:]}")
        print(f"[CARTAO] {parcelas}x de R${valor_parcela:.2f}")
        print(f"[CARTAO] Pagamento aprovado!")


class PagamentoPix(MetodoPagamento):
    DESCONTO = 0.05

    def nome(self) -> str:
        return "PIX"

    def processar(self, valor: float, dados: dict) -> None:
        chave = dados.get("chave_pix", "N/A")
        desconto = valor * self.DESCONTO
        valor_final = valor - desconto
        print(f"[PIX] Gerando QR Code para chave: {chave}")
        print(f"[PIX] Valor original: R${valor:.2f}")
        print(f"[PIX] Desconto PIX ({self.DESCONTO:.0%}): -R${desconto:.2f}")
        print(f"[PIX] Valor final: R${valor_final:.2f}")
        print(f"[PIX] Pagamento confirmado!")


class PagamentoBoleto(MetodoPagamento):
    def nome(self) -> str:
        return "Boleto"

    def processar(self, valor: float, dados: dict) -> None:
        vencimento = dados.get("vencimento", "3 dias úteis")
        codigo = "23793.38128 60000.000003 00000.000400 1 84340000012345"
        print(f"[BOLETO] Gerando boleto de R${valor:.2f}")
        print(f"[BOLETO] Vencimento: {vencimento}")
        print(f"[BOLETO] Código de barras: {codigo}")
        print(f"[BOLETO] Boleto gerado com sucesso!")


class PagamentoApplePay(MetodoPagamento):
    """Novo meio de pagamento — sem modificar NADA no código existente!"""

    def nome(self) -> str:
        return "Apple Pay"

    def processar(self, valor: float, dados: dict) -> None:
        device = dados.get("device_id", "iPhone")
        print(f"[APPLE PAY] Autenticando via Face ID no {device}...")
        print(f"[APPLE PAY] Cobrando R${valor:.2f}")
        print(f"[APPLE PAY] Pagamento aprovado via Apple Pay!")


class ProcessadorPagamento:
    """Processa pagamentos usando qualquer MetodoPagamento.
    Não precisa ser modificado quando novos meios de pagamento são criados."""

    def processar(self, metodo: MetodoPagamento, valor: float, dados: dict) -> None:
        print(f"Processando pagamento via {metodo.nome()}...")
        metodo.processar(valor, dados)
        print(f"Transação finalizada.\n")


if __name__ == "__main__":
    processador = ProcessadorPagamento()

    print("=== Pagamento com Cartão ===")
    processador.processar(PagamentoCartaoCredito(), 299.90, {
        "numero": "4111111111111111",
        "parcelas": 3,
    })

    print("=== Pagamento com PIX ===")
    processador.processar(PagamentoPix(), 299.90, {
        "chave_pix": "joao@email.com",
    })

    print("=== Pagamento com Boleto ===")
    processador.processar(PagamentoBoleto(), 299.90, {
        "vencimento": "15/07/2025",
    })

    # Apple Pay adicionado SEM modificar o ProcessadorPagamento!
    print("=== Pagamento com Apple Pay ===")
    processador.processar(PagamentoApplePay(), 299.90, {
        "device_id": "iPhone 15 Pro",
    })
