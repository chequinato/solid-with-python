# O — Open/Closed Principle (Princípio Aberto/Fechado)

## Definição

> "Entidades de software devem ser abertas para extensão, mas fechadas para modificação."
> — Bertrand Meyer

Você deve conseguir **adicionar novos comportamentos** sem precisar **alterar o código existente** que já funciona.

## Cenário Real: Gateway de Pagamento (Stripe)

Imagine que você trabalha no Stripe e precisa suportar vários meios de pagamento:
cartão de crédito, PIX, boleto, Apple Pay, Google Pay, PayPal...

Se cada novo meio de pagamento exige modificar a classe `ProcessadorPagamento`, você está violando o OCP.

## O Problema no `before.py`

```python
class ProcessadorPagamento:
    def processar(self, tipo: str, valor: float, dados: dict):
        if tipo == "cartao_credito":
            self._processar_cartao_credito(valor, dados)
        elif tipo == "pix":
            self._processar_pix(valor, dados)
        elif tipo == "boleto":
            self._processar_boleto(valor, dados)
        # elif tipo == "apple_pay": ...  ← Precisa modificar!
        # elif tipo == "google_pay": ... ← Precisa modificar!
```

Problemas:
- Cada novo pagamento = modificar a classe existente
- Cadeia de `if/elif` cresce infinitamente
- Risco de quebrar pagamentos que já funcionam ao adicionar novos

## A Solução no `after.py`

```python
class MetodoPagamento(ABC):
    @abstractmethod
    def processar(self, valor, dados): ...

class PagamentoCartaoCredito(MetodoPagamento): ...
class PagamentoPix(MetodoPagamento): ...
class PagamentoBoleto(MetodoPagamento): ...
class PagamentoApplePay(MetodoPagamento): ...  # ← Só criar nova classe!
```

O `ProcessadorPagamento` não precisa saber os detalhes de cada meio — ele recebe qualquer `MetodoPagamento` e chama `.processar()`.

## Por Que Isso é Importante em Empresas?

### 1. Deploy sem medo
Adicionar Apple Pay não toca no código de cartão de crédito. Zero risco de quebrar pagamentos existentes.

### 2. Plugins e extensibilidade
No Stripe, parceiros podem criar seus próprios meios de pagamento sem acesso ao código-fonte do processador principal.

### 3. Testes isolados
Cada meio de pagamento é testado de forma independente. Testes do PIX não rodam código de boleto.

### 4. Escalabilidade de equipe
A equipe A pode criar `PagamentoApplePay` enquanto a equipe B cria `PagamentoGooglePay`, em branches separadas, sem conflito.

## Padrões que ajudam a aplicar o OCP

- **Strategy Pattern** — encapsula algoritmos intercambiáveis (é o que usamos no exemplo)
- **Template Method** — define a estrutura na classe base, delega detalhes para subclasses
- **Plugin/Registry** — registra implementações em runtime

## Regra Prática

Quando você vê uma cadeia de `if/elif/else` baseada em "tipo", pergunte:
> "Posso trocar esses ifs por polimorfismo?"

Se sim, extraia uma classe abstrata e crie uma implementação para cada caso.
