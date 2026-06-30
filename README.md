# SOLID com Python

Estudo prático dos 5 princípios SOLID usando Python, com exemplos reais de empresas e cenários do dia a dia.

Cada princípio tem:
- **`before.py`** — código que **viola** o princípio
- **`after.py`** — código **refatorado** aplicando o princípio
- **`explanation.md`** — explicação detalhada com contexto de negócio

## Estrutura

```
solid-with-python/
├── README.md
├── 01_srp/          # Single Responsibility Principle
│   ├── before.py
│   ├── after.py
│   └── explanation.md
├── 02_ocp/          # Open/Closed Principle
│   ├── before.py
│   ├── after.py
│   └── explanation.md
├── 03_lsp/          # Liskov Substitution Principle
│   ├── before.py
│   ├── after.py
│   └── explanation.md
├── 04_isp/          # Interface Segregation Principle
│   ├── before.py
│   ├── after.py
│   └── explanation.md
├── 05_dip/          # Dependency Inversion Principle
│   ├── before.py
│   ├── after.py
│   └── explanation.md
└── challenge/       # Desafio final integrando todos os princípios
    ├── README.md
    └── challenge.py
```

## Os 5 Princípios SOLID

| # | Sigla | Princípio | Resumo |
|---|-------|-----------|--------|
| 1 | **S** | Single Responsibility | Uma classe deve ter apenas **uma razão para mudar** |
| 2 | **O** | Open/Closed | Aberto para **extensão**, fechado para **modificação** |
| 3 | **L** | Liskov Substitution | Subclasses devem ser **substituíveis** pelas suas classes base |
| 4 | **I** | Interface Segregation | Muitas interfaces específicas são melhores que **uma interface genérica** |
| 5 | **D** | Dependency Inversion | Dependa de **abstrações**, não de implementações concretas |

## Cenários Usados

Cada princípio usa um cenário real inspirado em empresas conhecidas:

- **SRP** — Sistema de pedidos tipo iFood (separação de responsabilidades)
- **OCP** — Gateway de pagamento tipo Stripe (extensão de meios de pagamento)
- **LSP** — Sistema de notificações tipo Twilio (substituição de canais)
- **ISP** — Sistema de usuários tipo Spotify (interfaces por tipo de usuário)
- **DIP** — Sistema de e-commerce tipo Amazon (inversão de dependências)

## Como Estudar

1. Leia o `before.py` e identifique os problemas
2. Leia o `explanation.md` para entender o princípio
3. Compare com o `after.py` para ver a solução
4. Tente refatorar o `before.py` por conta própria antes de ver o `after.py`
5. Faça o desafio final na pasta `challenge/`

## Como Executar

```bash
# Executar qualquer exemplo
python 01_srp/before.py
python 01_srp/after.py

# Ou todos de uma vez
for dir in 01_srp 02_ocp 03_lsp 04_isp 05_dip; do
    echo "=== $dir ==="
    python "$dir/before.py"
    echo "---"
    python "$dir/after.py"
    echo ""
done
```

## Requisitos

- Python 3.10+
- Nenhuma dependência externa (usa apenas a biblioteca padrão)
