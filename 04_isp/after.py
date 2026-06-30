"""
ISP - Interface Segregation Principle (DEPOIS)
Cenário: Sistema de usuários inspirado no Spotify

Solução: Interfaces pequenas e específicas. Cada tipo de usuário
implementa APENAS as interfaces que fazem sentido para ele.
"""

from abc import ABC, abstractmethod


class Reprodutor(ABC):
    """Interface: quem pode ouvir músicas."""

    @abstractmethod
    def reproduzir_musica(self, musica: str) -> None:
        ...


class PuladorMusica(ABC):
    """Interface: quem pode pular músicas sem limite."""

    @abstractmethod
    def pular_musica(self) -> None:
        ...


class BaixadorMusica(ABC):
    """Interface: quem pode baixar músicas offline."""

    @abstractmethod
    def baixar_musica(self, musica: str) -> None:
        ...


class CriadorPlaylist(ABC):
    """Interface: quem pode criar playlists."""

    @abstractmethod
    def criar_playlist(self, nome: str) -> None:
        ...


class VisualizadorAnuncios(ABC):
    """Interface: quem visualiza anúncios."""

    @abstractmethod
    def ver_anuncios(self) -> None:
        ...


class PublicadorConteudo(ABC):
    """Interface: quem pode publicar conteúdo na plataforma."""

    @abstractmethod
    def publicar_album(self, album: str) -> None:
        ...

    @abstractmethod
    def agendar_lancamento(self, data: str) -> None:
        ...


class AnalistaEstatisticas(ABC):
    """Interface: quem pode ver estatísticas de artista."""

    @abstractmethod
    def ver_estatisticas(self) -> None:
        ...


class UsuarioGratis(Reprodutor, CriadorPlaylist, VisualizadorAnuncios):
    """Usuário gratuito: ouve músicas, cria playlists e vê anúncios.
    NÃO pode pular, baixar ou publicar — e nem precisa implementar!"""

    def __init__(self, nome: str):
        self.nome = nome
        self.pulos_restantes = 6

    def reproduzir_musica(self, musica: str) -> None:
        print(f"[FREE] {self.nome} ouvindo: {musica}")

    def criar_playlist(self, nome: str) -> None:
        print(f"[FREE] {self.nome} criou playlist: {nome}")

    def ver_anuncios(self) -> None:
        print(f"[FREE] Exibindo anúncio para {self.nome}...")

    def tentar_pular(self) -> None:
        """Pular com limite (não é a interface PuladorMusica sem limite)."""
        if self.pulos_restantes > 0:
            self.pulos_restantes -= 1
            print(f"[FREE] {self.nome} pulou! ({self.pulos_restantes} pulos restantes)")
        else:
            print(f"[FREE] {self.nome} sem pulos disponíveis!")


class UsuarioPremium(Reprodutor, PuladorMusica, BaixadorMusica, CriadorPlaylist):
    """Usuário premium: tudo do grátis + pular sem limite + baixar offline.
    SEM anúncios, SEM funcionalidades de artista."""

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


class Artista(Reprodutor, PuladorMusica, BaixadorMusica, PublicadorConteudo, AnalistaEstatisticas):
    """Artista: ouve + pula + baixa + publica + vê estatísticas.
    NÃO precisa de playlist nem de anúncios."""

    def __init__(self, nome: str):
        self.nome = nome

    def reproduzir_musica(self, musica: str) -> None:
        print(f"[ARTISTA] {self.nome} ouvindo: {musica}")

    def pular_musica(self) -> None:
        print(f"[ARTISTA] {self.nome} pulou a música!")

    def baixar_musica(self, musica: str) -> None:
        print(f"[ARTISTA] {self.nome} baixou: {musica}")

    def publicar_album(self, album: str) -> None:
        print(f"[ARTISTA] {self.nome} publicou o álbum: {album}")

    def agendar_lancamento(self, data: str) -> None:
        print(f"[ARTISTA] {self.nome} agendou lançamento para {data}")

    def ver_estatisticas(self) -> None:
        print(f"[ARTISTA] {self.nome} - 1.5M ouvintes mensais")


def reproduzir_para_todos(usuarios: list[Reprodutor], musica: str) -> None:
    """Aceita qualquer um que implemente Reprodutor."""
    for usuario in usuarios:
        usuario.reproduzir_musica(musica)


def baixar_offline(usuarios: list[BaixadorMusica], musica: str) -> None:
    """Aceita APENAS quem pode baixar — sem erros em runtime!"""
    for usuario in usuarios:
        usuario.baixar_musica(musica)


if __name__ == "__main__":
    gratis = UsuarioGratis("Maria")
    premium = UsuarioPremium("João")
    artista = Artista("Anitta")

    print("=== Todos podem ouvir ===")
    reproduzir_para_todos([gratis, premium, artista], "Envolver - Anitta")

    print("\n=== Só premium e artista podem baixar ===")
    baixar_offline([premium, artista], "Envolver - Anitta")

    print("\n=== Funcionalidades específicas ===")
    gratis.ver_anuncios()
    gratis.tentar_pular()

    premium.pular_musica()
    premium.criar_playlist("Meus Favoritos")

    artista.publicar_album("Versions of Me")
    artista.ver_estatisticas()
    artista.agendar_lancamento("01/08/2025")
