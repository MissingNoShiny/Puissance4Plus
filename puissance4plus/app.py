# coding: utf-8

import os

import mimetypes
from flask import Flask, request, send_from_directory, render_template
from flaskwebgui import FlaskUI

app = Flask(__name__)
ui = FlaskUI(app)


@app.route("/resource/<path:path>")
def get_resource(path):
    path = path.replace("/", os.path.sep)
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
    return send_from_directory(os.path.join(app.static_folder, directory), path)


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    ui.run()
