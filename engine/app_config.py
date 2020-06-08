import configparser
import logging

# Running as standalone or part of the application
if __name__ == '__main__' or __name__ == 'app_config':
    from loggerinitializer import initialize_logger
else: 
    from engine.loggerinitializer import initialize_logger


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

config = configparser.ConfigParser()
config.read('../config.ini')

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

def print_config():
    config.read('config.ini')
    return {s:dict(config.items(s)) for s in config.sections()}

def load_config():
    logging.info('Loading config')
    config.read('config.ini')

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

    # Force testing environment with 'True' in config.ini
    _test = ConfigSectionMap('test')['test_mode']
    logging.debug('_test = '+ _test + ' ')
    
    if _test.lower() == 'true':
    # if len(argv) > 1 or _test:  
    #    print ('Arguments: ', argv[1:])
        _logPath = ConfigSectionMap('test')['logpath']
        # initialize_logger(_logPath)
        logging.info('Test mode loading config')
        _sourceFolder = ConfigSectionMap('test')['sourcefolder']
        _destinationFolder = ConfigSectionMap('test')['destinationfolder']
        _numberOfPics = int(ConfigSectionMap('parameter')['numberofpics_test'])
        _foldersizeUpperLimit = int(ConfigSectionMap('parameter')['foldersizeupperlimit_test'])
        _jobInterval = int(ConfigSectionMap('parameter')['jobinterval_test'])
    else:
        _logPath = ConfigSectionMap('folder')['logpath']
        # initialize_logger(_logPath)
        logging.info('Loading PRODUCTION config')
        _sourceFolder = ConfigSectionMap('folder')['sourcefolder']
        _destinationFolder = ConfigSectionMap('folder')['destinationfolder']
        _numberOfPics = int(ConfigSectionMap('parameter')['numberofpics']) 
        _foldersizeUpperLimit = int(ConfigSectionMap('parameter')['foldersizeupperlimit'])
        _jobInterval = int(ConfigSectionMap('parameter')['jobinterval'])

    _fileType = tuple(dict(config.items('ext')).values())
    # _MaxNumberOfPics = int(ConfigSectionMap('parameter')['MaxNumberOfPics'])
    _newerPhotos = ConfigSectionMap('parameter')['newerphotos']
    _criteria = int(ConfigSectionMap('sort')['criteria'])
    # _logLevel = ConfigSectionMap('loglevel')['level']
    _port = ConfigSectionMap('parameter')['port']
    

# load_config()

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

    print (_sourceFolder, _destinationFolder, _logPath, _fileType, \
        _numberOfPics, _MaxNumberOfPics, _foldersizeUpperLimit, \
        _newerPhotos, _criteria)
    print(print_config())

if __name__ == '__main__':
    test()
