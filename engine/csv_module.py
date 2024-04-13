##!/usr/bin/env python3

# By Paulo Natel
# Jan/2021
# pnatel@live.com

# Check README.md for more information

# Importing required libraries
from pathlib import Path
import os.path
import shutil
import random
import logging
import datetime
import csv
from PIL import Image

# Running as standalone or part of the application
if __name__ == '__main__' or __name__ == 'csv_module':
    import app_config as cfg
    from loggerinitializer import initialize_logger
    import setup as stp
    from file_class import Photo
    stp.setup()

else:
    import engine.app_config as cfg
    from engine.loggerinitializer import initialize_logger
    from engine.file_class import Photo


cfg.load_config()
initialize_logger(cfg._logPath)


def add_record_csv(recordDict, csv_file):
    """
    docstring
    """
    if recordDict['destination_folder'] != '':
        recordDict["counter"] = int(recordDict["counter"]) + 1
        # if int(recordDict['rotate']) != 0:
        #     fileRotate(recordDict['destination_folder'], recordDict['filename'],
        #                side=int(recordDict['rotate']))
    with open(csv_file, 'a+') as file:
        headers = []
        for key in recordDict.keys():
            headers.append(key)

        writer = csv.DictWriter(file, fieldnames=headers)
        # Check if the file is empty and add the header
        file.seek(0)
        if not len(file.read(100)):
            writer.writeheader()
            logging.warning('CSV is empty, generating headers')
        # Read the file and dump test if record is not already in the file
        file.seek(0)
        read = file.read()
        # print(read)
        if recordDict["filename"] not in read:
            writer.writerow(recordDict)
            logging.info('adding row for: ' + recordDict["filename"])
        else:
            update_record_csv(recordDict["filename"], csv_file,
                              counter=recordDict["counter"])
            logging.debug('File already in CSV: ' + recordDict["filename"])


def read_CSV(csv_file):
    """
    docstring
    """
    temp = []
    with open(csv_file, 'r') as file:
        records = csv.DictReader(file)
        for record in records:
            temp.append(record)
    return temp


