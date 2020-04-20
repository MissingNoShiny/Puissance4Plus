# coding: utf-8

import json
import os
import sys
from os import path
from configparser import ConfigParser

from flask import Flask, request, send_from_directory, render_template, redirect
from PyQt5 import QtCore, QtMultimedia
from webui import WebUI

from puissance4plus.board import *


class UI(WebUI):
    def __init__(self, app: Flask, debug=False):
        super().__init__(app, debug=debug)
        self.view.setWindowTitle('Puissance 4 SUPER')
        self.view.setMinimumSize(1280, 720)
        self.player = QtMultimedia.QMediaPlayer(flags=QtMultimedia.QMediaPlayer.LowLatency)
        self.playlist = QtMultimedia.QMediaPlaylist()
        media_folder = path.join(app.static_folder, "audio")
        url = QtCore.QUrl.fromLocalFile(path.join(media_folder, "background.wma"))
        media = QtMultimedia.QMediaContent(url)
        self.playlist.addMedia(media)
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.player.setPlaylist(self.playlist)
        self.player.play()

    def set_fullscreen(self, fullscreen):
        if fullscreen:
            self.view.showFullScreen()
        else:
            self.view.showNormal()

    def set_volume(self, volume):
        self.player.setVolume(volume)

class Game:

    FOLDER_NAME = ".puissance4"

    def __init__(self):
        self.app = Flask(__name__)
        self.ui = UI(self.app, debug=True)
        # NO CACHE
        self.app.config["CACHE_TYPE"] = "null"

        try:
            self.app.root_path = sys._MEIPASS
        except AttributeError:
            pass
            # self.app.root_path = os.getcwd()

        self.game_directory = path.join(path.expanduser("~"), self.FOLDER_NAME)
        self.config = ConfigParser()
        if path.exists(path.join(self.game_directory, "config.ini")):
            self.config.read(path.join(self.game_directory, "config.ini"))
        else:
            self.config.read(path.join(self.app.static_folder, "config.ini"))

        self.language_data = {}
        self.update_settings()

        @self.app.route("/resource/<resource_path>")
        def get_resource(resource_path):
            # path = path.replace("/", path.sep)
            directories = {
                ".js": "js",
                ".css": "css",
                ".png": "image",
                ".jpg": "image",
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
            is_full_screen = "checked" if self.ui.view.isFullScreen() else "unchecked"
            return render_template('main_menu.html',
                                   is_full_screen=is_full_screen,
                                   lang=self.language_data["main_menu"],
                                   selected_lang=self.config.get("puissance4", "Language"))

        @self.app.route("/gameOptions", methods=['GET'])
        def game_options_menu():
            return render_template('game_options_menu.html',
                                   mode=request.args.get('mode'),
                                   lang=self.language_data)

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

        self.ui.run()

    def stop(self):
        self.ui.view.close()

    def load_language(self, language):
        language_folder = path.join(self.app.static_folder, "lang")
        if not path.isfile(path.join(language_folder, f"{language}.json")):
            language = "en"
        with open(path.join(language_folder, f"{language}.json"), "r", encoding="utf-8") as file:
            return json.load(file)

    def save_config(self):
        if not path.isdir(self.game_directory):
            os.mkdir(self.game_directory)
        with open(path.join(self.game_directory, "config.ini"), "w") as file:
            self.config.write(file)

    def update_settings(self):
        self.ui.set_fullscreen(self.config.getboolean("puissance4", "Fullscreen"))
        self.language_data = self.load_language(self.config.get("puissance4", "Language"))
        self.ui.set_volume(self.config.getint("puissance4", "Volume"))


if __name__ == "__main__":
    Game()
