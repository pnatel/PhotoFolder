#!/usr/bin/env python3

# Version: 1.0

# Use pipreqs to generate the requirements.txt 

# run in console or redirect output to a log file

# Some of the Research sources for reference:
# https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/

# TODO:
# add sftp feature so the code does need to be ran from the host
# Make it run on Docker

# Importing required libraries
from pathlib import Path
import base64
import shutil, random, os
from datetime import datetime
from dateutil.relativedelta import relativedelta

# -----------------
# Application parameters, configuration and variables:
_sourceFolder = '/mnt/usbstorage/media/Pictures/Minhas_imagens/Guimaraes_Silva_Collection/'
_destinationFolder = '/mnt/usbstorage/PhotoFolder'  # change for a folder
_fileType = ('jpg','JPEG','JPG','jpeg')
_numberOfPics = 100
# _MaxNumberOfPics = 100
_foldersizeUpperLimit = 1000 # in Megabytes
_newerPhotos = datetime.now() - relativedelta(years=3)
_criteria = 1 # 1 = Random, 
              # 2 = Shuffle recently, 
              # 3 = Shuffle oldest,
              # 4 = Descendent by Date taken, 
              # 5 = By Location (Need to read it from pic or Google)

# --------------------------------
# Main function copy photos based on the parameters selected
# --------------------------------
def main(): 
    print('---------START---------')
    print(datetime.now())
    print('Loading list of available photos from: ' + _sourceFolder)
    filenames = getListOfFiles(_sourceFolder)
    print('choosing and Sorting the sample')
    sample = sorting(filenames, _criteria)

    print('---------PRUNNING---------')
    folderPrunning(multiplier = 2)

    print('Number of selected files on the sample: ' + str(len(sample)))
    for fname in sample:
        if fname.endswith(_fileType):
            print('Copying file ' + fname)
            # srcpath = os.path.join(_sourceFolder, fname)
            shutil.copy(fname, _destinationFolder)
    print('New folder Size ' + str(getSizeMB(_destinationFolder)) + 'Mb')
        
    print('------------------')
    print(datetime.now())
    print('--------END----------')

    
   
# checking size of the destination folder to trigger a cleanup
def folderPrunning(folder = _destinationFolder, multiplier = 1):
    folderSize = getSizeMB(folder)
    print('Destination folder Size ' + str(folderSize) + 'Mb')
    if folderSize > _foldersizeUpperLimit:
        filenames = getListOfFiles(folder)
        prune = sorting(filenames, 1, _numberOfPics * multiplier)
        for fname in prune:
            print('Removing file ' + fname)
            os.remove(fname)
            # srcpath = os.path.join(folder, fname)
            # print(srcpath)
        print('Folder Size after prunning ' + str(getSizeMB(folder)) + 'Mb')


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
def sorting(filenames, criteria=1, sampleSize=_numberOfPics):
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
        pass

#self test
def _test():
    # print(readFolderContent('..'))
    # copyFilesRandom()
    # # print(getListOfFilesWalk(_sourceFolder, False))
    # print('Source size', getSizeMB(_sourceFolder), 'Mbytes')
    print('Destin Size', getSizeMB(_destinationFolder), 'Mbytes')
    folderPrunning()
    # printList(getListOfFilesWalk(_sourceFolder))
    # printIter(_destinationFolder)
    # print(_newerPhotos)

if __name__ == '__main__':
    # _test()
    main()
    

