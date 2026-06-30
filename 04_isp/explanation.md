# I — Interface Segregation Principle (Princípio da Segregação de Interface)

## Definição

> "Nenhum cliente deve ser forçado a depender de métodos que não utiliza."
> — Robert C. Martin

É melhor ter **várias interfaces pequenas e específicas** do que uma interface grande e genérica.

## Cenário Real: Sistema de Usuários (Spotify)

No Spotify existem diferentes tipos de usuários:
- **Grátis**: ouve com anúncios, pulos limitados
- **Premium**: ouve sem anúncios, pula à vontade, baixa offline
- **Artista**: publica álbuns, vê estatísticas, agenda lançamentos

Se todos implementam a MESMA interface gigante, cada um é forçado a ter métodos que não fazem sentido.

## O Problema no `before.py`

```python
class Usuario(ABC):
    def reproduzir_musica(self, musica): ...
    def pular_musica(self): ...
    def baixar_musica(self, musica): ...
    def criar_playlist(self, nome): ...
    def ver_anuncios(self): ...
    def publicar_album(self, album): ...     # Ouvinte precisa disso?
    def ver_estatisticas(self): ...           # Ouvinte precisa disso?
    def agendar_lancamento(self, data): ...   # Ouvinte precisa disso?
```

Resultado:
- `UsuarioGratis.baixar_musica()` → `raise NotImplementedError`
- `UsuarioPremium.publicar_album()` → `raise NotImplementedError`
- `Artista.ver_anuncios()` → `pass` (ignora silenciosamente)

Métodos que lançam `NotImplementedError` ou que fazem `pass` são **red flags** de violação do ISP.

## A Solução no `after.py`

```python
class Reprodutor(ABC):           # Ouvir músicas
class PuladorMusica(ABC):        # Pular sem limite
class BaixadorMusica(ABC):       # Baixar offline
class CriadorPlaylist(ABC):      # Criar playlists
class VisualizadorAnuncios(ABC): # Ver anúncios
class PublicadorConteudo(ABC):   # Publicar álbuns
class AnalistaEstatisticas(ABC): # Ver estatísticas

class UsuarioGratis(Reprodutor, CriadorPlaylist, VisualizadorAnuncios): ...
class UsuarioPremium(Reprodutor, PuladorMusica, BaixadorMusica, CriadorPlaylist): ...
class Artista(Reprodutor, PuladorMusica, BaixadorMusica, PublicadorConteudo, AnalistaEstatisticas): ...
```

Cada tipo implementa **apenas** o que faz sentido. Sem `NotImplementedError`, sem `pass`.

## Python e Herança Múltipla

Python suporta herança múltipla nativamente, o que facilita muito o ISP:

```python
class UsuarioPremium(Reprodutor, PuladorMusica, BaixadorMusica, CriadorPlaylist):
    ...
```

Em linguagens como Java/C#, isso é feito com interfaces (`implements`). Em Python, usamos classes abstratas com `ABC` e herança múltipla.

## Sinais de Violação do ISP

1. **Métodos com `raise NotImplementedError`** em subclasses
2. **Métodos com `pass`** que não fazem nada
3. **Interfaces com mais de 5-6 métodos** (geralmente pode ser dividida)
4. **Subclasses que só usam metade** dos métodos da interface
5. **Comentários tipo** "este método não se aplica a esta classe"

## Por Que Isso é Importante em Empresas?

### 1. Funções tipadas corretamente
```python
def baixar_offline(usuarios: list[BaixadorMusica], musica: str):
    # O type checker GARANTE que todos podem baixar
```

### 2. Evolução independente
Adicionar uma feature de "podcast" não afeta as interfaces de música.

### 3. Composição flexível
Novo tipo de usuário? Basta escolher quais interfaces implementar:
```python
class UsuarioFamilia(Reprodutor, PuladorMusica, CriadorPlaylist):
    ...
```

### 4. Testes menores
Testar se alguém pode baixar músicas precisa apenas da interface `BaixadorMusica`.

## Regra Prática

Quando sua interface tem mais de 5 métodos, pergunte:
> "Todos os implementadores usam TODOS esses métodos?"

Se não, **divida a interface** em partes menores e mais coesas.
