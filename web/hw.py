#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'bp'
__version__ = (0, 0, 1)

import os
from flask import Flask, render_template, request, redirect, url_for

from settings import BASICAUTH, STORAGEPATH
from utils import requires_auth
from common.storage import IndexFileStorage

ALLOWED_EXTENSIONS = ['bin', 'txt', 'odt', 'pdf']

app = Flask(__name__)
IndexFileStorage.root = STORAGEPATH
ifs = IndexFileStorage()
app.config['UPLOAD_FOLDER'] = STORAGEPATH


@app.route('/')
@requires_auth
def secret_page():
    user = BASICAUTH[request.authorization.username]
    file_set = ifs.list(user.username)
    return render_template('index.html', user=user, file_set=file_set)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
@requires_auth
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename + '.tmp'
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(os.path.join(filepath))
            try:
                ifs.add_file(request.authorization.username, file.filename, open(filepath, 'rb').read())
            except IndexFileStorage.FileExists as error:
                return render_template('error.html', error=error)
            finally:
                os.unlink(filepath)
            return redirect('/')
            return redirect(url_for('show_file', filename=filename))
    return render_template('upload.html')


@app.route('/<filename>/del')
@requires_auth
def delete_file(filename):
    try:
        ifs.del_file(request.authorization.username, filename)
        return redirect('/')
    except IndexFileStorage.FileNotFound as error:
        return render_template('error.html', error=error)


if __name__ == "__main__":
    app.run(debug=True)