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
        self.view.showFullScreen()


class GameSettings:

    DIRECTORY_NAME = "puissance4"

    def __init__(self, static_directory):
        self.directory = os.path.join(os.path.expanduser("~"), self.DIRECTORY_NAME)
        self.config = ConfigParser.ConfigParser()
        if os.path.isdir(self.directory):
            self.config.read(os.path.join(self.directory, "config.ini"))
        else:
            os.mkdir(self.directory)
            self.config.read(os.path.join(static_directory), "config.ini")

    def save_config(self):
        with open(os.path.join(self.directory, "config.ini"), "w") as file:
            self.config.write(file)


class Game:
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

        self.settings = GameSettings(self.app.root_path)

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
        def mainMenu():
            status = "checked" if(self.ui.view.isFullScreen()) else "unchecked"
            return render_template('main_menu.html', status=status)

        @self.app.route("/gameOptions", methods=['GET'])
        def gameOptionsMenu():
            return render_template('game_options_menu.html', mode=request.args.get('mode'))

        @self.app.route("/close")
        def close():

            self.stop()

        @self.app.route("/settings", methods=['GET'])
        def graphicalOptions():
            self.toggleFullscreen(request.args.get('fullscreen'))
            return redirect("/")

        self.ui.run()

    def stop(self):
        self.settings.save_config()
        self.ui.view.close()

    def load_language(self, language):
        language_folder = os.path.join(self.app.static_folder, "lang")
        with open(os.path.join(language_folder, f"{language}.txt"), "r") as file:
            data = json.load(file)
            
    def toggleFullscreen(self, fullscreen):
        if fullscreen:
            self.ui.view.showFullScreen()
        else:
            self.ui.view.showNormal()


if __name__ == "__main__":
    Game()
