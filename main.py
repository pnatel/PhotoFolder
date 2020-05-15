#!/usr/bin/env python3

from flask import Flask, flash, render_template, request, redirect
import os
import FileModule as fm
import app_config as cfg

# os.environ.get("ENV_VAR_NAME")


app = Flask(__name__)
app.secret_key = "Zcg,ddh}k^Q(uh/~qM*PT!cJ5?/Q$3QQ"

@app.route('/')
@app.route('/', methods = ['GET', 'POST'])
def index():
    list = fm.getListOfFiles(cfg._destinationFolder)
    if request.method == 'GET':
        return load_pics(list, title='List of Pictures')

    else:
        payload = request.get_data().decode("utf-8")
        flash(payload, 'debug')
        if request.form.get('left'):
            rotate(payload, list, 'left')
            list = fm.getListOfFiles(cfg._destinationFolder)
            return load_pics(list, title='ROTATED Pictures')

        elif request.form.get('right'):
            rotate(payload, list, 'right')
            list = fm.getListOfFiles(cfg._destinationFolder)
            return load_pics(list, title='ROTATED Pictures')

        elif request.form.get('favorite'):
            flash('FAVORITE.', 'warning')
            return load_pics(list, title='FAVORITE Pictures')

        elif request.form.get('delete'):
            delete(payload, list)
            list = fm.getListOfFiles(cfg._destinationFolder)
            return load_pics(list, title='Remaining Pictures')

        elif request.form.get('manual_copy'):
            fm.main()
            list = fm.getListOfFiles(cfg._destinationFolder)
            return load_pics(list, title='New Set of Pictures')

        else:
            flash('No option selected, try again.', 'error')
            return load_pics(list, title='List of Pictures')

def load_pics(list, page='index.html', title=''):
    flash('Files loaded: ' + str(len(list)), 'info')
    return render_template(page, title=title, \
            images=list, len_list=len(list))

def rotate(payload, list, side):
    for i  in range(len(list)):
        if list[i] in payload:
            # flash(list[i], 'warning')
            message = fm.fileRotate(list[i], side)
            flash(message, 'warning')
        # flash('.', 'info')

def delete(payload, list):
    # flash(request.get_data(), 'message')
    for i  in range(len(list)):
        if list[i] in payload:
            # flash(list[i], 'warning')
            message = fm.filePrunning(list[i])
            flash(message, 'warning')
        # flash('.', 'info')

@app.route('/config', methods = ['GET', 'POST'])
def config():
    if request.method == 'GET':
        with open("config.ini", "r") as f:
            return render_template('config.html', \
                config_file=f.read(), \
                title='Active Config')
    else:
        try:
            if os.path.exists('config.old'):
                os.remove('config.old')
            os.rename('config.ini', 'config.old')
            flash('Backup original config', 'info')
            with open('config.ini', 'w') as f:
                f.write(request.form.get('config'))
                flash('Config saved', 'info')
            f.close()
            return redirect('/') 
        except IOError as e:
            flash(e, 'error')
             
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=23276, debug=0)