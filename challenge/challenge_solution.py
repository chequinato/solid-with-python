
"""
Desafio Final: Aplicando Todos os Princípios SOLID
Solução: challenge_solucao.py
"""

from abc import ABC, abstractmethod
from datetime import datetime
import json

# Entidades

class Conta:
    def __init__(self, numero, titular, saldo, tipo):
        self.numero = numero
        self.titular = titular
        self.saldo = saldo
        self.tipo = tipo

# SRP: Validação de Transferência

class ValidadorTransferencia:

    def validar(self, origem, destino, valor, tipo_transferencia):

        if origem is None:
            raise ValueError("Conta origem inexistente.")

        if destino is None:
            raise ValueError("Conta destino inexistente.")

        if origem.saldo < valor:
            raise ValueError("Saldo insuficiente.")

        if valor > tipo_transferencia.limite:
            raise ValueError(
                f"Limite de R${tipo_transferencia.limite:.2f} excedido."
            )


# OCP

class TipoTransferencia(ABC):

    @property
    @abstractmethod
    def taxa(self):
        pass

    @property
    @abstractmethod
    def limite(self):
        pass

    @property
    @abstractmethod
    def nome(self):
        pass


class PixTransferencia(TipoTransferencia):

    @property
    def taxa(self):
        return 0.0

    @property
    def limite(self):
        return 5000.0

    @property
    def nome(self):
        return "PIX"


class TedTransferencia(TipoTransferencia):

    @property
    def taxa(self):
        return 8.50

    @property
    def limite(self):
        return 10000.0

    @property
    def nome(self):
        return "TED"


class DocTransferencia(TipoTransferencia):

    @property
    def taxa(self):
        return 12.0

    @property
    def limite(self):
        return 50000.0

    @property
    def nome(self):
        return "DOC"


# DIP

class Repositorio(ABC):

    @abstractmethod
    def salvar(self, transacao):
        pass


class JsonRepositorio(Repositorio):

    def salvar(self, transacao):

        with open("transacoes.json", "a", encoding="utf8") as f:
            f.write(json.dumps(transacao) + "\n")

        print("[DB] Transação salva.")


# ISP

class Notificador(ABC):

    @abstractmethod
    def notificar(self, transacao):
        pass


class EmailNotificador(Notificador):

    def notificar(self, transacao):

        print(
            f"[EMAIL] Transferência de R${transacao['valor']:.2f} realizada."
        )


class SMSNotificador(Notificador):

    def notificar(self, transacao):

        print(
            f"[SMS] Transferência de R${transacao['valor']:.2f} realizada."
        )


class PushNotificador(Notificador):

    def notificar(self, transacao):

        print(
            f"[PUSH] Transferência de R${transacao['valor']:.2f} realizada."
        )


# SRP

class GeradorComprovante:

    def gerar(self, transacao):

        comprovante = f"""
========== COMPROVANTE ==========
Origem: {transacao['origem']}
Destino: {transacao['destino']}
Tipo: {transacao['tipo']}
Valor: R${transacao['valor']:.2f}
Taxa: R${transacao['taxa']:.2f}
=================================
"""
        print(comprovante)
        return comprovante


# SISTEMA

class SistemaTransferencia:

    def __init__(
        self,
        tipo_transferencia,
        repositorio,
        comprovante,
        notificadores,
        validador,
    ):

        self.tipo_transferencia = tipo_transferencia
        self.repositorio = repositorio
        self.comprovante = comprovante
        self.notificadores = notificadores
        self.validador = validador

    def transferir(self, origem, destino, valor):

        self.validador.validar(
            origem,
            destino,
            valor,
            self.tipo_transferencia,
        )

        origem.saldo -= valor + self.tipo_transferencia.taxa
        destino.saldo += valor

        transacao = {
            "origem": origem.numero,
            "destino": destino.numero,
            "valor": valor,
            "taxa": self.tipo_transferencia.taxa,
            "tipo": self.tipo_transferencia.nome,
            "data": datetime.now().isoformat(),
        }

        self.repositorio.salvar(transacao)

        for notificador in self.notificadores:
            notificador.notificar(transacao)

        self.comprovante.gerar(transacao)


# EXEMPLO

if __name__ == "__main__":

    conta1 = Conta("001", "Ana", 5000, "premium")
    conta2 = Conta("002", "Bruno", 2000, "basico")

    sistema = SistemaTransferencia(
        tipo_transferencia=TedTransferencia(),
        repositorio=JsonRepositorio(),
        comprovante=GeradorComprovante(),
        notificadores=[
            EmailNotificador(),
            SMSNotificador(),
            PushNotificador(),
        ],
        validador=ValidadorTransferencia(),
    )

    sistema.transferir(conta1, conta2, 500)

    print(conta1.saldo)
    print(conta2.saldo)