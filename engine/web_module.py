#!/usr/bin/env python3

from flask import Flask, flash, render_template, request, redirect
import os
import pandas as pd
from werkzeug.serving import run_simple
# from distutils.util import strtobool
from flask_thumbnails import Thumbnail
# Running as standalone or part of the application
if __name__ == '__main__' or __name__ == 'web_module':
    import app_config as cfg
    cfg.load_config()
    if cfg._DataMode == 'txt':
        import FileModule as db
    elif cfg._DataMode == 'csv':
        import csv_module as db
    elif cfg._DataMode == 'mongo':
        import mongodb_module as db
    else:
        print('''
>>>>>>>>>Failed to load the database<<<<<<<<

This is usually due a typo in the config.ini
Check data/config.ini > parameters.
Reloading basic txt mode to keep you running.
''')
#        import FileModule as db
#    import setup as stp
else:
    import engine.app_config as cfg
    cfg.load_config()
    if cfg._DataMode == 'txt':
        import engine.FileModule as db
    elif cfg._DataMode == 'csv':
        import engine.csv_module as db
    elif cfg._DataMode == 'mongo':
        import engine.mongodb_module as db
    else:
        print('''
>>>>>>>>>Failed to load the database<<<<<<<<

This is usually due a typo in the config.ini
Check data/config.ini > parameters.
Reloading basic txt mode to keep you running.
''')
#        import engine.FileModule as db
#    import engine.setup as stp

# Check configuration files and create any missing file
# stp.setup()

# set to True to inform that the app needs to be re-created
to_reload = False

# os.environ.get("ENV_VAR_NAME")


