# coding: utf-8

import os

import mimetypes
from flask import Flask, request, send_from_directory, render_template
from flaskwebgui import FlaskUI

mimetypes.init()
app = Flask(__name__)
ui = FlaskUI(app)


@app.route("/resource/<path:path>")
def get_resource(path):
    directories = {
        "application/js": "js",
        "text/css": "css",
        "image/png": "image",
        "image/jpeg": "image",
        "image/svg+xml": "image",
        "audio/mpeg": "audio",
        "audio/ogg": "audio",
        "font/ttf": "font"
    }
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.types_map.get(ext, "text/html")
    directory = directories.get(mimetype, "")
    directory_path = os.path.join("resources", directory)
    return send_from_directory(os.path.join(app.static_folder, directory_path), path)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    ui.run()
