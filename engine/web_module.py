#!/usr/bin/env python3

from flask import Flask, flash, render_template, request, redirect
import os, time
from werkzeug.serving import run_simple
from distutils.util import strtobool
# Running as standalone or part of the application
if __name__ == '__main__' or __name__ == 'web_module':
    from FileModule import getListOfFiles, copy_job, fileRotate, filePrunning
    import app_config as cfg
    import list_module as ls
else: 
    from engine.FileModule import getListOfFiles, copy_job, fileRotate, filePrunning
    import engine.app_config as cfg
    import engine.list_module as ls

# set to True to inform that the app needs to be re-created
to_reload = False

# os.environ.get("ENV_VAR_NAME")
cfg.load_config()

def get_app():
    print("create app now")
    app = Flask(__name__)
    app.secret_key = "Zcg,ddh}k^Q(uh/~qM*PT!cJ5?/Q$3QQ"

    @app.route('/')
    @app.route('/', methods = ['GET', 'POST'])
    def index():
        list = getListOfFiles(cfg._destinationFolder)
        if request.method == 'GET':
            return load_pics(list, title='List of Pictures')

        else:
            payload = request.get_data().decode("utf-8")
            # only shows debug if in demo mode
            if bool(strtobool(cfg._test.capitalize())):
                flash(payload, 'debug')
            if request.form.get('left'):
                rotate(payload, list, 'left')
                title='ROTATED Pictures'

            elif request.form.get('right'):
                rotate(payload, list, 'right')
                title='ROTATED Pictures'
                
            elif request.form.get('favorite'):
                faves = ls.common(payload, list)
                flash('FAVORITED {}'.format(faves), 'info')
                ls.append_multiple_lines('config/whitelist.txt', faves)
                title='FAVORITE Pictures'

            elif request.form.get('delete'):
                delete(payload, list)
                black = ls.common(payload, list)
                flash('BLACKLISTED {}'.format(black), 'info')
                ls.append_multiple_lines('config/blacklist.txt', black)
                title='Remaining Pictures'

            elif request.form.get('copy_job'):
                copy_job()
                flash('Copy Job completed.', 'warning')
                title='New Set of Pictures'

            else:
                # This should never be triggered
                flash('No option selected, try again.', 'error')
                title='List of Pictures'

            list = getListOfFiles(cfg._destinationFolder)    
            return load_pics(list, title=title)

    def load_pics(list, page='index.html', title=''):
        flash('Files loaded: ' + str(len(list)), 'message')
        return render_template(page, title=title, \
                images=list, len_list=len(list), \
                extra_list=(read_file('config/whitelist.txt')))

    def rotate(payload, list, side):
        for i  in range(len(list)):
            if list[i] in payload:
                flash(list[i], 'warning')
                fileRotate(list[i], side)
            # flash('.', 'info')

    def delete(payload, list):
        # flash(request.get_data(), 'message')
        for i  in range(len(list)):
            if list[i] in payload:
                flash(list[i], 'warning')
                filePrunning(list[i])
            # flash('.', 'info')

    def read_file(file):
        try:
            with open(file, 'r') as f:
                return f.read()
        except IOError as e:
            flash('Operation failed: {}'.format(e.strerror), 'error')
    
    def write_file(file, content):
        try:
            if os.path.exists(file+'_old'):
                os.remove(file+'_old')
                flash('removing backup file', 'info')
            os.rename(file, file+'_old')
            flash('Backup original configuration to {}_old'.format(file), 'info')
            with open(file, 'w') as f:
                f.write(content)
                flash('File saved on {}'.format(file), 'info')
        except IOError as e:
            flash(e, 'error')


    @app.route('/config', methods = ['GET', 'POST'])
    def config():
        if request.method == 'GET':
            return render_template('config.html', \
                config_file=read_file('config/config.ini'), \
                title='Active Config')
        else:
            write_file('config/config.ini', request.form.get('config'))
            flash('RESTART THE APPLICATION FOR THE NEW SETTINGS TO GET EFFECT', 'critical')
            reload()
            return redirect('/config') 


    @app.route('/blacklist', methods = ['GET', 'POST'])
    def blacklist():
        if request.method == 'GET':
            return render_template('blacklist.html', \
                blacklist=read_file('config/blacklist.txt'), \
                title='Blacklisted files')
        else:
            write_file('config/blacklist.txt', request.form.get('blacklist'))
            return redirect('/blacklist') 


    @app.route('/whitelist', methods = ['GET', 'POST'])
    def whitelist():
        if request.method == 'GET':
            return render_template('whitelist.html', \
                whitelist=read_file('config/whitelist.txt'), \
                title='whitelisted files')
        else:
            write_file('config/whitelist.txt', request.form.get('whitelist'))
            flash('New whitelist file saved', 'info')
            return redirect('/whitelist') 


    @app.route('/reload')
    def reload():
        global to_reload
        to_reload = True
        flash('Reloading completed', 'info')
        return 'reloaded'

    return app


class AppReloader(object):
    def __init__(self, create_app):
        self.create_app = create_app
        self.app = create_app()

    def get_application(self):
        global to_reload
        if to_reload:
            self.app = self.create_app()
            to_reload = False
        cfg.load_config()
        return self.app

    def __call__(self, environ, start_response):
        app = self.get_application()
        return app(environ, start_response)

def website():
    # change reloader and debugger to false in production
    test = bool(strtobool(cfg._test.capitalize()))
    print('Loading DEMO mode? ', test)
    run_simple('0.0.0.0', int(cfg._port), application,
               use_reloader=test, use_debugger=test, use_evalex=True)

# This application object can be used in any WSGI server
# for example in gunicorn, you can run "gunicorn app"
application = AppReloader(get_app)

if __name__ == '__main__':
    website()