# coding: utf-8

__author__ = "Mathias Billot, Xavier Hoyois, Nicolas Jeuniaux, Vincent Larcin, Maxence Manteau"
__version__ = "1.0"
__status__ = "Production"

from os import path

from PyQt5 import QtCore, QtMultimedia, QtWebEngineWidgets, QtWidgets


class UI:
    def __init__(self, static_folder: str, port: int):
        self.static_folder: str = static_folder
        self.url: str = f"http://127.0.0.1:{port}"

        self.app: QtWidgets.QApplication = QtWidgets.QApplication([])
        self.view: QtWebEngineWidgets.QWebEngineView = QtWebEngineWidgets.QWebEngineView(self.app.activeModalWidget())
        self.set_minimum_resolution()

        self.playlist: QtMultimedia.QMediaPlaylist = QtMultimedia.QMediaPlaylist()
        self.player: QtMultimedia.QMediaPlayer = QtMultimedia.QMediaPlayer(flags=QtMultimedia.QMediaPlayer.LowLatency)
        self.initialize_player()

    def run(self) -> None:
        self.view.load(QtCore.QUrl(self.url))
        self.view.page().settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalStorageEnabled, True)
        self.view.show()
        self.app.exec_()

    def stop(self):
        """
        Ferme la fenêtre et stoppe le programme
        :return:
        """
        self.view.close()

    def set_fullscreen(self, fullscreen: bool) -> None:
        """
        Change l'état de plein écran de la fenêtre de jeu
        :param fullscreen: True pour passer la fenêtre en plein écran, False pour la minimiser
        """
        if fullscreen:
            self.view.showFullScreen()
        else:
            self.view.showNormal()

    def set_volume(self, volume: int) -> None:
        """
        Change le volume de la musique de fond
        :param volume: Le nouveau volume
        """
        self.player.setVolume(volume)

    def set_minimum_resolution(self, height: int = 720, width: int = 1280) -> None:
        """
        Change la résolution minimale de la fenêtre de jeu
        :param height: La hauteur de la fenêtre, en pixels
        :param width: La largeur de la fenêtre, en pixels
        """
        self.view.setMinimumSize(width, height)

    def set_window_title(self, name: str = 'Puissance 4 SUPER') -> None:
        """
        Change le nom de la fenêtre de jeu
        :param name: Nom de la fenêtre
        """
        self.view.setWindowTitle(name)

    def initialize_player(self) -> None:
        """
        Initialise le lecteur de musique
        """
        self.set_volume(0)
        media_folder = path.join(self.static_folder, "audio")
        url = QtCore.QUrl.fromLocalFile(path.join(media_folder, "background.wav"))
        media = QtMultimedia.QMediaContent(url)
        self.playlist.addMedia(media)
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.player.setPlaylist(self.playlist)
        self.player.play()
