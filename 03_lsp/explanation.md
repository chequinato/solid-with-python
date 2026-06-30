# L — Liskov Substitution Principle (Princípio da Substituição de Liskov)

## Definição

> "Se S é um subtipo de T, então objetos do tipo T podem ser substituídos por objetos do tipo S sem alterar as propriedades desejáveis do programa."
> — Barbara Liskov

Em termos simples: **se uma função espera um objeto da classe base, qualquer subclasse deve funcionar perfeitamente no lugar**, sem surpresas, exceções inesperadas ou comportamentos diferentes.

## Cenário Real: Sistema de Notificações (Twilio)

Imagine que você trabalha no Twilio e tem um sistema que envia notificações por vários canais: e-mail, SMS, push, WhatsApp. Todos herdam de `Notificacao`.

O problema surge quando uma subclasse **não consegue cumprir o contrato** da classe base.

## O Problema no `before.py`

```python
class Notificacao:
    def enviar(self): ...
    def agendar(self, horario): ...    # Promete que toda notificação pode ser agendada
    def obter_status(self) -> str: ...  # Promete retornar uma string

class NotificacaoPush(Notificacao):
    def agendar(self, horario):
        raise NotImplementedError("Push não suporta agendamento!")  # QUEBRA!

    def obter_status(self):
        return {"status": "enviado", "plataforma": "iOS"}  # Retorna dict, não str!
```

Violações do LSP:
1. **`agendar()` lança exceção** — a classe base promete que funciona, mas a subclasse explode
2. **`obter_status()` retorna tipo diferente** — quem espera `str` recebe `dict`
3. **`NotificacaoSMS` trunca a mensagem** — muda silenciosamente o conteúdo enviado

## A Solução no `after.py`

```python
class Notificacao(ABC):           # Contrato mínimo: enviar + status
    def enviar(self): ...
    def obter_status(self) -> str: ...

class NotificacaoAgendavel(Notificacao):  # Extensão: + agendamento
    def agendar(self, horario): ...

class NotificacaoEmail(NotificacaoAgendavel): ...  # Suporta tudo
class NotificacaoSMS(NotificacaoAgendavel): ...    # Suporta tudo
class NotificacaoPush(Notificacao): ...            # Só envio (sem agendamento)
```

- `NotificacaoPush` herda de `Notificacao` (não de `NotificacaoAgendavel`)
- Ela cumpre 100% do contrato que promete
- Funções que precisam agendar recebem `list[NotificacaoAgendavel]`

## Sinais de Violação do LSP

1. **Subclasse lança exceção em método da classe base** (`raise NotImplementedError`)
2. **Subclasse retorna tipo diferente** do esperado
3. **Subclasse ignora ou altera silenciosamente** os parâmetros
4. **Verificações de tipo em runtime** (`if isinstance(obj, Push): ...`)
5. **Comentários tipo** "não usar este método nesta subclasse"

## Por Que Isso é Importante em Empresas?

### 1. Código genérico funciona de verdade
Uma função `enviar_notificacoes(lista)` funciona com qualquer canal, sem `try/except` defensivo.

### 2. Novos canais não quebram o sistema
Adicionar WhatsApp ou Telegram não exige revisar todo o código que usa `Notificacao`.

### 3. Contratos claros entre equipes
A equipe que cria o canal de WhatsApp sabe exatamente o que precisa implementar.

### 4. Type checkers funcionam
Com tipos corretos, ferramentas como `mypy` conseguem pegar erros antes de rodar o código.

## Regra Prática

Antes de fazer uma subclasse, pergunte:
> "Se eu trocar a classe base por esta subclasse em QUALQUER lugar do código, tudo continua funcionando?"

Se não, a herança está errada — repense a hierarquia.
