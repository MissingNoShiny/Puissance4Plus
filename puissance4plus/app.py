# coding: utf-8

import json
import os
import sys
from configparser import ConfigParser

from flask import Flask, request, send_from_directory, render_template, redirect
from webui import WebUI


class UI(WebUI):
    def __init__(self, app, debug=False):
        super().__init__(app, debug=debug)
        self.view.setWindowTitle('Puissance 4 SUPER')
        self.view.setMinimumSize(1280, 720)

    def set_fullscreen(self, fullscreen):
        print(fullscreen)
        if fullscreen:
            self.view.showFullScreen()
        else:
            self.view.showNormal()

class Game:

    FOLDER_NAME = "puissance4"

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

        self.game_directory = os.path.join(os.path.expanduser("~"), self.FOLDER_NAME)
        self.config = ConfigParser()
        if os.path.exists(os.path.join(self.game_directory, "config.ini")):
            self.config.read(os.path.join(self.game_directory, "config.ini"))
        else:
            self.config.read(os.path.join(self.app.static_folder, "config.ini"))

        self.update_settings()

        @self.app.route("/resource/<path:path>")
        def get_resource(path):
            # path = path.replace("/", os.path.sep)
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
            ext = os.path.splitext(path)[1]
            directory = directories.get(ext, "")
            return send_from_directory(os.path.join(self.app.static_folder, directory), path)

        @self.app.route("/")
        def main_menu():
            status = "checked" if(self.ui.view.isFullScreen()) else "unchecked"
            return render_template('main_menu.html', status=status)

        @self.app.route("/gameOptions", methods=['GET'])
        def game_options_menu():
            return render_template('game_options_menu.html', mode=request.args.get('mode'))

        @self.app.route("/close")
        def close():
            self.stop()

        @self.app.route("/settings", methods=['GET'])
        def settings():
            fullscreen = False if request.args.get("fullscreen") is None else True
            self.config.set("puissance4", "Fullscreen", str(fullscreen))
            self.update_settings()
            return redirect("/")

        self.ui.run()

    def stop(self):
        self.save_config()
        self.ui.view.close()

    def load_language(self, language):
        language_folder = os.path.join(self.app.static_folder, "lang")
        with open(os.path.join(language_folder, f"{language}.txt"), "r") as file:
            data = json.load(file)

    def save_config(self):
        if not os.path.isdir(self.game_directory):
            os.mkdir(self.game_directory)
        with open(os.path.join(self.game_directory, "config.ini"), "w") as file:
            self.config.write(file)

    def update_settings(self):
        self.ui.set_fullscreen(self.config.getboolean("puissance4", "Fullscreen"))


if __name__ == "__main__":
    Game()
