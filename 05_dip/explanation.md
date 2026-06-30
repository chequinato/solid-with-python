# D — Dependency Inversion Principle (Princípio da Inversão de Dependência)

## Definição

> "Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem depender de abstrações."
> — Robert C. Martin

Em outras palavras: **dependa de interfaces, não de implementações concretas**. E as dependências devem ser **injetadas de fora**, não criadas internamente.

## Cenário Real: E-commerce (Amazon)

Imagine que você trabalha na Amazon e tem um `ServicoDeCompra` que:
- Busca produtos no **MySQL**
- Envia pelo **Correios**
- Cobra via **Stripe**

Se amanhã a empresa decidir migrar para PostgreSQL, trocar para uma transportadora, ou usar PagSeguro... você precisa **reescrever** o ServicoDeCompra?

Com DIP, **não**.

## O Problema no `before.py`

```python
class ServicoDeCompra:
    def __init__(self):
        self.repositorio = RepositorioMySQL()    # Acoplado!
        self.frete = ServicoCorreios()            # Acoplado!
        self.pagamento = GatewayStripe()          # Acoplado!
```

O `ServicoDeCompra` **cria** suas dependências internamente. Isso significa:
- Trocar MySQL → PostgreSQL = modificar ServicoDeCompra
- Trocar Correios → Transportadora = modificar ServicoDeCompra
- Trocar Stripe → PagSeguro = modificar ServicoDeCompra
- Testar sem banco/API real = praticamente impossível

## A Solução no `after.py`

```python
class ServicoDeCompra:
    def __init__(
        self,
        repo_produto: RepositorioProduto,       # Interface!
        repo_pedido: RepositorioPedido,          # Interface!
        servico_frete: ServicoFrete,             # Interface!
        gateway_pagamento: GatewayPagamento,     # Interface!
    ):
        self.repo_produto = repo_produto
        ...
```

O `ServicoDeCompra` **recebe** suas dependências de fora (injeção de dependência) e depende de **abstrações** (interfaces), não de implementações concretas.

## A "Inversão" no Nome

Sem DIP:
```
ServicoDeCompra → RepositorioMySQL
ServicoDeCompra → ServicoCorreios
ServicoDeCompra → GatewayStripe
```
O módulo de alto nível depende dos módulos de baixo nível.

Com DIP:
```
ServicoDeCompra → RepositorioProduto (interface)
RepositorioMySQL → RepositorioProduto (interface)
```
Ambos dependem da abstração. A direção da dependência foi **invertida** para o módulo de baixo nível.

## Injeção de Dependência em Python

A forma mais comum é pelo **construtor**:

```python
# MySQL + Correios + Stripe
servico = ServicoDeCompra(
    repo_produto=RepositorioProdutoMySQL(),
    repo_pedido=RepositorioPedidoMySQL(),
    servico_frete=ServicoCorreios(),
    gateway_pagamento=GatewayStripe(),
)

# PostgreSQL + Transportadora + PagSeguro (SEM mudar ServicoDeCompra!)
servico = ServicoDeCompra(
    repo_produto=RepositorioProdutoPostgreSQL(),
    repo_pedido=RepositorioPedidoPostgreSQL(),
    servico_frete=ServicoTransportadora(),
    gateway_pagamento=GatewayPagSeguro(),
)
```

## Por Que Isso é Importante em Empresas?

### 1. Testes unitários de verdade
```python
# Em testes, injeta implementações fake
servico = ServicoDeCompra(
    repo_produto=RepositorioFake(),
    repo_pedido=RepositorioFake(),
    servico_frete=FreteFake(),
    gateway_pagamento=PagamentoFake(),
)
```
Sem banco de dados real, sem API externa, sem custos.

### 2. Migração gradual
Na Amazon, podem migrar do MySQL para DynamoDB **sem tocar** no ServicoDeCompra. Basta criar `RepositorioProdutoDynamoDB` e injetar.

### 3. Ambientes diferentes
- Desenvolvimento: banco local + frete fake
- Staging: banco de staging + Correios sandbox
- Produção: banco real + Correios real

Tudo configurado na hora de criar o `ServicoDeCompra`, sem alterar código.

### 4. Múltiplas configurações em paralelo
Pode rodar vendas do Brasil com Correios e vendas dos EUA com FedEx, usando o MESMO `ServicoDeCompra`.

## Regra Prática

Quando uma classe cria suas dependências com `self.x = ClasseConcreta()`, pergunte:
> "E se eu precisar trocar essa implementação amanhã?"

Se a resposta for "teria que modificar esta classe", **extraia uma interface e injete a dependência**.
