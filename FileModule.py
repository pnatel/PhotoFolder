#!/usr/bin/env python3

# By Paulo Natel 
# Mar/2020
# pnatel@live.com

# Check README.md for more information
# Change configuration in config.ini
# --------ATTENTION!----------
# RUN FROM THE FOLDER OR CONFIG WILL NOT BE FOUND
# python3 FileModule.py


# Importing required libraries
from pathlib import Path
import base64, shutil, random
import PIL, os
from PIL import Image
from sys import argv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import configparser
import logging

# Global Variables
config = configparser.ConfigParser()
_sourceFolder = ''
_destinationFolder = ''
_logPath = ''
_fileType = []
_numberOfPics = 0
_MaxNumberOfPics = 0
_foldersizeUpperLimit = 0
_newerPhotos = 0
_criteria = 0
_test = True

def open_log():
    logging.basicConfig(filename= _logPath, 
                        format='%(asctime)s - %(levelname)s - %(message)s', 
                        level=logging.INFO) # TODO: change config.ini loglevel here

# --------------------------------
# Main function copy photos based on the parameters selected
# --------------------------------
def main(): 
    open_log()
    logging.info('--------START--------')
    start = datetime.now()
    print('Job Start time:',start)
    logging.info('Loading list of available photos from: ' + _sourceFolder)
    filenames = getListOfFiles(_sourceFolder)
    logging.info('Found: ' + str(len(filenames)) + ' available files')
    logging.info('choosing and Sorting the sample')
    sample = sorting(filenames, _criteria, _numberOfPics)
    logging.info('-------PRUNNING--------')
    folderPrunning(_destinationFolder, 2)
    logging.info('Number of selected files on the sample: ' + str(len(sample)))
    copyFiles(sample)
    logging.info('New folder Size ' + str(getSizeMB(_destinationFolder)) + 'Mb')      
    logging.info('---------------------')
    end = datetime.now()
    print('Job finish time:',end)
    logging.info('Time elapsed:' + str(end-start) + 'secs')
    logging.info('--------END----------')

# Loading Conguration file (config.ini)
# Code from https://wiki.python.org/moin/ConfigParserExamples
def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                logging.warning("skip: %s" % option)
        except:
            logging.error("exception on %s!" % option)
            dict1[option] = None
    return dict1

# Copy a list of files to the folder
def copyFiles(fileList):
    for fname in fileList:
        if fname.endswith(_fileType):
            logging.info('Copying file ' + fname)
            shutil.copy(fname, _destinationFolder)    
   
# checking size of the destination folder to trigger a cleanup
def folderPrunning(folder = _destinationFolder, multiplier = 1):
    folderSize = getSizeMB(folder)
    # logging.info (folder, folderSize)
    logging.info('Destination folder Size ' + str(folderSize) + 'Mb')
    if folderSize > _foldersizeUpperLimit:
        filenames = getListOfFiles(folder)
        prune = sorting(filenames, 1, _numberOfPics * multiplier)
        for fname in prune:
            logging.info('Removing file ' + fname)
            os.remove(fname)
        logging.info('Folder Size after prunning ' + str(getSizeMB(folder)) + 'Mb')
    else: logging.info(str(folderSize) + ' smaller than ' + str(_foldersizeUpperLimit))

def filePrunning(filePath):
    # open_log()
    try:
        os.remove(filePath)
    except OSError as e:
        logging.error(e.errno)
        logging.error('FILE NOT FOUND', filePath)
        return 'File Not Found: '+ filePath
    else:
        logging.info('file removed', filePath)
        return 'File removed: '+ filePath
    

def fileRotate(filePath):
    try:
        picture= Image.open(filePath)
        path = filePath.split('.')
        ext = path.pop()
        new_path = '_'.join(path) + '_R.' + ext
        picture.rotate(90, expand=True).save(new_path)
        picture.close()
        filePrunning(filePath)
        print (new_path)
    except OSError as e:
        logging.error(e.errno)
        logging.info('Failed to rotate', filePath)
        return 'Failed to rotate: '+ filePath
    else:
        logging.info('file rotated 90o', filePath)
        return 'file rotated 90o: '+ filePath
    

# -----------------
def getListOfFiles(dirName):
    '''
    For the given path, get the List of all files in the directory tree 
    '''
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles        

