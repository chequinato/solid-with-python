# S — Single Responsibility Principle (Princípio da Responsabilidade Única)

## Definição

> "Uma classe deve ter um, e apenas um, motivo para mudar."
> — Robert C. Martin

Isso significa que cada classe deve ter **uma única responsabilidade** bem definida. Se você precisa mudar a classe por mais de um motivo, ela está fazendo coisas demais.

## Cenário Real: Sistema de Pedidos (iFood)

Imagine que você trabalha no iFood e tem uma classe `Pedido` que:
- Calcula o total do pedido
- Salva no banco de dados
- Envia e-mail de confirmação
- Gera nota fiscal

Se a regra de cálculo da taxa de entrega mudar, você mexe na classe `Pedido`.
Se o formato do e-mail mudar, você mexe na classe `Pedido`.
Se o banco de dados migrar de JSON para PostgreSQL, você mexe na classe `Pedido`.

**Isso é perigoso!** Uma mudança no e-mail pode quebrar o cálculo do total sem querer.

## O Problema no `before.py`

```python
class Pedido:
    def calcular_total(self): ...       # Regra de negócio
    def salvar_no_banco(self): ...      # Persistência
    def enviar_email_confirmacao(self): ...  # Notificação
    def gerar_nota_fiscal(self): ...    # Documento fiscal
    def processar_pedido(self): ...     # Orquestração
```

A classe `Pedido` tem **4 motivos para mudar** — viola completamente o SRP.

## A Solução no `after.py`

```python
class Pedido:               # Apenas dados do pedido
class CalculadoraPedido:     # Apenas cálculos
class RepositorioPedido:     # Apenas persistência
class NotificadorEmail:      # Apenas notificações
class GeradorNotaFiscal:     # Apenas nota fiscal
class ProcessadorPedido:     # Apenas orquestração
```

Cada classe tem **um único motivo para mudar**:
- Mudou a taxa de entrega? → `CalculadoraPedido`
- Mudou o banco de dados? → `RepositorioPedido`
- Mudou o template do e-mail? → `NotificadorEmail`
- Mudou o layout da nota fiscal? → `GeradorNotaFiscal`

## Por Que Isso é Importante em Empresas?

### 1. Equipes diferentes podem trabalhar em paralelo
No iFood, a equipe de billing pode mexer no `CalculadoraPedido` enquanto a equipe de comunicação mexe no `NotificadorEmail`, sem conflitos de merge.

### 2. Testes ficam mais simples
Testar o cálculo do total não precisa de um banco de dados nem de um servidor de e-mail.

### 3. Bugs ficam isolados
Um bug no gerador de nota fiscal não vai afetar o salvamento no banco de dados.

### 4. Reutilização
O `NotificadorEmail` pode ser usado em outros contextos (promoções, cancelamentos) sem arrastar toda a lógica de pedidos.

## Regra Prática

Antes de criar uma classe, pergunte:
> "Essa classe tem mais de um motivo para mudar?"

Se sim, **separe as responsabilidades**.
