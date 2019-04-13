#!/usr/bin/python3

import random
import string
from file_handler import FileHandler
import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, abort, send_file
from werkzeug.utils import secure_filename
from Video_Creation.video_maker import VideoMaker

DIRNAME = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(DIRNAME, 'uploaded_files')

app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

FH = FileHandler()
VM = VideoMaker()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/set_video', methods=['GET', 'POST'])
def set_video():
    if request.method == "POST":

        # Video settings
        settings_dict = {}
        settings_dict['resolution'] = request.form.get('resolution')
        settings_dict['format'] = request.form.get('filetype')
        settings_dict['font'] = request.form.get('font')
        settings_dict['name'] = request.form.get('filename')
        settings_dict['gender'] = request.form.get('gender')
        settings_dict['age'] = request.form.get('age')
        settings_dict['price'] = request.form.get('pricename')
        settings_dict['product'] = request.form.get('productname')
        settings_dict['brand'] = request.form.get('brandname')
        settings_dict['sale'] = request.form.get('salename')
        settings_dict['video_id'] = request.form.get('u_id')

        # create directory and subdirectories for new user
        user_id = request.form.get('u_id')
        FH.create_user_folder(user_id)
        FH.create_subdir_in_user(user_id)

        products_dir = FH.get_user_dir_products(user_id)
        stickers_dir = FH.get_user_dir_stickers(user_id)
        bg_dir = FH.get_user_dir_background(user_id)

        # Save files in subdirectories
        if 'products' in request.files:
            prod_list = request.files.getlist('products')
            for prod in prod_list:
                prod_name = secure_filename(prod.filename)
                prod.save(os.path.join(products_dir, prod_name))
        if 'stickers' in request.files:
            sticker_list = request.files.getlist('stickers')
            for sticker in sticker_list:
                sticker_name = secure_filename(sticker.filename)
                sticker.save(os.path.join(stickers_dir, sticker_name))
        if 'background' in request.files:
            bg_list = request.files.getlist('background')
            for bg in bg_list:
                bg_name = secure_filename(bg.filename)
                bg.save(os.path.join(bg_dir, bg_name))
        # CALL VIDEO GEN ALGORITHM HERE
        VM.generate_video(settings_dict)

        return redirect(url_for('video', id=user_id, name=settings_dict['name'], ext=settings_dict['format']))
    else:
        letters = string.ascii_lowercase
        user_id = ''.join(random.choice(letters) for i in range(20))
        return render_template('set_video.html', user_id=user_id)

@app.route('/video')
def video():
        user_id = request.args.get('id')
        vid_name = request.args.get('name')
        ext = request.args.get('ext')
        vid_dir = FH.get_video_path(user_id)
        vid_path = vid_dir + "/" + vid_name + "." + ext
        return send_file(vid_path, as_attachment=True)