def get_app():
    print("create app now")
    app = Flask(__name__)
    thumb = Thumbnail(app)
    app.secret_key = "Zcg,ddh}k^Q(uh/~qM*PT!cJ5?/Q$3QQ"
    app.config['THUMBNAIL_MEDIA_ROOT'] = os.getcwd()+'/'+cfg._destinationFolder
    app.config['THUMBNAIL_MEDIA_URL'] = cfg._destinationFolder
    app.config['THUMBNAIL_MEDIA_THUMBNAIL_ROOT'] = (os.getcwd() + '/' +
                                                    cfg._destinationFolder +
                                                    '/thumbnail/')
    app.config['THUMBNAIL_MEDIA_THUMBNAIL_URL'] = '/thumbnail/'

    print('path to pics', os.getcwd()+'/'+cfg._destinationFolder)

    @app.route('/')
    @app.route('/', methods=['GET', 'POST'])
    def index():
        list = db.getListOfFiles(cfg._destinationFolder, add_path=False)
        # flash(list, 'debug')
        if request.method == 'GET':
            return load_pics(list, title='List of Pictures')

        else:
            payload = request.get_data().decode("utf-8")
            # only shows debug if in demo mode
            if cfg._test:
                flash(payload, 'debug')

            if request.form.get('left'):
                rotate(payload, list, 'left')
                title = 'ROTATED Pictures'

            elif request.form.get('right'):
                rotate(payload, list, 'right')
                title = 'ROTATED Pictures'

            elif request.form.get('180'):
                rotate(payload, list, '180')
                title = 'UPSIDE-DOWN Pictures'

            elif request.form.get('favorite'):
                faves = db.common(payload, list)
                flash('FAVORITED {} pics'.format(len(faves)), 'warning')
                if cfg._DataMode == 'txt':
                    db.append_multiple_lines('data/whitelist.txt', faves)
                elif cfg._DataMode == 'csv':
                    for fave in faves:
                        db.update_record_csv(fave, cfg._csvDB, favorite=True)
                title = 'FAVORITE Pictures'

            elif request.form.get('delete'):
                delete(payload, list)
                black = db.common(payload, list)
                if cfg._DataMode == 'txt':
                    # Check for common with whitelist
                    fave_removed = db.remove_common_from_file(
                        'data/whitelist.txt', black)
                    # only shows debug if in demo mode
                    if cfg._test:
                        flash(f'Removed {len(fave_removed)} Fave pics',
                              'debug')
                    db.append_multiple_lines('data/blacklist.txt', black)
                flash('BLACKLISTED {} pics'.format(len(black)), 'info')
                title = 'Remaining Pictures'

            elif request.form.get('copy_job'):
                db.copy_job()
                flash('Copy Job completed.', 'warning')
                title = 'New Set of Pictures'

            else:
                # This should never be triggered
                flash('No option selected, try again.', 'error')
                title = 'List of Pictures'

            list = db.getListOfFiles(cfg._destinationFolder, add_path=False)
            return load_pics(list, title=title)

    def load_pics(list, page='index.html', title='', extra_list=[]):
        flash('Files loaded: ' + str(len(list)), 'message')
        if cfg._DataMode == 'txt':
            extra_list = read_file('data/whitelist.txt')
        elif cfg._DataMode == 'csv':
            faves = db.filter_record_csv(favorite=True)
            extra_list = []
            for fave in faves:
                extra_list.append(fave['filename'])
        return render_template(page, title=title,
                               images=list, len_list=len(list),
                               path=cfg._destinationFolder[7:],
                               extra_list=extra_list)

    def rotate(payload, list, side):
        pic = 0
        for i in range(len(list)):
            if list[i] in payload:
                pic += 1
                # flash(list[i], 'warning')
                db.fileRotate(cfg._destinationFolder, list[i], side)
        flash('Rotating {} pics to {}'.format(pic, side), 'warning')

    def delete(payload, list):
        # flash(request.get_data(), 'message')
        pic = 0
        for i in range(len(list)):
            if list[i] in payload:
                pic += 1
                # flash(list[i], 'warning')
                db.filePrunning(list[i])
        flash('Deleting {} pics'.format(pic), 'warning')

    def read_file(file):
        try:
            # print(file)
            with open(file, 'r') as f:
                # print(f.read())
                return f.read()
        except IOError as e:
            flash('Operation failed: {}'.format(e.strerror), 'error')

    def write_file(file, content):
        try:
            if os.path.exists(file+'_old'):
                os.remove(file+'_old')
                flash('removing backup file', 'info')
            os.rename(file, file+'_old')
            flash('Backup original configuration to {}_old'.format(file),
                  'info')
            if len(content) > 0:
                with open(file, 'w') as f:
                    f.write(content)
                    flash('File saved on {}'.format(file), 'info')
            else:
                flash('File writing failed, restoring original', 'error')
                os.copy(file+'_old', file)
        except IOError as e:
            flash(e, 'error')

    @app.route('/copy_job')
    def copy_job():
        db.copy_job()
        flash('Copy Job completed.', 'warning')
        title = 'New Set of Pictures'
        list = db.getListOfFiles(cfg._destinationFolder, add_path=False)
        return load_pics(list, title=title)

    @app.route('/config', methods=['GET', 'POST'])
    def config():
        if request.method == 'GET':
            mode = ('demo' if cfg._test
                    else 'normal')
            return render_template('config.html',
                                   config_file=read_file('data/config.ini'),
                                   mode=mode, datamode=cfg._DataMode,
                                   title='Configuration')
        else:
            write_file('data/config.ini', request.form.get('config'))
            flash('RESTART THE APPLICATION IF SETTINGS FAIL TO BE APPLIED',
                  'critical')
            reload()
            return redirect('/config')

    @app.route('/blacklist', methods=['GET', 'POST'])
    def blacklist():
        if request.method == 'GET':
            return render_template('blacklist.html',
                                   blacklist=read_file('data/blacklist.txt'),
                                   title='Blacklisted files')
        else:
            write_file('data/blacklist.txt', request.form.get('blacklist'))
            return redirect('/blacklist')

    @app.route('/whitelist', methods=['GET', 'POST'])
    def whitelist():
        if request.method == 'GET':
            return render_template('whitelist.html',
                                   whitelist=read_file('data/whitelist.txt'),
                                   title='whitelisted files')
        else:
            write_file('data/whitelist.txt', request.form.get('whitelist'))
            flash('New whitelist file saved', 'info')
            return redirect('/whitelist')

    @app.route('/reload')
    def reload():
        global to_reload
        to_reload = True
        cfg.load_config()
        flash('Reloading completed', 'info')
        return 'reloaded'

    @app.route('/reset')
    def reset():
        db.reset_config(True)
        reload()
        flash('Restore completed', 'info')
        flash('RESTART THE APPLICATION IF SETTINGS FAIL TO BE APPLIED',
              'critical')
        return redirect('/config')

    @app.route('/clear')
    def clear():
        db.reset_config(False)
        flash('non-essential content removed. Ready for packaging', 'info')
        return redirect('/config')

    @app.route('/slideshow')
    def slideshow():
        list = db.getListOfFiles(cfg._destinationFolder, add_path=False)
        return load_pics(list, page='slideshow.html', title='Slideshow')

    @app.route('/csv_table')
    def csv_table():
        table = pd.read_csv('data/photofolderDB.csv', 
                            parse_dates=['datetime'],
                            dayfirst=True)
        table['datetime'] = pd.to_datetime(table['datetime'], unit='s')
        # print(table['datetime'].astype('datetime64[s]'))
        table.info()
        return render_template('csv_table.html', data=table.to_html(),
                               title='CSV Table')

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
    # test = bool(strtobool(cfg._test.capitalize()))
    print('Loading DEMO mode? ', cfg._test)
    run_simple('0.0.0.0', int(cfg._port), application,
               use_reloader=cfg._test,
               use_debugger=cfg._test,
               use_evalex=True)


# This application object can be used in any WSGI server
# for example in gunicorn, you can run "gunicorn app"
application = AppReloader(get_app)

if __name__ == '__main__':
    website()
