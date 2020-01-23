#!/usr/bin/env python3

# By Paulo Natel 
# Dec/2019
# pnatel@gmail.com

# Check README.md for information
# Change configuration in config.ini
# --------ATTENTION!----------
# RUN FROM THE FOLDER OR CONFIG WILL NOT BE FOUND
# python3 FileModule.py


# Importing required libraries
from pathlib import Path
import base64
import shutil, random, os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import configparser

config = configparser.ConfigParser()
_sourceFolder = ''
_destinationFolder = ''
_fileType = []
_numberOfPics = 0
_MaxNumberOfPics = 0
_foldersizeUpperLimit = 0
_newerPhotos = 0
_criteria = 0

# --------------------------------
# Main function copy photos based on the parameters selected
# --------------------------------
def main(): 
    print('--------START--------')
    start = datetime.now()
    print(start)
    print('Loading list of available photos from: ' + _sourceFolder)
    filenames = getListOfFiles(_sourceFolder)
    print('choosing and Sorting the sample')
    sample = sorting(filenames, _criteria, _numberOfPics)
    print('-------PRUNNING--------')
    folderPrunning(_destinationFolder, 2)
    print('Number of selected files on the sample: ' + str(len(sample)))
    copyFiles(sample)
    print('New folder Size ' + str(getSizeMB(_destinationFolder)) + 'Mb')      
    print('---------------------')
    end = datetime.now()
    print(end)
    print('Time elapsed:', end-start, 'secs')
    print('--------END----------')

# Loading Conguration file (config.ini)
# Code from https://wiki.python.org/moin/ConfigParserExamples
def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

# Copy a list of files to the folder
def copyFiles(fileList):
    for fname in fileList:
        if fname.endswith(_fileType):
            print('Copying file ' + fname)
            shutil.copy(fname, _destinationFolder)    
   
# checking size of the destination folder to trigger a cleanup
def folderPrunning(folder = _destinationFolder, multiplier = 1):
    folderSize = getSizeMB(folder)
    # print (folder, folderSize)
    print('Destination folder Size ' + str(folderSize) + 'Mb')
    if folderSize > _foldersizeUpperLimit:
        filenames = getListOfFiles(folder)
        prune = sorting(filenames, 1, _numberOfPics * multiplier)
        for fname in prune:
            print('Removing file ' + fname)
            os.remove(fname)
        print('Folder Size after prunning ' + str(getSizeMB(folder)) + 'Mb')
    else: print(folderSize, 'smaller than', _foldersizeUpperLimit)

def logPrunning(file='log.txt'):
    pass

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
        print('Getting a random set of ' + str(sampleSize) + ' Photos')
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


config.read('config.ini')
_sourceFolder = ConfigSectionMap('folder')['sourcefolder']
_destinationFolder = ConfigSectionMap('folder')['destinationfolder']
_fileType = tuple(dict(config.items('ext')).values())
_numberOfPics = int(ConfigSectionMap('parameter')['numberofpics'])
# _MaxNumberOfPics = int(ConfigSectionMap('parameter')['MaxNumberOfPics'])
_foldersizeUpperLimit = int(ConfigSectionMap('parameter')['foldersizeupperlimit'])
_newerPhotos = ConfigSectionMap('parameter')['newerphotos']
_criteria = int(ConfigSectionMap('sort')['criteria'])

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

