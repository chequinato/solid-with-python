"""
LSP - Liskov Substitution Principle (DEPOIS)
Cenário: Sistema de notificações inspirado no Twilio

Solução: Separamos as capacidades em interfaces distintas.
Nem toda notificação precisa suportar agendamento.
Cada subtipo cumpre 100% do contrato que promete.
"""

from abc import ABC, abstractmethod


class Notificacao(ABC):
    """Contrato base: toda notificação DEVE conseguir enviar e dar status."""

    def __init__(self, destinatario: str, mensagem: str):
        self.destinatario = destinatario
        self.mensagem = mensagem

    @abstractmethod
    def enviar(self) -> None:
        ...

    @abstractmethod
    def obter_status(self) -> str:
        ...


class NotificacaoAgendavel(Notificacao):
    """Extensão: notificações que TAMBÉM suportam agendamento."""

    @abstractmethod
    def agendar(self, horario: str) -> None:
        ...


class NotificacaoEmail(NotificacaoAgendavel):
    def enviar(self) -> None:
        print(f"[EMAIL] Enviando para {self.destinatario}: {self.mensagem}")

    def obter_status(self) -> str:
        return "enviado"

    def agendar(self, horario: str) -> None:
        print(f"[EMAIL] Agendado para {self.destinatario} às {horario}")


class NotificacaoSMS(NotificacaoAgendavel):
    LIMITE_CARACTERES = 160

    def enviar(self) -> None:
        if len(self.mensagem) > self.LIMITE_CARACTERES:
            partes = [
                self.mensagem[i:i + self.LIMITE_CARACTERES]
                for i in range(0, len(self.mensagem), self.LIMITE_CARACTERES)
            ]
            for i, parte in enumerate(partes, 1):
                print(f"[SMS] Parte {i}/{len(partes)} para {self.destinatario}: {parte}")
        else:
            print(f"[SMS] Enviando para {self.destinatario}: {self.mensagem}")

    def obter_status(self) -> str:
        return "enviado"

    def agendar(self, horario: str) -> None:
        print(f"[SMS] Agendado para {self.destinatario} às {horario}")


class NotificacaoPush(Notificacao):
    """Push notification — NÃO herda de NotificacaoAgendavel
    porque push não suporta agendamento. E tudo bem!"""

    def enviar(self) -> None:
        print(f"[PUSH] Enviando para {self.destinatario}: {self.mensagem}")

    def obter_status(self) -> str:
        return "enviado"


class NotificacaoWhatsApp(Notificacao):
    """Outro canal que não suporta agendamento — sem problemas!"""

    def enviar(self) -> None:
        print(f"[WHATSAPP] Enviando para {self.destinatario}: {self.mensagem}")

    def obter_status(self) -> str:
        return "enviado"


def enviar_notificacoes(notificacoes: list[Notificacao]) -> None:
    """Funciona com QUALQUER Notificacao — sem surpresas!"""
    for notificacao in notificacoes:
        notificacao.enviar()
        status = notificacao.obter_status()
        print(f"Status: {status}\n")


def agendar_notificacoes(notificacoes: list[NotificacaoAgendavel], horario: str) -> None:
    """Só aceita notificações que DE FATO suportam agendamento."""
    for notificacao in notificacoes:
        notificacao.agendar(horario)


if __name__ == "__main__":
    # Todas as notificações podem ser enviadas — LSP respeitado!
    todas = [
        NotificacaoEmail("joao@email.com", "Sua conta foi criada!"),
        NotificacaoSMS("+5511999998888", "Código de verificação: 123456"),
        NotificacaoPush("user_device_token_abc", "Você tem uma nova mensagem!"),
        NotificacaoWhatsApp("+5511999997777", "Olá! Bem-vindo ao nosso serviço."),
    ]

    print("=== Enviando todas as notificações ===")
    enviar_notificacoes(todas)

    # Só agenda as que suportam agendamento
    agendaveis = [
        NotificacaoEmail("joao@email.com", "Lembrete de reunião"),
        NotificacaoSMS("+5511999998888", "Sua consulta é amanhã às 14h"),
    ]

    print("=== Agendando notificações ===")
    agendar_notificacoes(agendaveis, "08:00")
