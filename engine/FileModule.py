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
    import setup as stp
    
else: 
    import engine.setup as stp
    import engine.app_config as cfg
    from engine.loggerinitializer import initialize_logger

stp.setup()
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
        append_multiple_lines('data/source.txt', sample)
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

def filePrunning(path, _file):
    try:
        os.remove(path + _file)
        filename, file_extension = os.path.splitext(_file)
        # Thumbnail removal changes in index.html may require adjustments here
        os.remove(path + '/thumbnail/' + filename + '_200x200_fit_90' + file_extension)
    except OSError as e:
        logging.error(e.errno)
        logging.error('FILE NOT FOUND ' + path + _file)
        return 'File Not Found: ' + path + _file
    else:
        logging.info('file removed '  + path + _file)
        return 'File removed: ' + path + _file


def fileRotate(path, _file, side='left'):
    try:
        picture= Image.open(path + _file)
        filename, file_extension = os.path.splitext(_file)
        # path = path + _file.split('.')
        # ext = path.pop()
        if side=='left':
            new_path = path + filename + '_L' + file_extension
            picture.rotate(90, expand=True).save(new_path)
        else:
            # new_path = '_'.join(path + filename) + '_R' + file_extension
            new_path = path + filename + '_R' + file_extension
            picture.rotate(270, expand=True).save(new_path)
        picture.close()
        filePrunning(path, _file)
        # print (new_path)
    except OSError as e:
        logging.error(e.errno + e)
        logging.error('Failed to rotate ' + path + _file)
        return 'Failed to rotate: ' + path + _file
    else:
        logging.info('file rotated '+ side + ': ' + new_path)
        return 'file rotated ' + side + ': ' + new_path


# -----------------
def getListOfFiles(dirName, add_path=True):
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
        if add_path: 
            fullPath = os.path.join(dirName, entry)
        else: 
            fullPath = fullPath = entry
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
            non_black = remove_common_from_list ('data/blacklist.txt', list_sample, 'data/source.txt')
            non_white = remove_common_from_list ('data/whitelist.txt', list_sample)
            logging.debug('non_black' + str(non_black))
            logging.debug('non_white' + str(non_white))
            return common(non_black, non_white)
        except ValueError as error:
            logging.error(error)
            return False

    # NO OTHER SORTING METHOD IS WORKING  :-[
    # elif criteria == 2:
    #     print('Getting a random set of ' + str(cfg._numberOfPics)) # + ' Photos with no less than ' + str(cfg._newerPhotos/365) + ' years')
    #     files = sorted(os.listdir(cfg._sourceFolder), key=os.path.getctime)
    #     # while files[i]. os.path.getctime > cfg._newerPhotos:
    #     for i in range(cfg._numberOfPics):
    #         newest = files[-i]
    #         return random.sample(newest, cfg._numberOfPics)
    # elif criteria == 3:
    #     files = sorted(os.listdir(cfg._sourceFolder),
    #         key=os.path.getctime, reverse = True)
    #     return random.sample(files, cfg._numberOfPics)
    # # elif:
    # #     oldest = files[0]
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
        if common(str(item), file_list):
            logging.info('common btw lists: '+ item)
        else: 
            clean_baselist.append(item) 
    
    logging.info('=============end remove common==================')
    return clean_baselist

# ---------old list_module.py----------

# https://www.codespeedy.com/find-the-common-elements-in-two-lists-in-python/
# payload = request.get_data().decode("utf-8")
# list = getListOfFiles(cfg._destinationFolder)

def common(lst1, lst2):
    if type(lst1) is str:
        return common_string_in_list (lst1, lst2)
    elif type(lst2) is str:
        return common_string_in_list (lst2, lst1)
    else:
        return list(set(lst1).intersection(lst2))
        # return list(set(lst1) & set(lst2))

def uncommon(base_list, special_list):
    # remove EOL special string
    # base_list = [item.replace('\n', '') for item in base_list]
    # special_list = [item.replace('\n', '') for item in special_list]
    a = set(base_list)
    b = set(special_list)
    print(base_list, a)
    print(special_list, b)
    print(list(a - b))
    return list(a - b)

def common_string_in_list(string, list):
    new_list = []
    for item in list:
        if str(item) in string and '/' in str(item):
            item = item.split('/')[-1:]
            new_list.append(item[0])
        elif str(item) in string:
            new_list.append(item)
    return new_list

def clear_duplicates(file):
    with open(file, "r") as f:
        file_list = f.readlines()

        # Walk the list and remove empty lines
        for item in file_list:
            if item == '':
                file_list.pop(item)

    # remove duplicates before record
        file_list.sort()
        new_list = set(file_list)
    with open(file, "w") as f:
        f.writelines(new_list)

# "borrowed" from https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/
def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

def append_multiple_lines(file_name, lines_to_append):
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        appendEOL = False
        # Move read cursor to the start of file.
        file_object.seek(0)
        # Check if file is not empty
        data = file_object.read(100)
        if len(data) > 0:
            appendEOL = True
            file_object.seek(0)
            source = file_object.readlines()
            # clear unwanted EOL from original file
            source = [item.replace('\n', '') for item in source]
            # remove possible duplicates
            lines_to_append = uncommon(lines_to_append, source)
        # Iterate over each string in the list
        for line in lines_to_append:
            # If file is not empty then append '\n' before first line for
            # other lines always append '\n' before appending line
            if appendEOL == True:
                file_object.write("\n")
            else:
                appendEOL = True
            # Append element at the end of file
            file_object.write(line)

def remove_multiple_lines(file_name, lines_to_remove):
    with open(file_name, "w+") as f:
        file_list = f.readlines()
        toBeRemoved = common (file_list, lines_to_remove)
        # Walk the list and remove empty lines
        for item in file_list:
            if item in toBeRemoved:
                file_list.pop(item)
        f.writelines(file_list)
        return toBeRemoved

def reset_config():
    stp.clean_folders(warning=0)
    stp.setup()

def common_test():
    a=[2,9,4,5]
    b=[3,5,7,9]
    c='2,9,4,5'
    print('[9, 5] ==', common(a,b))
    print('[5, 9] ==', common(b,c))
    print('[2, 4] ==', uncommon(a, b))
    print(uncommon(b,c))


if __name__ == '__main__':
    main()
   