# This alternative code could be useful on a different moment
# Get the list of all files in directory tree at given path
def getListOfFilesWalk(dirName, returnList=True):
    listOfFiles = list()
    walk = os.walk(dirName)
    for (dirpath, dirnames, filenames) in walk:
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    if returnList:
        return listOfFiles
    else:
        return walk

# returns the size of the folder in bytes
def getSizeMB(folder = '.'):
    root_directory = Path(folder)
    size = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    return size/(10**6)

# Print the list of files
def printList(listOfFiles):
    # Print the files
    for elem in listOfFiles:
        print(elem)

# print a folder content (no subdirectories)
def printIter(path='.'):
    for path in Path(path).iterdir():
        print(path)

# different way to perform the read of the contents (no subfolders)  
def readFolderContent(path= '.'):
    # Path.iterdir() returns an iterator, which can be easily turned into a list:
    contents = list(Path(path).iterdir())
    return contents

# choosing and Sorting the sample
def sorting(filenames, criteria=1, sampleSize=10):
    # print(len(filenames), criteria, sampleSize)
    if criteria == 1: # Random pics from source
        logging.info('Getting a random set of ' + str(sampleSize) + ' Photos')
        return random.sample(filenames, sampleSize)

    # NO OTHER SORTING METHOD IS WORKING    
    elif criteria == 2:
        print('Getting a random set of ' + str(_numberOfPics)) # + ' Photos with no less than ' + str(_newerPhotos/365) + ' years')
        files = sorted(os.listdir(_sourceFolder), key=os.path.getctime)
        # while files[i]. os.path.getctime > _newerPhotos:
        for i in range(_numberOfPics):
            newest = files[-i]
            return random.sample(newest, _numberOfPics)
    elif criteria == 3:
        files = sorted(os.listdir(_sourceFolder), 
            key=os.path.getctime, reverse = True)
        return random.sample(files, _numberOfPics)
    # elif:
    #     oldest = files[0]
    else:
        print ('Criteria not met!')


# Loading configuration
# ---------------------
config.read('config.ini')
if len(argv) > 1 or _test:
    print ('Arguments: ', argv[1:])
    _sourceFolder = ConfigSectionMap('test')['sourcefolder']
    _destinationFolder = ConfigSectionMap('test')['destinationfolder']
    _logPath = ConfigSectionMap('test')['logpath']
    _numberOfPics = int(ConfigSectionMap('parameter')['numberofpics_test'])
    _foldersizeUpperLimit = int(ConfigSectionMap('parameter')['foldersizeupperlimit_test'])
else:
    _sourceFolder = ConfigSectionMap('folder')['sourcefolder']
    _destinationFolder = ConfigSectionMap('folder')['destinationfolder']
    _logPath = ConfigSectionMap('folder')['logpath']
    _numberOfPics = int(ConfigSectionMap('parameter')['numberofpics']) 
    _foldersizeUpperLimit = int(ConfigSectionMap('parameter')['foldersizeupperlimit'])

_fileType = tuple(dict(config.items('ext')).values())
# _MaxNumberOfPics = int(ConfigSectionMap('parameter')['MaxNumberOfPics'])
_newerPhotos = ConfigSectionMap('parameter')['newerphotos']
_criteria = int(ConfigSectionMap('sort')['criteria'])
_logLevel = ConfigSectionMap('loglevel')['level']

#self test
def _test():
    # print(readFolderContent('..'))
    # copyFilesRandom()
    # print(getListOfFilesWalk(_sourceFolder, False))
    print('Source size', getSizeMB(_sourceFolder), 'Mbytes')
    print('Destin Size', getSizeMB(_destinationFolder), 'Mbytes')
    # folderPrunning()
    # printList(getListOfFilesWalk(_sourceFolder))
    # printIter(_destinationFolder)
    # print(_newerPhotos)
    # print(type(_fileType))
    
    # config.read('config.ini')

    # _sourceFolder = ConfigSectionMap('folder')['sourcefolder']

    print (type(_sourceFolder), type(_destinationFolder),
         type(_fileType), type(_numberOfPics), type(_foldersizeUpperLimit), 
         type(_newerPhotos), type(_criteria))

    for section in config.sections():
        for key in config[section]:  
            print(config[section][key])

if __name__ == '__main__':
    
    main()
    # _test()