def remove_record_csv(filename, csv_file):
    """
    docstring
    """
    read = read_CSV(csv_file)

    for item in read:
        if filename in item['filename']:
            record_found = item
            # print('\n\tremove_record_csv', filename, item['filename'],
            #       filename in item['filename'])
            logging.debug('removing: ' + filename + ' from ' + csv_file)
            read.remove(item)

            # print('\n\n', read)
            with open(csv_file, 'w') as writeFile:
                headers = []
                for key in read[0].keys():
                    headers.append(key)
                writer = csv.DictWriter(writeFile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(read)
                return record_found
    return False


def update_record_csv(filepath, csv_file, **kargs):
    """
    docstring
    """
    filename = os.path.basename(filepath)
    modified = False
    logging.debug(f'update_record_csv param: {filename}, {csv_file}, {kargs}')
    records = read_CSV(csv_file)
    for record in records:
        temp = dict(record)
        if filename in temp['filename']:
            logging.debug('Found: ' + filename +
                          ' Counter: ' + temp['counter'])
            for key, value in temp.items():
                if key in kargs and key != 'counter':
                    # print(f'{key:25}: {value}, {key in kargs}, \
                    #       {temp[key]} != {kargs[key]}')
                    if temp[key] != str(kargs[key]):
                        modified = True
                        temp[key] = kargs[key]
                        logging.debug(f'{filename} - {key} changing \
                                      from {value} to {kargs[key]}')
                    else:
                        logging.error(f'param in record ({temp[key]}) \
                                      is the same as provided: {kargs[key]}')
            break

        else:
            logging.debug(f"{filename} differ than {temp['filename']}")
    if modified:
        removed_record = remove_record_csv(temp['filename'], csv_file)
        if removed_record:
            temp['counter'] = int(removed_record['counter'])
            logging.info('SUCCESS: ' + temp['filename'] +
                         ' removed from ' + csv_file)
            add_record_csv(temp, csv_file)
            logging.info(f"{temp['filename']} successfully updated, \
                         FINAL counter: {temp['counter']}")
        else:
            logging.warning('FAILED: ' + temp['filename']
                         + ' NOT removed from ' + csv_file)
    else:
        logging.error(f"{filename} was NOT changed")
    logging.debug(f'update_record_csv output: {temp}')
    return temp


def filter_record_csv(csv_file=cfg._csvDB, **kargs):
    """[summary]

    Args:
        csv_file ([type], optional): [description]. Defaults to cfg._csvDB.

    Returns:
        [type]: [description]
    """
    logging.debug(f'filter_record_csv param: {csv_file}, {kargs}')
    records = read_CSV(csv_file)
    temp = []
    for record in records:
        for key in kargs:
            # logging.debug(f'key in kargs: {key}, {(kargs.get(key))} == {(record[key])}')
            # logging.debug(
            #     f'key in record: {key in record}, and kargs.get(key) == record[key] {str(kargs.get(key)) == str(record[key])}')
            if key in record and str(kargs.get(key)) == str(record[key]):
                temp.append(record)
    logging.debug(f'filter_record_csv result: {temp}')
    return temp


def add_multiple_csv_records(list_file_paths, csv_file, destination_folder=''):
    """
        docstring
    """
    for file_path in list_file_paths:
        record = Photo.byPath(file_path, destination_folder)
        add_record_csv(record.asdict(), csv_file)


# IMPURE
def fileTypeTest(file, typeList=cfg._fileType):
    '''
        checks if the file extension is in the list of
        acceptable extensions.
        The default list is in the config.ini under filetype

        The parameter typeList=cfg._fileType, can be changed
        to bypass the defaults.
    '''
    if file.endswith(typeList):
        logging.debug('extension accepted ' + file)
        return True
    else:
        logging.warning('extension invalid ' + file)
        return False


def copyFiles(fileList,
              ftype=cfg._fileType,
              destination=cfg._destinationFolder,
              csv=cfg._csvDB):
    '''
        Copy a list of files to the folder
    '''
    logging.info('Copying ' + str(len(fileList)) + ' files')
#    logging.debug(fileList)

    for fname in fileList:
        if fileTypeTest(fname, ftype):
            logging.debug(f'Copying file {fname} to {destination}')
            shutil.copy(fname, destination)
            update_record_csv(fname, csv, destination_folder=destination)


def getSizeMB(folder='.'):
    '''
        returns the size of the folder in bytes
    '''
    root_directory = Path(folder)
    size = sum(f.stat().st_size
               for f in root_directory.glob('**/*')
               if f.is_file())
    return size/(10**6)


# ------Legacy Function-----------
def getListOfFiles(dirName, add_path=True):
    '''
    For the given path, get the List of all files in the directory tree
    '''
    return update_csv_ListOfFiles(dirName, cfg._csvDB, clean=False,
                                  add_path=add_path)


# -----------------
# IMPURE
def update_csv_ListOfFiles(dirName, csv_file, clean=False, add_path=True):
    '''
    For the given path, get the List of all files in the directory tree
    '''
    # create a list of files and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            if 'thumbnail' in fullPath:
                pass
            else:
                update_csv_ListOfFiles(fullPath, csv_file)
        else:
            if fileTypeTest(entry, cfg._fileType):
                record = Photo.byPath(fullPath)
                add_record_csv(record.asdict(), csv_file)
            else:
                logging.debug(entry + ' INVALID FILE TYPE ' +
                              str(cfg._fileType))
    if cfg._sourceFolder in dirName:
        return rebuild_path_from_csv(csv_file, 'source_folder',
                                     clean, add_path)
    else:
        return rebuild_path_from_csv(csv_file, 'destination_folder',
                                     clean, add_path)


def am_I_unique(dictRecord, target='source_folder'):
    """
    docstring
    """
    if target == 'source_folder':
        if dictRecord['destination_folder'] == '':
            return True
        else:
            return False
    else:
        if dictRecord['destination_folder'] == '':
            return False
        else:
            return True


# IMPURE
def rebuild_path_from_csv(csv_file, folder, clean=False, add_path=True):
    """
    docstring
    """
    # logging.debug(folder)
    # logging.debug(csv_file)
    # logging.debug(str(clean))
    # logging.debug(str(add_path))
    # logging.debug(type(clean))
    # logging.debug(type(add_path))
    temp = []
    source = read_CSV(csv_file)
    for item in source:
        # logging.debug(item)
        if clean:
            # no duplicates
            # logging.debug('Clean True')
            # logging.debug(str(clean))
            if am_I_unique(item, folder):
                logging.debug('Unique True')
                if add_path:
                    # logging.debug('adding path')
                    # logging.debug(str(add_path))
                    if item[folder][-1] == '/':
                        temp.append(''.join(item[folder] +
                                    item['filename']))
                    else:
                        temp.append(''.join(item[folder] +
                                    '/' + item['filename']))
                else:
                    # logging.debug('NO path')
                    # logging.debug(str(add_path))
                    temp.append(item['filename'])
        else:
            if item[folder] == '':
                pass
            else:
                if add_path:
                    # logging.debug('adding path')
                    # logging.debug(str(add_path))
                    if item[folder][-1] == '/':
                        temp.append(''.join(item[folder] +
                                            item['filename']))
                    else:
                        temp.append(''.join(item[folder] +
                                            '/' + item['filename']))
                else:
                    # logging.debug('NO path')
                    # logging.debug(str(add_path))
                    temp.append(item['filename'])
    logging.debug(f'Returning {len(temp)} path from {csv_file}')
    # logging.debug(temp)
    return temp


def sorting(filenames, criteria=1, sampleSize=10):
    '''
        Choosing and Sorting the sample
    '''
    # print(len(filenames), criteria, sampleSize)
    if len(filenames) < sampleSize:
        logging.warning('The Sample (' + str(sampleSize) +
                        ') is bigger than the source size (' +
                        str(len(filenames)) + ')')
        sampleSize = int(len(filenames) / 2) + (len(filenames) % 2 > 0)
        logging.info('New Sample Size: ' + str(sampleSize))

    # sorting criterias
    if criteria == 1:  # Random pics from source
        logging.info('Getting a random set of ' + str(sampleSize) + ' Photos')
        try:
            sample = random.sample(filenames, sampleSize)
            # logging.debug('SAMPLE: ' + str(sample))
            return sample

        except ValueError as error:
            logging.error(error)
            return False

    # NO OTHER SORTING METHOD IS WORKING  :-[
    # elif criteria == 2:
    #     print('Getting a random set of ' + str(cfg._numberOfPics)) # +
    #           ' Photos with no less than ' + str(cfg._newerPhotos/365) +
    #           ' years')
    #     files = sorted(os.listdir(cfg._sourceFolder), key=os.path.getctime)
    #     # while files[i]. os.path.getctime > cfg._newerPhotos:
    #     for i in range(cfg._numberOfPics):
    #         newest = files[-i]
    #         return random.sample(newest, cfg._numberOfPics)
    # elif criteria == 3:
    #     files = sorted(os.listdir(cfg._sourceFolder),
    #         key=os.path.getctime, reverse = True)
    #     return random.sample(files, cfg._numberOfPics)
    #  elif:
    #      oldest = files[0]
    else:
        logging.error('Sorting criteria not met n. of files: ' +
                      str(len(filenames)))
        print('Sorting criteria not met')


# IMPURE
def folderPrunning(folder=cfg._destinationFolder,
                   csv_file=cfg._csvDB,
                   multiplier=1,
                   upper_limit=cfg._foldersizeUpperLimit,
                   size=cfg._numberOfPics):
    '''
        checking size of the destination folder to trigger a cleanup

    '''
    folderSize = getSizeMB(folder)
    logging.info('Destination folder Size ' + str(folderSize) + 'Mb')
    if folderSize > upper_limit:
        logging.debug('Prunning folder in ' + csv_file)
        filenames = rebuild_path_from_csv(csv_file, 'destination_folder',
                                          clean=True)
        # print(filenames)
        if len(filenames) > (cfg._numberOfPics * multiplier):
            prune = sorting(filenames, 1, size * multiplier)
        else:
            prune = sorting(filenames, 1, size * int(multiplier/2))
        logging.debug(f'To be pruned: {prune}')
        for fname in prune:
            logging.info('Removing file ' + fname)
            filePrunning(fname, csv_file)
        if getSizeMB(folder) == folderSize:
            logging.error('FOLDER PRUNNING FAILED')
            return False
        else:
            logging.info('Folder Size after prunning ' +
                         str(getSizeMB(folder)) + 'Mb')
    else:
        logging.info(str(folderSize) + ' smaller than ' + str(upper_limit))
    return True


def filePrunning(_file, csv_file=cfg._csvDB, folder=cfg._destinationFolder):
    logging.debug("Running filePrunning()")
    try:
        temp_dict = update_record_csv(_file, csv_file,
                                      destination_folder='',
                                      favorite=False,
                                      deleted=True)
        logging.debug(temp_dict)
        logging.debug(_file)
        if temp_dict['source_folder'] not in _file and folder in _file:
            os.remove(_file)
            head, tail = os.path.split(_file)
            thumbnail_removal(head, tail)

        elif folder not in _file:
            if folder[-1] == '/':
                os.remove(''.join(folder + _file))
            else:
                os.remove(''.join(folder + '/' + _file))
            # os.remove(folder + _file)
            thumbnail_removal(folder, _file)

        else:
            # This code should delete a picture from source
            logging.critical('ATTENTION: DELETING ORIGINAL FILE')
            # os.remove(str(temp_dict['SOURCE_folder']) + _file)

    except OSError as e:
        logging.error(e.errno)
        logging.error('FILE NOT FOUND ' + _file)
        return 'File Not Found: ' + _file
    else:
        logging.info('file removed ' + _file)
        return 'File removed: ' + _file


def thumbnail_removal(_folder, _file):
    """
    docstring
    """
    try:
        filename, file_extension = os.path.splitext(_file)
        # Thumbnail removal changes in index.html
        # may require adjustments here:
        logging.info('Removing Thumbnail: ' + _folder + '/thumbnail/' +
                     filename + '_200x200_fit_90' + file_extension)
        os.remove(_folder + '/thumbnail/' +
                  filename + '_200x200_fit_90' + file_extension)

    except OSError as e:
        logging.error(e.errno)
        logging.error('THUMBNAIL NOT FOUND ' + _file)
        return 'THUMBNAIL Not Found: ' + _file
    else:
        logging.info('THUMBNAIL removed ' + _file)
        return 'THUMBNAIL removed: ' + _file


def fileRotate(path, _file, side='left', csv=cfg._csvDB):
    logging.debug("Running fileRotate()")
    try:
        picture = Image.open(path + _file)
        print(path + _file)
        print(picture)

        filename, file_extension = os.path.splitext(_file)
        if side == 'left' or side == 90:
            rotateBy = 90
        elif side == 'right' or side == 270:
            rotateBy = 270
        else:
            rotateBy = 180
        
        new_path = path + filename + '_' + side + file_extension
        picture.rotate(rotateBy, expand=True).save(new_path)
        record = Photo.byPath(new_path)
        recordDict = record.asdict()
        recordDict.update({'destination_folder': cfg._destinationFolder,
                          'rotate': rotateBy})
        picture.close()
        add_record_csv(recordDict, csv)
        filePrunning(_file)
    except OSError as e:
        logging.error(e.errno + e)
        logging.error('Failed to rotate ' + path + _file)
        return 'Failed to rotate: ' + path + _file
    else:
        logging.info(f'file rotated {side}: {_file}')
        return f'file rotated {side}: {_file}'



# ++++++++++++++++++++++++++++++++++++++
# ---------old list_module.py----------
# ++++++++++++++++++++++++++++++++++++++

# https://www.codespeedy.com/find-the-common-elements-in-two-lists-in-python/
# payload = request.get_data().decode("utf-8")
# list = getListOfFiles(cfg._destinationFolder)

def common(lst1, lst2):
    if type(lst1) is str:
        return common_string_in_list(lst1, lst2)
    elif type(lst2) is str:
        return common_string_in_list(lst2, lst1)
    else:
        return list(set(lst1).intersection(lst2))
        # return list(set(lst1) & set(lst2))


def uncommon(base_list, special_list):
    # remove EOL special string
    # base_list = [item.replace('\n', '') for item in base_list]
    # special_list = [item.replace('\n', '') for item in special_list]
    a = set(base_list)
    b = set(special_list)
    # print(base_list, a)
    # print(special_list, b)
    # print(list(a - b))
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


# def append_multiple_lines(file_name, lines_to_append):
#     # Open the file in append & read mode ('a+')
#     with open(file_name, "a+") as file_object:
#         appendEOL = False
#         # Move read cursor to the start of file.
#         file_object.seek(0)
#         # Check if file is not empty
#         data = file_object.read(100)
#         if len(data) > 0:
#             appendEOL = True
#             file_object.seek(0)
#             source = file_object.readlines()
#             # clear unwanted EOL from original file
#             source = [item.replace('\n', '') for item in source]
#             # remove possible duplicates
#             lines_to_append = uncommon(lines_to_append, source)
#         # Iterate over each string in the list
#         for line in lines_to_append:
#             # If file is not empty then append '\n' before first line for
#             # other lines always append '\n' before appending line
#             if appendEOL:
#                 file_object.write("\n")
#             else:
#                 appendEOL = True
#             # Append element at the end of file
#             file_object.write(line)


def reset_config(option=True):
    stp.clean_folders(warning=0)
    if option:
        stp.setup()
    else:
        # update requirements for packing prior uplod to GitHub
        stp.enhance_requirements()


def common_test():
    a = [2, 9, 4, 5]
    b = [3, 5, 7, 9]
    c = '2,9,4,5'
    print('[9, 5] ==', common(a, b))
    print('[5, 9] ==', common(b, c))
    print('[2, 4] ==', uncommon(a, b))
    print(uncommon(b, c))


# --------------------------------
# Main function copy photos based on the parameters selected
# --------------------------------
def copy_job():
    logging.info('--------COPY JOB START--------')
    start = datetime.datetime.now()
    print('Job Start time:', start)
    logging.info('Loading list of available photos from: ' + cfg._sourceFolder)
    filenames = update_csv_ListOfFiles(cfg._sourceFolder,
                                       cfg._csvDB, clean=True)
    logging.info('Found: ' + str(len(filenames)) + ' available files')
    logging.info('choosing and Sorting the sample')
    sample = sorting(filenames, cfg._criteria, cfg._numberOfPics)

    if sample is not False:
        logging.info('-------PRUNNING--------')
        if (folderPrunning(multiplier=2)):
            logging.info('Number of selected files on the sample: ' +
                         str(len(sample)))
            # keeping source address of all files for backtrack
            # append_multiple_lines(cfg._csv_source, sample)
            copyFiles(sample)
        else:
            logging.error('Error! Failed to prune destination folder\n \
                        NO FILES COPIED.')

    logging.info('New folder Size ' +
                 str(getSizeMB(cfg._destinationFolder)) + 'Mb')
    logging.info('-' * 30)
    end = datetime.datetime.now()
    print('Job finish time:', end)
    logging.info('Time elapsed:' + str(end-start) + 'secs')
    logging.info('--------COPY JOB END----------')


if __name__ == '__main__':
    copy_job()
