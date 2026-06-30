"""
DESAFIO: Sistema de Transferências Bancárias
Este código viola TODOS os 5 princípios SOLID.
Sua missão: refatorar aplicando S.O.L.I.D.

Dica: leia os exemplos em 01_srp até 05_dip antes de começar.
"""

import json
from datetime import datetime


class SistemaTransferencia:
    """
    Classe que faz TUDO — viola SRP, OCP, LSP, ISP e DIP.
    Leia com atenção e identifique cada violação.
    """

    def __init__(self):
        self.saldo_contas = {
            "001": {"titular": "Ana Costa", "saldo": 5000.00, "tipo": "premium"},
            "002": {"titular": "Bruno Lima", "saldo": 1500.00, "tipo": "basico"},
            "003": {"titular": "Carlos Mendes", "saldo": 800.00, "tipo": "basico"},
        }
        self.historico = []

    # --- VIOLA SRP: faz validação, transferência, persistência,
    #     notificação e comprovante tudo na mesma classe ---

    def transferir(
        self,
        conta_origem: str,
        conta_destino: str,
        valor: float,
        tipo_transferencia: str,
    ) -> dict:
        # Validação
        if conta_origem not in self.saldo_contas:
            raise ValueError(f"Conta {conta_origem} não encontrada!")
        if conta_destino not in self.saldo_contas:
            raise ValueError(f"Conta {conta_destino} não encontrada!")

        origem = self.saldo_contas[conta_origem]
        destino = self.saldo_contas[conta_destino]

        if origem["saldo"] < valor:
            raise ValueError(f"Saldo insuficiente! Saldo: R${origem['saldo']:.2f}")

        # --- VIOLA OCP: cada novo tipo de transferência = mais um if ---
        if tipo_transferencia == "ted":
            taxa = 8.50
            limite = 10000.00
            print(f"[TED] Processando transferência de R${valor:.2f}")
        elif tipo_transferencia == "pix":
            taxa = 0.00
            limite = 5000.00
            print(f"[PIX] Processando transferência instantânea de R${valor:.2f}")
        elif tipo_transferencia == "doc":
            taxa = 12.00
            limite = 50000.00
            print(f"[DOC] Processando transferência de R${valor:.2f}")
        # elif tipo_transferencia == "swift": ...  # Precisaria modificar!
        else:
            raise ValueError(f"Tipo de transferência '{tipo_transferencia}' não suportado!")

        if valor > limite:
            raise ValueError(f"Valor R${valor:.2f} excede o limite de R${limite:.2f} para {tipo_transferencia.upper()}")

        # Executa a transferência
        valor_total = valor + taxa
        origem["saldo"] -= valor_total
        destino["saldo"] += valor

        print(f"Transferência de R${valor:.2f} (taxa: R${taxa:.2f})")
        print(f"{origem['titular']} -> {destino['titular']}")
        print(f"Saldo {origem['titular']}: R${origem['saldo']:.2f}")
        print(f"Saldo {destino['titular']}: R${destino['saldo']:.2f}")

        # --- VIOLA DIP: salva diretamente em arquivo JSON ---
        transacao = {
            "id": len(self.historico) + 1,
            "origem": conta_origem,
            "destino": conta_destino,
            "valor": valor,
            "taxa": taxa,
            "tipo": tipo_transferencia,
            "data": datetime.now().isoformat(),
        }
        self.historico.append(transacao)
        with open("transacoes.json", "a") as f:
            f.write(json.dumps(transacao) + "\n")
        print(f"[DB] Transação #{transacao['id']} salva.")

        # --- VIOLA ISP: notificação genérica que mistura canais ---
        self._notificar(origem["titular"], destino["titular"], valor, tipo_transferencia)

        # Gera comprovante
        comprovante = self._gerar_comprovante(transacao, origem, destino)

        return {"transacao": transacao, "comprovante": comprovante}

    def _notificar(
        self,
        remetente: str,
        destinatario: str,
        valor: float,
        tipo: str,
    ) -> None:
        """Notificação que mistura e-mail, SMS e push — viola ISP."""
        # E-mail
        print(f"[EMAIL] Para {remetente}: Transferência {tipo.upper()} de R${valor:.2f} enviada.")
        print(f"[EMAIL] Para {destinatario}: Você recebeu R${valor:.2f} via {tipo.upper()}.")

        # SMS
        print(f"[SMS] {remetente}: Transf. R${valor:.2f} enviada")
        print(f"[SMS] {destinatario}: Recebeu R${valor:.2f}")

        # Push (nem todo mundo tem app instalado!)
        print(f"[PUSH] {remetente}: Transferência enviada!")
        print(f"[PUSH] {destinatario}: Dinheiro na conta!")

    def _gerar_comprovante(self, transacao: dict, origem: dict, destino: dict) -> str:
        """Gera comprovante da transação."""
        comprovante = f"""
    ======== COMPROVANTE DE TRANSFERÊNCIA ========
    Transação: #{transacao['id']}
    Data: {transacao['data']}
    Tipo: {transacao['tipo'].upper()}
    -----------------------------------------------
    De: {origem['titular']} (Conta {transacao['origem']})
    Para: {destino['titular']} (Conta {transacao['destino']})
    Valor: R${transacao['valor']:.2f}
    Taxa: R${transacao['taxa']:.2f}
    Total debitado: R${transacao['valor'] + transacao['taxa']:.2f}
    ===============================================
        """
        print(comprovante)
        return comprovante

    # --- VIOLA LSP: método que não funciona para todos os tipos ---

    def agendar_transferencia(
        self,
        conta_origem: str,
        conta_destino: str,
        valor: float,
        tipo_transferencia: str,
        data_agendamento: str,
    ) -> None:
        """PIX é instantâneo — agendamento não faz sentido para PIX."""
        if tipo_transferencia == "pix":
            # Viola LSP: se trato PIX como qualquer transferência,
            # agendar deveria funcionar, mas explode aqui
            raise NotImplementedError("PIX não pode ser agendado!")

        print(f"[AGENDAMENTO] {tipo_transferencia.upper()} de R${valor:.2f}")
        print(f"[AGENDAMENTO] De {conta_origem} para {conta_destino}")
        print(f"[AGENDAMENTO] Data: {data_agendamento}")


if __name__ == "__main__":
    sistema = SistemaTransferencia()

    print("=" * 50)
    print("TRANSFERÊNCIA 1: TED")
    print("=" * 50)
    sistema.transferir("001", "002", 500.00, "ted")

    print(f"\n{'=' * 50}")
    print("TRANSFERÊNCIA 2: PIX")
    print("=" * 50)
    sistema.transferir("001", "003", 200.00, "pix")

    print(f"\n{'=' * 50}")
    print("AGENDAMENTO TED")
    print("=" * 50)
    sistema.agendar_transferencia("001", "002", 1000.00, "ted", "2025-08-01")

    print(f"\n{'=' * 50}")
    print("TENTANDO AGENDAR PIX (vai falhar!)")
    print("=" * 50)
    try:
        sistema.agendar_transferencia("001", "002", 100.00, "pix", "2025-08-01")
    except NotImplementedError as e:
        print(f"ERRO: {e}")
