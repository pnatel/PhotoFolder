#!/usr/bin/env python3

# By Paulo Natel
# Dec/2020
# pnatel@live.com

# Check README.md for more information


# Importing required libraries
from pathlib import Path
import os.path
import shutil
import random
import csv
import logging
import datetime
# from distutils.util import strtobool

# Running as standalone or part of the application
# print(__name__)
if __name__ == '__main__' or __name__ == 'file_class':
    import app_config as cfg
    from loggerinitializer import initialize_logger
    import setup as stp
    stp.setup()

else:
    import engine.app_config as cfg
    from engine.loggerinitializer import initialize_logger


cfg.load_config()
initialize_logger(cfg._logPath)


class Photo:
    """
    docstring
    """

    def __init__(self, filename, source_folder, destination_folder,
                 datetime, size, favorite=False, deleted=False,
                 pruned=False, counter=0):
        self.filename = filename
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.datetime = datetime
        self.size = size
        self.favorite = favorite
        self.deleted = deleted
        self.pruned = pruned
        self.counter = counter
        logging.info('Photo object created: ' + filename)

    @classmethod
    def byPath(self, source_filepath, destination_folder=''):
        """
        docstring
        """
        source_folder, filename = os.path.split(source_filepath)
        logging.debug('Photo object created by path: ' + filename)
        return self(filename, source_folder, destination_folder,
                    os.path.getmtime(source_filepath),
                    os.path.getsize(source_filepath))

    def asdict(self):
        return {
            'filename': self.filename,
            'source_folder': self.source_folder,
            'destination_folder': self.destination_folder,
            'datetime': self.datetime,
            'size': self.size,
            'favorite': self.favorite,
            'deleted': self.deleted,
            'pruned': self.pruned,
            'counter': self.counter
        }

    def print_photo(self):
        """
        docstring
        """
        print(self.filename)
        print(self.source_folder)
        print(self.destination_folder)
        print(self.datetime)
        print(self.size)
        print(self.favorite)
        print(self.deleted)
        print(self.pruned)
        print(self.counter)

    def add_record_csv(self, csv_file):
        """
        docstring
        """
        self.counter = int(self.counter) + 1
        with open(csv_file, 'a+') as file:
            headers = []
            for key in self.asdict().keys():
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
            if self.filename not in read:
                writer.writerow(self.asdict())
                logging.info('adding row for: ' + self.filename)
            else:

                update_record_csv(self.filename, csv_file,
                                  counter=self.counter, pruned=False)
                logging.debug('File already in CSV: ' + self.filename)


# ===============================
# -----non-class functions-------
# ===============================

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
            if temp['pruned']:
                # adjustment of counter due artificial remove/add
                temp['counter'] = int(removed_record['counter']) - 1
            logging.info('SUCCESS: ' + temp['filename'] +
                         ' removed from ' + csv_file)
            # print('\n\n', temp)
            new = Photo(**temp)
            # new.print_photo()
            new.add_record_csv(csv_file)
            logging.info(f"{temp['filename']} successfully updated")
        else:
            logging.info('FAILED: ' + temp['filename']
                         + ' NOT removed from ' + csv_file)
    else:
        logging.error(f"{filename} was NOT changed")
    return temp


def add_multiple_csv_records(list_file_paths, csv_file, destination_folder=''):
    """
        docstring
    """
    for file_path in list_file_paths:
        record = Photo.byPath(file_path, destination_folder)
        record.add_record_csv(csv_file)


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
              destin=cfg._destinationFolder,
              csv=cfg._csv_destination):
    '''
        Copy a list of files to the folder
    '''
    logging.info('Copying ' + str(len(fileList)) + ' files')
#    logging.debug(fileList)

    for fname in fileList:
        if fileTypeTest(fname, ftype):
            logging.debug('Copying file ' + fname)
            shutil.copy(fname, destin)
            Photo.byPath(fname, destin).add_record_csv(csv)


def getSizeMB(folder='.'):
    '''
        returns the size of the folder in bytes
    '''
    root_directory = Path(folder)
    size = sum(f.stat().st_size
               for f in root_directory.glob('**/*')
               if f.is_file())
    return size/(10**6)


# -----------------
# IMPURE
def update_csv_ListOfFiles(dirName, csv_file):
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
            update_csv_ListOfFiles(fullPath, csv_file)
        else:
            if fileTypeTest(entry, cfg._fileType):
                record = Photo.byPath(fullPath)
                record.add_record_csv(csv_file)
            else:
                logging.debug(entry + ' INVALID FILE TYPE ' +
                              str(cfg._fileType))
    if cfg._sourceFolder in dirName:
        return rebuild_path_from_csv(csv_file, 'source_folder')
    else:
        return rebuild_path_from_csv(csv_file, 'destination_folder')


def clear_sample_source(csv_source, csv_destination):
    """
    docstring
    """
    return uncommon(rebuild_path_from_csv(csv_source, 'source_folder'),
                    rebuild_path_from_csv(csv_destination, 'source_folder'))


# IMPURE
def rebuild_path_from_csv(csv_file, folder):
    """
    docstring
    """
    temp = []
    source = read_CSV(csv_file)
    for item in source:
        if item[folder][-1] == '/':
            temp.append(''.join(item[folder] + item['filename']))
        else:
            temp.append(''.join(item[folder] + '/' + item['filename']))
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
                   csv_file=cfg._csv_destination,
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
        filenames = rebuild_path_from_csv(csv_file, 'destination_folder')
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


def filePrunning(_file, csv_file):
    try:
        temp_dict = update_record_csv(_file, csv_file, pruned=True)
#        logging.debug(temp_dict)
        if temp_dict['destination_folder'] != '':
            os.remove(_file)
            # filename, file_extension = os.path.splitext(_file)
            # Thumbnail removal changes in index.html
            # may require adjustments here:
            # os.remove(temp_dict['destination_folder'] + '/thumbnail/' +
            #           filename + '_200x200_fit_90' + file_extension)

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
            if appendEOL:
                file_object.write("\n")
            else:
                appendEOL = True
            # Append element at the end of file
            file_object.write(line)


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
    filenames = clear_sample_source(cfg._csv_source, cfg._csv_destination)
    if filenames == []:
        filenames = update_csv_ListOfFiles(cfg._sourceFolder, cfg._csv_source)
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
    #  photo1 = Photo.byPath('engine/static/demo/source/black-crt-tv-showing-gray-screen-704555.jpg')
    #  photo2 = Photo.byPath('engine/static/demo/source/bandwidth-close-up-computer-connection-1148820.jpg')

    #  photo1.print_photo()
    #  print(photo1.asdict())
    #  photo1.add_record_csv('data/test.csv')
    #  photo2.add_record_csv('data/test.csv')

    #  print(datetime.datetime.fromtimestamp(photo1.datetime))
    # print (remove_record_csv('bandwidth-close-up-computer-connection-1148820.jpg', 'data/test.csv'))
    #  update_record_csv('black-crt-tv-showing-gray-screen-704555.jpg','data/test.csv', favorite = True)
    #  print(read_CSV('data/test.csv'))
    # update_csv_ListOfFiles(cfg._sourceFolder, 'data/test2.csv')
    # filePrunning(pat-whelen-BDeSzt-dhxc-unsplash.jpg, csv_file)
    # print(clear_sample_source('data/test.csv', 'data/test2.csv'))

    copy_job()
