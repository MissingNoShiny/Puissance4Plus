# coding: utf-8

import os

from flask import Flask, request, send_from_directory, render_template
from webui import WebUI


class UI(WebUI):
    def __init__(self, app, debug=False):
        super().__init__(app, debug=debug)
        self.view.showFullScreen()


class Game:
    def __init__(self):
        self.app = Flask(__name__)
        self.ui = UI(self.app, debug=True)

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
        def index():
            return render_template('main_menu.html')

        @self.app.route("/close")
        def close():
            self.stop()

        self.ui.run()

    def stop(self):
        self.ui.view.close()


if __name__ == "__main__":
    Game()
