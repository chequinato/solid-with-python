# Desafio Final: Aplicando Todos os Princípios SOLID

## O Cenário

Você é desenvolvedor em uma fintech e precisa construir um sistema de **transferências bancárias** que:

1. Valida a transferência (saldo, limites, fraude)
2. Executa a transferência entre contas
3. Registra a transação no banco de dados
4. Envia notificação para o remetente e destinatário
5. Gera comprovante da transação

## O Código Atual (`challenge.py`)

O arquivo `challenge.py` contém uma implementação que **viola todos os 5 princípios SOLID**. Sua missão é refatorar o código aplicando:

- **SRP**: Separar as responsabilidades em classes diferentes
- **OCP**: Permitir adicionar novos tipos de transferência sem modificar código existente
- **LSP**: Garantir que subtipos sejam substituíveis
- **ISP**: Criar interfaces específicas em vez de uma interface genérica
- **DIP**: Injetar dependências em vez de criar internamente

## Instruções

1. Leia o `challenge.py` com cuidado
2. Identifique quais princípios estão sendo violados (e onde)
3. Crie um arquivo `challenge_solucao.py` com sua refatoração
4. Teste executando ambos os arquivos para garantir que o comportamento é o mesmo

## Dicas

- Comece pelo **SRP** — separe as responsabilidades
- Depois aplique **DIP** — extraia interfaces e injete dependências
- O **OCP** vai surgir naturalmente ao usar polimorfismo
- **LSP** e **ISP** ajudam a definir contratos corretos

## Critérios de Sucesso

- [ ] Cada classe tem uma única responsabilidade
- [ ] Novos tipos de transferência podem ser adicionados sem modificar classes existentes
- [ ] Todas as subclasses cumprem o contrato da classe base
- [ ] Nenhuma classe é forçada a implementar métodos que não usa
- [ ] Dependências são injetadas, não criadas internamente
- [ ] O sistema produz o mesmo output que o original

Boa sorte!
