"""
OCP - Open/Closed Principle (ANTES)
Cenário: Gateway de pagamento inspirado no Stripe

Problema: Toda vez que um novo meio de pagamento é adicionado,
precisamos MODIFICAR a classe ProcessadorPagamento com mais um if/elif.
Isso viola o OCP — a classe deveria estar fechada para modificação.
"""


class ProcessadorPagamento:
    def processar(self, tipo: str, valor: float, dados: dict) -> None:
        """Processa o pagamento baseado no tipo."""
        if tipo == "cartao_credito":
            self._processar_cartao_credito(valor, dados)
        elif tipo == "pix":
            self._processar_pix(valor, dados)
        elif tipo == "boleto":
            self._processar_boleto(valor, dados)
        # Cada novo meio de pagamento = mais um elif aqui
        # elif tipo == "apple_pay": ...
        # elif tipo == "google_pay": ...
        # elif tipo == "paypal": ...
        else:
            raise ValueError(f"Tipo de pagamento '{tipo}' não suportado.")

    def _processar_cartao_credito(self, valor: float, dados: dict) -> None:
        numero = dados.get("numero", "****")
        parcelas = dados.get("parcelas", 1)
        valor_parcela = valor / parcelas
        print(f"[CARTAO] Cobrando R${valor:.2f} no cartão {numero[-4:]}")
        print(f"[CARTAO] {parcelas}x de R${valor_parcela:.2f}")
        print(f"[CARTAO] Pagamento aprovado!")

    def _processar_pix(self, valor: float, dados: dict) -> None:
        chave = dados.get("chave_pix", "N/A")
        desconto = valor * 0.05  # 5% de desconto no PIX
        valor_final = valor - desconto
        print(f"[PIX] Gerando QR Code para chave: {chave}")
        print(f"[PIX] Valor original: R${valor:.2f}")
        print(f"[PIX] Desconto PIX (5%): -R${desconto:.2f}")
        print(f"[PIX] Valor final: R${valor_final:.2f}")
        print(f"[PIX] Pagamento confirmado!")

    def _processar_boleto(self, valor: float, dados: dict) -> None:
        vencimento = dados.get("vencimento", "3 dias úteis")
        codigo = "23793.38128 60000.000003 00000.000400 1 84340000012345"
        print(f"[BOLETO] Gerando boleto de R${valor:.2f}")
        print(f"[BOLETO] Vencimento: {vencimento}")
        print(f"[BOLETO] Código de barras: {codigo}")
        print(f"[BOLETO] Boleto gerado com sucesso!")


if __name__ == "__main__":
    processador = ProcessadorPagamento()

    print("=== Pagamento com Cartão ===")
    processador.processar("cartao_credito", 299.90, {
        "numero": "4111111111111111",
        "parcelas": 3,
    })

    print("\n=== Pagamento com PIX ===")
    processador.processar("pix", 299.90, {
        "chave_pix": "joao@email.com",
    })

    print("\n=== Pagamento com Boleto ===")
    processador.processar("boleto", 299.90, {
        "vencimento": "15/07/2025",
    })

    # Se quiser adicionar Apple Pay, tem que MODIFICAR a classe
    # processador.processar("apple_pay", 299.90, {})  # ValueError!
