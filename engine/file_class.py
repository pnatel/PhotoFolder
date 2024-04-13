#!/usr/bin/env python3

# By Paulo Natel
# Dec/2020
# pnatel@live.com

# Check README.md for more information

# Importing required libraries
import os.path
import logging

# Running as standalone or part of the application
# # print(__name__)
# if __name__ == '__main__' or __name__ == 'file_class':
#     import app_config as cfg
#     from loggerinitializer import initialize_logger
#     import setup as stp
#     stp.setup()

# else:
#     import engine.app_config as cfg
#     from engine.loggerinitializer import initialize_logger


# cfg.load_config()
# initialize_logger(cfg._logPath)


class Photo:
    """
    docstring
    """

    def __init__(self, filename, source_folder, destination_folder, datetime,
                 size, favorite=False, deleted=False, rotate=0, counter=0):
        self.filename = filename
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.datetime = datetime
        self.size = size
        self.favorite = favorite
        self.deleted = deleted
        self.rotate = rotate
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
            'rotate': self.rotate,
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
        print(self.rotate)
        print(self.counter)
