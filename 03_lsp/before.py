"""
LSP - Liskov Substitution Principle (ANTES)
Cenário: Sistema de notificações inspirado no Twilio

Problema: A classe NotificacaoPush herda de Notificacao mas não pode
enviar de verdade (lança exceção). Isso viola o LSP — uma subclasse
não deveria quebrar o comportamento esperado da classe base.
"""


class Notificacao:
    """Classe base para envio de notificações."""

    def __init__(self, destinatario: str, mensagem: str):
        self.destinatario = destinatario
        self.mensagem = mensagem

    def enviar(self) -> None:
        raise NotImplementedError("Subclasses devem implementar enviar()")

    def agendar(self, horario: str) -> None:
        print(f"[AGENDADO] Notificação para {self.destinatario} às {horario}")

    def obter_status(self) -> str:
        return "enviado"


class NotificacaoEmail(Notificacao):
    def enviar(self) -> None:
        print(f"[EMAIL] Enviando para {self.destinatario}: {self.mensagem}")

    def obter_status(self) -> str:
        return "enviado"


class NotificacaoSMS(Notificacao):
    def enviar(self) -> None:
        if len(self.mensagem) > 160:
            # Trunca a mensagem em vez de enviar completa
            # Isso MUDA o comportamento esperado!
            self.mensagem = self.mensagem[:157] + "..."
        print(f"[SMS] Enviando para {self.destinatario}: {self.mensagem}")

    def obter_status(self) -> str:
        return "enviado"


class NotificacaoPush(Notificacao):
    """Push notification que NÃO suporta agendamento — viola LSP!"""

    def enviar(self) -> None:
        print(f"[PUSH] Enviando para {self.destinatario}: {self.mensagem}")

    def agendar(self, horario: str) -> None:
        # Viola LSP: a classe base promete que agendar() funciona,
        # mas esta subclasse lança exceção!
        raise NotImplementedError(
            "Push notifications não suportam agendamento!"
        )

    def obter_status(self) -> str:
        # Viola LSP: retorna tipo diferente do esperado (dict vs str)
        return {"status": "enviado", "plataforma": "iOS"}  # type: ignore


def enviar_notificacoes_em_massa(notificacoes: list[Notificacao]) -> None:
    """Função que deveria funcionar com QUALQUER Notificacao."""
    for notificacao in notificacoes:
        notificacao.enviar()
        notificacao.agendar("08:00")  # BOOM! Push vai explodir aqui
        status = notificacao.obter_status()
        # Espera uma string, mas Push retorna dict
        print(f"Status ({len(status)} chars): {status}")


if __name__ == "__main__":
    notificacoes = [
        NotificacaoEmail("joao@email.com", "Sua conta foi criada!"),
        NotificacaoSMS("+5511999998888", "Código de verificação: 123456"),
    ]

    print("=== Enviando Email e SMS (funciona) ===")
    enviar_notificacoes_em_massa(notificacoes)

    print("\n=== Adicionando Push (vai quebrar!) ===")
    notificacoes.append(
        NotificacaoPush("user_device_token_abc", "Você tem uma nova mensagem!")
    )
    try:
        enviar_notificacoes_em_massa(notificacoes)
    except NotImplementedError as e:
        print(f"\nERRO: {e}")
        print("A subclasse NotificacaoPush QUEBROU o contrato da classe base!")
