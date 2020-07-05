#!/usr/bin/env python3

# By Paulo Natel
# May/2020
# pnatel@live.com

# Check README.md for more information
# Change configuration in config.ini
# --------ATTENTION!----------
# RUN FROM THE FOLDER OR CONFIG WILL NOT BE FOUND
# python3 FileModule.py


# Importing required libraries
from pathlib import Path
import base64, shutil, random
import os
from PIL import Image
from sys import argv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
# Running as standalone or part of the application
# print(__name__)
if __name__ == '__main__' or __name__ == 'FileModule':
    import app_config as cfg
    from loggerinitializer import initialize_logger
    import list_module as ls
else: 
    import engine.app_config as cfg
    from engine.loggerinitializer import initialize_logger
    import engine.list_module as ls

cfg.load_config()
initialize_logger(cfg._logPath)

# def open_log():
#     logging.basicConfig(filename= cfg._logPath,
#                         format='%(asctime)s - %(levelname)s - %(message)s',
#                         level=logging.INFO) # TODO: change config.ini loglevel here

# --------------------------------
# Main function copy photos based on the parameters selected
# --------------------------------
def copy_job():
    logging.info('--------START--------')
    start = datetime.now()
    print('Job Start time:',start)
    logging.info('Loading list of available photos from: ' + cfg._sourceFolder)
    filenames = getListOfFiles(cfg._sourceFolder)
    logging.info('Found: ' + str(len(filenames)) + ' available files')
    logging.info('choosing and Sorting the sample')
    sample = sorting(filenames, cfg._criteria, cfg._numberOfPics)
    try:
        sample != False
    except:
        logging.error('Sample size returned FALSE')
    else:
        logging.info('-------PRUNNING--------')
        folderPrunning(cfg._destinationFolder, 2)
        logging.info('Number of selected files on the sample: ' + str(len(sample)))
        # keeping source address of all files for backtrack 
        ls.append_multiple_lines('config/source.txt', sample)
        copyFiles(sample)

    logging.info('New folder Size ' + str(getSizeMB(cfg._destinationFolder)) + 'Mb')
    logging.info('---------------------')
    end = datetime.now()
    print('Job finish time:',end)
    logging.info('Time elapsed:' + str(end-start) + 'secs')
    logging.info('--------END----------')

# A legacy function calling function
def main():
    copy_job()

def fileTypeTest(file, typeList=cfg._fileType):
    if file.endswith(typeList):
        logging.debug('extension accepted ' + file)
        return True
    else:
        logging.warning('extension invalid ' + file)
        return False

# Copy a list of files to the folder
def copyFiles(fileList):
    for fname in fileList:
        if fileTypeTest(fname, cfg._fileType):
            logging.info('Copying file ' + fname)
            shutil.copy(fname, cfg._destinationFolder)

# checking size of the destination folder to trigger a cleanup
def folderPrunning(folder = cfg._destinationFolder, multiplier = 1):
    folderSize = getSizeMB(folder)
    # logging.info (folder, folderSize)
    logging.info('Destination folder Size ' + str(folderSize) + 'Mb')
    if folderSize > cfg._foldersizeUpperLimit:
        filenames = getListOfFiles(folder)
        if len(filenames) > (cfg._numberOfPics * multiplier):
            prune = sorting(filenames, 1, cfg._numberOfPics * multiplier)
        else:
            prune = sorting(filenames, 1, cfg._numberOfPics * int(multiplier/2))
        for fname in prune:
            logging.info('Removing file ' + fname)
            os.remove(fname)
        logging.info('Folder Size after prunning ' + str(getSizeMB(folder)) + 'Mb')
    else:
        logging.info(str(folderSize) + ' smaller than ' + str(cfg._foldersizeUpperLimit))

def filePrunning(filePath):
    try:
        os.remove(filePath)
    except OSError as e:
        logging.error(e.errno)
        logging.error('FILE NOT FOUND ' + filePath)
        return 'File Not Found: '+ filePath
    else:
        logging.info('file removed ' + filePath)
        return 'File removed: '+ filePath


