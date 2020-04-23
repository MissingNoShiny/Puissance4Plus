# coding: utf-8

import json
import os
import sys
from os import path
from configparser import ConfigParser
from flask import Flask, request, send_from_directory, render_template, redirect, Response, jsonify
from PyQt5 import QtCore, QtMultimedia
from webui import WebUI

from puissance4plus.board import *


class UI(WebUI):
    def __init__(self, app: Flask, debug: bool = False):
        super().__init__(app, debug=debug)
        self.set_window_title()
        self.set_minimum_resolution()
        self.player = QtMultimedia.QMediaPlayer(flags=QtMultimedia.QMediaPlayer.LowLatency)
        self.set_volume(0)
        self.playlist = QtMultimedia.QMediaPlaylist()
        media_folder = path.join(app.static_folder, "audio")
        url = QtCore.QUrl.fromLocalFile(path.join(media_folder, "background.wav"))
        media = QtMultimedia.QMediaContent(url)
        self.playlist.addMedia(media)
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.player.setPlaylist(self.playlist)
        self.player.play()

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


class Game:
    FOLDER_NAME = ".puissance4"

    def __init__(self):
        self.app: Flask = Flask(__name__)
        # NO CACHE
        self.app.config["CACHE_TYPE"] = "null"

        try:
            self.app.root_path = path.join(sys._MEIPASS, "puissance4plus")
        except AttributeError:
            pass
            # self.app.root_path = os.getcwd()
        self.ui: UI = UI(self.app, debug=True)

        self.game_directory: str = path.join(path.expanduser("~"), self.FOLDER_NAME)
        self.config: ConfigParser = self.load_config()
        self.language_data: dict = {}
        self.stats_data: dict = self.load_stats()
        self.update_settings()
        self.board: Optional[Board] = None
        self.selected_mode: GameMode = GameMode.SOLO

        @self.app.route("/resource/<resource_path>")
        def get_resource(resource_path: str):
            # path = path.replace("/", path.sep)
            directories = {
                ".js": "js",
                ".css": "css",
                ".png": "image",
                ".jpg": "image",
                ".gif": "image",
                ".svg": "image",
                ".ico": "image",
                ".mp3": "audio",
                ".ogg": "audio",
                ".ttf": "font",
            }
            ext = path.splitext(resource_path)[1]
            directory = directories.get(ext, "")
            return send_from_directory(path.join(self.app.static_folder, directory), resource_path)

        @self.app.route("/")
        def main_menu():
            print(self.stats_data)
            is_full_screen = "checked" if self.ui.view.isFullScreen() else "unchecked"
            return render_template('main_menu.html',
                                   is_full_screen=is_full_screen,
                                   lang=self.language_data["main_menu"],
                                   rules=self.language_data["rules"],
                                   selected_lang=self.config.get("puissance4", "Language"),
                                   volume=self.ui.player.volume(),
                                   stats=self.stats_data)

        @self.app.route("/gameOptions", methods=['GET', 'POST'])
        def game_options_menu():
            if request.method == 'GET':
                if request.args.get("mode") != "SOLO":
                    self.selected_mode = GameMode.parse_mode(request.args.get("mode"))
                    return render_template('game_options_menu.html',
                                           mode=self.language_data[request.args.get('mode')],
                                           lang=self.language_data["game_options_menu"])
                else:
                    self.board = Board([Player(self.language_data["human"], "#FF0000"),
                                        Player(self.language_data["robot"], "#333333", player_type=PlayerType.AI)],
                                       game_mode=GameMode.SOLO)
                    return redirect('/game')
            else:
                data = request.json
                players = []
                for key in data["players"]:
                    players.append(Player(data["players"][key]['name'], data["players"][key]['color']))
                self.board = Board(players, int(data['width']), int(data['height']), int(data['win_condition']),
                                   game_mode=self.selected_mode)
                return Response(status='200')

        @self.app.route("/game", methods=['GET'])
        def render_game():
            if self.board is None:
                return redirect("/")
            return render_template('game_board.html',
                                   lang=self.language_data["game_board"])

        @self.app.route("/game", methods=['PUT'])
        def update_game():
            column = int(request.data)
            if column == -1:
                self.board.force_place()
            else:
                self.board.place(column)
            return Response(json.dumps(self.board.to_dict()), mimetype='application/json')

        @self.app.route("/game", methods=['POST'])
        def start_game():
            data = {
                "language_data": self.language_data,
                "board": self.board.to_dict()
            }
            return Response(json.dumps(data), mimetype='application/json')

        @self.app.route("/close")
        def close():
            self.stop()

        @self.app.route("/settings", methods=['GET'])
        def settings():
            fullscreen = False if request.args.get("fullscreen") is None else True
            self.config.set("puissance4", "Fullscreen", str(fullscreen))
            language = request.args.get("lang", "en")
            self.config.set("puissance4", "Language", language)
            volume = request.args.get("volume", 1)
            self.config.set("puissance4", "Volume", volume)
            self.save_config()
            self.update_settings()
            return redirect("/")

        @self.app.route("/giveUp")
        def give_up():
            self.board = None
            return redirect("/")

        @self.app.route("/endGame")
        def end_game():
            self.update_stats()
            self.board = None
            return redirect("/")

        self.ui.run()

    def stop(self) -> None:
        """
        Ferme le jeu
        """
        self.ui.view.close()

    def load_language(self, language: str) -> dict:
        """
        Lit et charge en mémoire un fichier de langue. Si la langue spécifiée est introuvable, la langue par défaut
        sera choisie à la place
        :param language: La langue à charger
        :return Un dictionnaire contenant les données de la langue à charger
        """
        language_folder = path.join(self.app.static_folder, "lang")
        if not path.isfile(path.join(language_folder, f"{language}.json")):
            language = "en"
        with open(path.join(language_folder, f"{language}.json"), "r", encoding="utf-8") as file:
            return json.load(file)

    def load_config(self):
        config = ConfigParser()
        if path.exists(path.join(self.game_directory, "config.ini")):
            config.read(path.join(self.game_directory, "config.ini"))
        else:
            config.read(path.join(self.app.static_folder, "config.ini"))
        return config

    def save_config(self) -> None:
        """
        Sauvegarde les paramètres dans le fichier de configuration
        """
        if not path.isdir(self.game_directory):
            os.mkdir(self.game_directory)
        with open(path.join(self.game_directory, "config.ini"), "w") as file:
            self.config.write(file)

    def update_settings(self) -> None:
        """
        Met à jour le jeu en fonction des paramètres
        """
        self.ui.set_fullscreen(self.config.getboolean("puissance4", "Fullscreen"))
        self.language_data = self.load_language(self.config.get("puissance4", "Language"))
        self.ui.set_window_title(self.language_data["main_menu"]["title"])
        self.ui.set_volume(self.config.getint("puissance4", "Volume"))

    def load_stats(self) -> dict:
        data = {}
        if path.exists(path.join(self.game_directory, "stats.json")):
            data = json.load(open(path.join(self.game_directory, "stats.json"), "r", encoding="utf-8"))
        else:
            data = json.load(open(path.join(self.app.static_folder, "stats.json"), "r", encoding="utf-8"))
        return data

    def update_stats(self) -> None:
        game_mode = str(self.board.game_mode)
        if self.board.game_mode == GameMode.SOLO:
            if self.board.state == BoardState.DRAW:
                self.stats_data[game_mode]["DRAW"] += 1
            elif self.board.state == BoardState.WON:
                if self.board.current_player.player_type == PlayerType.AI:
                    self.stats_data[game_mode]["LOSS"] += 1
                else:
                    self.stats_data[game_mode]["WIN"] += 1
        else:
            if self.board.state == BoardState.DRAW:
                for player in self.board.players:
                    self.update_stat(player, game_mode, "DRAW")
            elif self.board.state == BoardState.WON:
                for player in self.board.players:
                    if player == self.board.current_player:
                        self.update_stat(player, game_mode, "WIN")
                    else:
                        self.update_stat(player, game_mode, "LOSS")
        self.save_stats()

    def update_stat(self, player, game_mode, outcome):
        if player.name not in self.stats_data[game_mode][outcome]:
            self.stats_data[game_mode][outcome][player.name] = 1
        else:
            self.stats_data[game_mode][outcome][player.name] += 1

    def save_stats(self) -> None:
        if not path.isdir(self.game_directory):
            os.mkdir(self.game_directory)
        with open(path.join(self.game_directory, "stats.json"), "w", encoding="utf-8") as file:
            json.dump(self.stats_data, file)

    def reset_stats(self) -> None:
        try:
            os.remove(path.join(self.game_directory, "stats.json"))
        except OSError:
            pass
        self.stats_data = self.load_stats()
