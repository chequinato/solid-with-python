"""
ISP - Interface Segregation Principle (ANTES)
Cenário: Sistema de usuários inspirado no Spotify

Problema: A interface Usuario é gigante — obriga TODOS os tipos de
usuário a implementar métodos que não fazem sentido para eles.
Usuário grátis não pode pular músicas ilimitadamente, e artista
não precisa de playlist.
"""

from abc import ABC, abstractmethod


class Usuario(ABC):
    """Interface GORDA — obriga todos a implementar tudo."""

    @abstractmethod
    def reproduzir_musica(self, musica: str) -> None:
        ...

    @abstractmethod
    def pular_musica(self) -> None:
        ...

    @abstractmethod
    def baixar_musica(self, musica: str) -> None:
        ...

    @abstractmethod
    def criar_playlist(self, nome: str) -> None:
        ...

    @abstractmethod
    def ver_anuncios(self) -> None:
        ...

    @abstractmethod
    def publicar_album(self, album: str) -> None:
        ...

    @abstractmethod
    def ver_estatisticas(self) -> None:
        ...

    @abstractmethod
    def agendar_lancamento(self, data: str) -> None:
        ...


class UsuarioGratis(Usuario):
    """Usuário gratuito — obrigado a implementar métodos que não usa."""

    def __init__(self, nome: str):
        self.nome = nome

    def reproduzir_musica(self, musica: str) -> None:
        print(f"[FREE] {self.nome} ouvindo: {musica}")

    def pular_musica(self) -> None:
        print(f"[FREE] {self.nome} não pode pular! (limite atingido)")

    def baixar_musica(self, musica: str) -> None:
        # Não faz sentido para usuário grátis!
        raise NotImplementedError("Usuário grátis não pode baixar músicas!")

    def criar_playlist(self, nome: str) -> None:
        print(f"[FREE] {self.nome} criou playlist: {nome}")

    def ver_anuncios(self) -> None:
        print(f"[FREE] Exibindo anúncio para {self.nome}...")

    def publicar_album(self, album: str) -> None:
        # Não faz NENHUM sentido para um ouvinte!
        raise NotImplementedError("Ouvinte não pode publicar álbum!")

    def ver_estatisticas(self) -> None:
        # Não faz sentido para ouvinte!
        raise NotImplementedError("Ouvinte não tem estatísticas de artista!")

    def agendar_lancamento(self, data: str) -> None:
        # Não faz sentido para ouvinte!
        raise NotImplementedError("Ouvinte não pode agendar lançamento!")


class UsuarioPremium(Usuario):
    """Usuário premium — ainda obrigado a implementar métodos de artista."""

    def __init__(self, nome: str):
        self.nome = nome

    def reproduzir_musica(self, musica: str) -> None:
        print(f"[PREMIUM] {self.nome} ouvindo (sem anúncios): {musica}")

    def pular_musica(self) -> None:
        print(f"[PREMIUM] {self.nome} pulou a música!")

    def baixar_musica(self, musica: str) -> None:
        print(f"[PREMIUM] {self.nome} baixou: {musica}")

    def criar_playlist(self, nome: str) -> None:
        print(f"[PREMIUM] {self.nome} criou playlist: {nome}")

    def ver_anuncios(self) -> None:
        # Premium não vê anúncios!
        pass

    def publicar_album(self, album: str) -> None:
        raise NotImplementedError("Ouvinte não pode publicar álbum!")

    def ver_estatisticas(self) -> None:
        raise NotImplementedError("Ouvinte não tem estatísticas de artista!")

    def agendar_lancamento(self, data: str) -> None:
        raise NotImplementedError("Ouvinte não pode agendar lançamento!")


class Artista(Usuario):
    """Artista — obrigado a implementar playlist e anúncios que não usa."""

    def __init__(self, nome: str):
        self.nome = nome

    def reproduzir_musica(self, musica: str) -> None:
        print(f"[ARTISTA] {self.nome} ouvindo: {musica}")

    def pular_musica(self) -> None:
        print(f"[ARTISTA] {self.nome} pulou a música!")

    def baixar_musica(self, musica: str) -> None:
        print(f"[ARTISTA] {self.nome} baixou: {musica}")

    def criar_playlist(self, nome: str) -> None:
        # Artista não precisa de playlist no mesmo sentido
        pass

    def ver_anuncios(self) -> None:
        # Artista não vê anúncios
        pass

    def publicar_album(self, album: str) -> None:
        print(f"[ARTISTA] {self.nome} publicou o álbum: {album}")

    def ver_estatisticas(self) -> None:
        print(f"[ARTISTA] {self.nome} - 1.5M ouvintes mensais")

    def agendar_lancamento(self, data: str) -> None:
        print(f"[ARTISTA] {self.nome} agendou lançamento para {data}")


if __name__ == "__main__":
    gratis = UsuarioGratis("Maria")
    premium = UsuarioPremium("João")
    artista = Artista("Anitta")

    print("=== Usuário Grátis ===")
    gratis.reproduzir_musica("Envolver - Anitta")
    gratis.ver_anuncios()
    try:
        gratis.baixar_musica("Envolver")  # ERRO!
    except NotImplementedError as e:
        print(f"ERRO: {e}")

    print("\n=== Usuário Premium ===")
    premium.reproduzir_musica("Envolver - Anitta")
    premium.baixar_musica("Envolver - Anitta")
    try:
        premium.publicar_album("Meu Album")  # ERRO!
    except NotImplementedError as e:
        print(f"ERRO: {e}")

    print("\n=== Artista ===")
    artista.publicar_album("Versions of Me")
    artista.ver_estatisticas()