def fileRotate(filePath,side='left'):
    try:
        picture= Image.open(filePath)
        path = filePath.split('.')
        ext = path.pop()
        if side=='left':
            new_path = '_'.join(path) + '_L.' + ext
            picture.rotate(90, expand=True).save(new_path)
        else:
            new_path = '_'.join(path) + '_R.' + ext
            picture.rotate(270, expand=True).save(new_path)
        picture.close()
        filePrunning(filePath)
        # print (new_path)
    except OSError as e:
        logging.error(e.errno + e)
        logging.error('Failed to rotate ' + filePath)
        return 'Failed to rotate: '+ filePath
    else:
        logging.info('file rotated '+ side + ': ' + new_path)
        return 'file rotated ' + side + ': ' + new_path


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
            if fileTypeTest(entry, cfg._fileType):
                allFiles.append(fullPath)
            else:
                logging.debug(entry + ' INVALID FILE TYPE ' + str(cfg._fileType))
    return allFiles

# This alternative code could be useful on a different moment
# Get the list of all files in directory tree at given path
def getListOfFilesWalk(dirName, returnList=True):
    listOfFiles = list()
    walk = os.walk(dirName)
    for (dirpath, dirnames, filenames) in walk:
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        print(dirpath, dirnames, filenames)
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
    if len(filenames) < sampleSize:
        logging.warning('The Sample (' + str(sampleSize) + ') is bigger than the source size (' + str(len(filenames)) + ')')
        sampleSize = int(len(filenames) / 2)
        logging.info('New Sample Size: ' + str(sampleSize))

    # sorting criterias
    if criteria == 1: # Random pics from source
        logging.info('Getting a random set of ' + str(sampleSize) + ' Photos')
        try:
            list_sample = random.sample(filenames, sampleSize)
            non_black = remove_common_from_list ('config/blacklist.txt', list_sample, 'config/source.txt')
            non_white = remove_common_from_list ('config/whitelist.txt', list_sample)
            logging.debug('non_black' + str(non_black))
            logging.debug('non_white' + str(non_white))
            return ls.common(non_black, non_white)
        except ValueError as error:
            logging.error(error)
            return False

    # NO OTHER SORTING METHOD IS WORKING  :-[
    elif criteria == 2:
        print('Getting a random set of ' + str(cfg._numberOfPics)) # + ' Photos with no less than ' + str(cfg._newerPhotos/365) + ' years')
        files = sorted(os.listdir(cfg._sourceFolder), key=os.path.getctime)
        # while files[i]. os.path.getctime > cfg._newerPhotos:
        for i in range(cfg._numberOfPics):
            newest = files[-i]
            return random.sample(newest, cfg._numberOfPics)
    elif criteria == 3:
        files = sorted(os.listdir(cfg._sourceFolder),
            key=os.path.getctime, reverse = True)
        return random.sample(files, cfg._numberOfPics)
    # elif:
    #     oldest = files[0]
    else:
        logging.error('Sorting criteria not met n. of files: ' + str(len(filenames)))
        print ('Sorting criteria not met')

def remove_common_from_list (file, baselist, keep_path=''):
    with open(file, "r") as f:
        file_list = f.readlines()
        # clear unwanted EOL from original file
        file_list = [item.replace('\n', '') for item in file_list]
    logging.debug(file + str(file_list) + str(baselist))
    clean_baselist = []
 
    logging.info('========Remove common items from list==========')               
    for item in baselist:
        logging.debug('item in baselist: ' + item)
        # print(ls.common(str(item), file_list))
        if ls.common(str(item), file_list):
            logging.info('common btw lists: '+ item)
        else: 
            clean_baselist.append(item) 
    
    logging.info('=============end remove common==================')
    return clean_baselist


if __name__ == '__main__':
    main()

