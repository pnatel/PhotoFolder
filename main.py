#!/usr/bin/env python3

from flask import Flask, flash, render_template, request
import os
import FileModule as fm

# os.environ.get("ENV_VAR_NAME")

pic_folder = fm.ConfigSectionMap('folder')['destinationfolder']
# pic_folder = fm.ConfigSectionMap('test')['destinationfolder']

app = Flask(__name__)
app.secret_key = "Zcg,ddh}k^Q(uh/~qM*PT!cJ5?/Q$3QQ"

@app.route('/')
@app.route('/', methods = ['GET', 'POST'])
def index():  
    list = fm.getListOfFiles(pic_folder)
    if request.method == 'GET':
        return load_pics(list, title='List of Pictures')

    else:
        payload = request.get_data().decode("utf-8")
        if request.form.get('rotate'):
            rotate(payload, list)
            list = fm.getListOfFiles(pic_folder)
            return load_pics(list, title='ROTATED Pictures')

        elif request.form.get('favorite'):
            flash('FAVORITE.', 'warning')
            return load_pics(list, title='FAVORITE Pictures')

        elif request.form.get('delete'): 
            delete(payload, list)
            list = fm.getListOfFiles(pic_folder)
            return load_pics(list, title='Remaining Pictures')

        elif request.form.get('manual_copy'):
            fm.main()
            list = fm.getListOfFiles(pic_folder)
            return load_pics(list, title='New Set of Pictures')

        else:
            flash('No option selected, try again.', 'error')
            return load_pics(list, title='List of Pictures')

def load_pics(list, page='index.html', title=''):
    flash('Files loaded: ' + str(list), 'info')
    return render_template(page, title=title, \
            images=list, len_list=len(list))

def rotate(payload, list):
    for i  in range(len(list)):
        if list[i] in payload:
            # flash(list[i], 'warning')
            message = fm.fileRotate(list[i])
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=88, debug=0)