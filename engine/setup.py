# Run this file before run the application
# to create/check file/folder integrity

import os
import logging
import shutil
import subprocess
import sys

# create console handler and set level to DEBUG
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

folders = [
    'data',
    'logs',
    'logs/demo',
    'logs/production',
    'engine/static/destination',
    'engine/static/demo/destination'
]

empty_files = [
    'data/blacklist.txt',
    'data/whitelist.txt',
    'data/source.txt',
    'data/photofolderDB.csv'
]

config = 'data/config.ini'


def empty_structure(folders=folders, files=empty_files):
    '''
    Create empty folders and files
    '''
    try:
        logging.debug('Creating folders: ' + str(folders))
        for folder in folders:
            folder_check(folder)
        logging.debug('Creating empty files: ' + str(files))
        for file in files:
            file_check(file)
    except OSError as identifier:
        print(identifier)


def folder_check(folder):
    '''
    Check if folder exists otherwise create it
    '''
    if os.path.exists(folder) and os.path.isdir(folder):
        logging.debug(folder + ' already exists')
    else:
        os.mkdir(folder)
        logging.info(folder + ' Created')


def file_check(file):
    '''
    Check if file exists otherwise create a blank version
    '''
    if os.path.exists(file) and os.path.isfile(file):
        logging.debug(file + ' already exists')
    else:
        with open(file, "x"):
            logging.info(file + ' Created')


# ----------Create config template-----------
def create_config(cfg=config):
    try:
        logging.debug('Creating template config in ' + config)
        if os.path.exists(config) and os.path.isfile(config):
            logging.info(config + ' already exists')
        else:
            # config
            with open(config, "x") as f:
                f.write(
                    '''# Production environment
[folder]
# Point SourceFolder to your pool of pictures
SourceFolder = /source
# only change destination if you are NOT using the website
DestinationFolder = engine/static/destination/
LogPath = logs/production

[data]
csvDB = data/photofolderDB.csv
MongoURL = mongodb+srv://" + cfg._dbUser + ":" + cfg._dbPass + "@cluster0.6nphj.mongodb.net/" + cfg._dbName + "?retryWrites=true&w=majority
dbUser = 
dbPass = 
dbName = 

[ext]
FileType1 = jpg
FileType2 = jpeg
FileType3 = png
FileType4 = JPG
FileType5 = JPEG
FileType6 = PNG

[parameter]
port = 23276
# Size of your sample of pictures from the source folder
NumberOfPics = 100
# not implemented
MaxNumberOfPics = 1000
# How much the folder can grow size in Megabytes
FoldersizeUpperLimit = 1000
NewerPhotos = datetime.now() - relativedelta(years=3)
# Waiting time between auto copy job (in seconds)
JobInterval = 86400
# Log Level usage: (Default = 3)
# 1 = debug    - Detailed information, typically of interest only
#                when diagnosing problems.
# 2 = info     - Confirmation that things are working as expected.
# 3 = warning  - An indication that something unexpected happened,
#                or indicative of some problem in the near future
#                (e.g. ‘disk space low’).
#                The software is still working as expected.
# 4 = error    - Due to a more serious problem, the software has not
#                been able to perform some function.
# 5 = critical - A serious error, indicating that the program itself
#                may be unable to continue running.
logLevel = 3
# How the data is manipulated? (txt, csv, mongo)
DataMode = csv

[notification]
# Run this command after the auto copy job is completed
# The command can do whatever you want. I use it to send
# notifications to https://healthchecks.io/
# e.g: "curl -fsS --retry 3 https://hc-ping.com/your-uuid-here"
command =

# ONLY RANDOM IS IMPLEMENTED
[sort]
# 1 = Random,
# 2 = Shuffle recently,
# 3 = Shuffle oldest,
# 4 = Descendent by Date taken,
# 5 = By Location (Need to read it from pic or Google)
Criteria = 1

# settings for application testing/DEMO and CI/CD on Github
[test]
# test_mode True for DEMO or False for production environment
test_mode = True
SourceFolder = engine/static/demo/source/
DestinationFolder = engine/static/demo/destination/
LogPath = logs/demo
NumberOfPics = 3
FoldersizeUpperLimit = 10
JobInterval = 60
command = tail logs/demo/debug.log''')
            logging.info(config + ' Created')
    except OSError as identifier:
        logging.critical(identifier)


def enhance_requirements():
    """
    This function change requirements.txt to accept
    newer versions of the modules.
    it replaces == with =>
    """
    os.system("pip install pipreqs")
    logging.info("Generating updated requirements")
    logging.debug('pipreqs result: ' + str(os.system("pipreqs --force")))
    with open(os.path.join(os.path.dirname(__file__),
              os.pardir, 'requirements.txt'), 'r') as f:
        reqs = f.read()
        reqs = reqs.replace('==', '>=')
    with open(os.path.join(os.path.dirname(__file__),
              os.pardir, 'requirements.txt'), 'w') as f:
        f.write(reqs)


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def install_requirements():
    """
    This function install if host has all libraries required
    """
    logging.info("Updating Application Requirements")
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                          "--no-cache-dir", "-r", "requirements.txt"])


def clean_folders(folders=folders, warning=1):
    logging.warning('''
    This function will reset the app to its defaults.
    All configuration, logs and other content will be
    removed with NO warnings
    ''')
    if warning:
        input('Press CTRL+C to exit or any key to continue.')
    try:
        logging.info('removing folders: ' + str(folders))
        for folder in folders:
            if os.path.exists(folder) and os.path.isdir(folder):
                shutil.rmtree(folder)
                logging.debug(folder + ' removed')
            else:
                logging.debug(folder + ' Not available')
    except OSError as identifier:
        logging.error(identifier)


def setup():
    install_requirements()
    empty_structure()
    create_config()


if __name__ == '__main__':

    while True:
        print('''
    Choose one of the below options:
    1 - Setup (Build the barebones for the app to run)
    2 - Clean-up (remove all non-essential files/folders)
    3 - Update requirements.txt
    0 - EXIT
    ''')
        option = input('your Choice [1, 2, 3 or 0]: ')

        if option == '1':
            # Build the barebones for the app to run
            setup()
        elif option == '2':
            # remove all non-essential files/folders
            clean_folders(warning=0)
        elif option == '3':
            # update requirements.txt
            enhance_requirements()
        elif option == '0':
            break
        else:
            print(option, 'Not valid!')
