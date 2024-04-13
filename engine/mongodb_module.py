##!/usr/bin/env python3

# By Paulo Natel
# Jan/2021
# pnatel@live.com

# Check README.md for more information

# Importing required libraries
import pymongo
import logging
import file_class as fc
import FileModule as fm

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

# overwriting MongoDB credentials:
cfg._dbUser = 'pnatel'
cfg._dbPass = 'vJWWpiAIPt4I8L3D'
cfg._dbName = 'photoFolderDB'

# Connect/open/create connecton with MOngoDB
url = cfg._MongoURL
client = pymongo.MongoClient(f'{url}')
print(f'f{url}')

def openDB(dbName):
    dbList = client.list_database_names()
    if dbName in dbList:
        logging.info("The database exists.")
    else:
        logging.info(f'Database {dbName} not in the list: {dbList}')
    return client[dbName]


# MongoDB Create Collection
# -------------------------

def createCollection(name, db):
    """
    docstring
    """
    return db[name]


def printCollectionItems(query):
    """
    docstring
    """
    # for item in query:
    print('------------printCollectionItems---------------')
    for x in query:
        print(x)


# MongoDB Insert Documents in Collection
# --------------------------------------

def addDocument(dictDoc, collection):
    """
    docstring
    """
    return collection.insert_one(dictDoc)


def addDocuments(list_dictDoc, collection):
    """
    docstring
    """
    return collection.insert_many(list_dictDoc)


def add_multiple_records(list_file_paths, table, destination_folder=''):
    """
        docstring
    """
    for file_path in list_file_paths:
        record = Photo.byPath(file_path, destination_folder)
        addDocument(record.asdict(), table)
    return len(list_file_paths)

# MongoDB Retrieve Documents in Collection
# ----------------------------------------



# MongoDB Update Documents in Collection
# --------------------------------------



# MongoDB Delete Documents in Collection
# --------------------------------------

if __name__ == "__main__":

    db = openDB(cfg._dbName)

    collection = createCollection("source_files", db)

    list_of_files = fm.getListOfFiles(cfg._sourceFolder)

    print('n. of docs: ', add_multiple_records(list_of_files, collection))

    printCollectionItems(collection.find().sort("name", 1))
