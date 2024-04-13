import configparser
import logging

# Running as standalone or part of the application
if __name__ == '__main__' or __name__ == 'app_config':
    import setup as stp
else:
    import engine.setup as stp

# Global Variables

_sourceFolder = ''
_destinationFolder = ''
_logPath = ''
_fileType = []
_numberOfPics = 0
_MaxNumberOfPics = 0
_foldersizeUpperLimit = 0
_newerPhotos = 0
_criteria = 0
_jobInterval = 0
_command = ''
_csvDB = ''
# _csv_destination = ''
_logLevel = 0

config = configparser.ConfigParser()


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
        except ValueError as errno:
            logging.error("exception on %s!" % option)
            logging.critical(errno)
            dict1[option] = None
    return dict1


def print_config():
    config.read('data/config.ini')
    return {s: dict(config.items(s)) for s in config.sections()}


def load_config():
    logging.info('Loading config via ' + __name__)
    # config.read('data/config.ini')

    try:
        f = open('data/config.ini')
        f.close()
        config.read('data/config.ini')
    except IOError:
        print("File not accessible")
        stp.setup()
        config.read('data/config.ini')

    global _sourceFolder
    global _destinationFolder
    global _logPath
    global _fileType
    global _numberOfPics
    global _MaxNumberOfPics
    global _foldersizeUpperLimit
    global _newerPhotos
    global _criteria
    global _port
    global _jobInterval
    global _command
    global _test
    global _csvDB
    global _logLevel
    global _DataMode
    global _MongoURL
    global _dbUser
    global _dbPass
    global _dbName

    # Force testing environment with 'True' in config.ini
    _test = config.getboolean('test', 'test_mode')
    # logging.debug('_test = ', _test)

    if _test:
        _logPath = ConfigSectionMap('test')['logpath']
        logging.info('Test mode loading config')
        _sourceFolder = ConfigSectionMap('test')['sourcefolder']
        _destinationFolder = ConfigSectionMap('test')['destinationfolder']
        _numberOfPics = config.getint('test', 'numberofpics')
        _foldersizeUpperLimit = config.getint('test', 'foldersizeupperlimit')
        _jobInterval = config.getint('test', 'jobinterval')
        _command = ConfigSectionMap('test')['command']
    else:
        _logPath = ConfigSectionMap('folder')['logpath']
        logging.info('Loading PRODUCTION config')
        _sourceFolder = ConfigSectionMap('folder')['sourcefolder']
        _destinationFolder = ConfigSectionMap('folder')['destinationfolder']
        _numberOfPics = config.getint('parameter', 'numberofpics')
        _foldersizeUpperLimit = config.getint('parameter',
                                              'foldersizeupperlimit')
        _jobInterval = config.getint('parameter', 'jobinterval')
        _command = ConfigSectionMap('notification')['command']

    _fileType = tuple(dict(config.items('ext')).values())
    # _MaxNumberOfPics = int(ConfigSectionMap('parameter')['MaxNumberOfPics'])
    _newerPhotos = ConfigSectionMap('parameter')['newerphotos']
    _criteria = config.getint('sort', 'criteria')
    _logLevel = config.getint('parameter', 'loglevel')
    _port = ConfigSectionMap('parameter')['port']
    _DataMode = ConfigSectionMap('parameter')['datamode']
    _csvDB = ConfigSectionMap('data')['csvdb']
    _MongoURL = ConfigSectionMap('data')['mongourl']
    _dbUser = ConfigSectionMap('data')['dbuser']
    _dbPass = ConfigSectionMap('data')['dbpass']
    _dbName = ConfigSectionMap('data')['dbname']


def test():

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    load_config()

    logging.info('Print config')

    print(_sourceFolder, _destinationFolder, _logPath, _fileType,
          _numberOfPics, _MaxNumberOfPics, _foldersizeUpperLimit,
          _newerPhotos, _criteria)
    print(print_config())


if __name__ == '__main__':
    test()
