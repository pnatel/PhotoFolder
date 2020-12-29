# Run this file before run the application 
# to create/check file/folder integrity

import os, logging
import shutil



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
    'data/source.txt'
]

config = 'data/config.ini'

def empty_structure(folders=folders, files=empty_files):
    '''
    Create empty folders and files
    '''
    try:
        print('Creating folders:', folders)
        for folder in folders:
            folder_check(folder)
        print('Creating empty files:', files)
        for file in files:
            file_check(file)
    except OSError as identifier:
        print(identifier)

def folder_check(folder):
    '''
    Check if folder exists otherwise create it
    '''
    if os.path.exists(folder) and os.path.isdir(folder):
        print(folder, 'already exists')
    else: 
        os.mkdir(folder)
        print(folder, 'Created')

def file_check(file):
    '''
    Check if file exists otherwise create a blank version
    '''
    if os.path.exists(file) and os.path.isfile(file):
        print(file, 'already exists')
    else: 
        with open(file, "x"):
            print(file, 'Created')

# ----------Create config template-----------
def create_config(cfg=config):
    try:
        print('Creating template config in', config)
        if os.path.exists(config) and os.path.isfile(config):
            print(config, 'already exists')
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
dbSource = data/source.csv
dbDestin = data/destination.csv


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
JobInterval = 10
command = ping google.com'''
            )
            print(config, 'Created')
    except OSError as identifier:
        print(identifier)

def enhance_requirements():
    """
    This function change requirements.txt to accept 
    newer versions of the modules.
    it replaces == with =>
    """
    logging.info("Generating updated requirements") 
    print(os.system("pipreqs --force"))
    with open(os.path.join(os.path.dirname(__file__), os.pardir, 'requirements.txt'), 'r') as f:
        reqs = f.read()
        reqs = reqs.replace('==', '>=')
    with open(os.path.join(os.path.dirname(__file__), os.pardir, 'requirements.txt'), 'w') as f:
        f.write(reqs)


def clean_folders(folders=folders, warning=1):
    print('''
    WARNING
    This function will reset the app to its defaults.
    All configuration, logs and other content will be 
    removed with NO warnings
    ''')
    if warning:
        input('Press CTRL+C to exit or any key to continue.')
    try:
        print('removing folders:', folders)
        for folder in folders:
            if os.path.exists(folder) and os.path.isdir(folder):
                shutil.rmtree(folder)
                print(folder, 'removed')
            else:
                print(folder, 'Not available')
    except OSError as identifier:
        print(identifier)

def setup():
    empty_structure()
    create_config()

if __name__ == '__main__':
    # Build the barebones for the app to run
    # setup()

    # remove all non-essential files/folders
    clean_folders()

    # update requirements.txt
    # enhance_requirements()

