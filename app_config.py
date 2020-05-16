import configparser
import logging

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

config = configparser.ConfigParser()
config.read('config.ini')

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

    # Force testing environment with 'True' in config.ini
_test = ConfigSectionMap('test')['test_mode']

if _test:
# if len(argv) > 1 or _test:  
#    print ('Arguments: ', argv[1:])
    logging.debug('Test mode loading config')
    _sourceFolder = ConfigSectionMap('test')['sourcefolder']
    _destinationFolder = ConfigSectionMap('test')['destinationfolder']
    _logPath = ConfigSectionMap('test')['logpath']
    _numberOfPics = int(ConfigSectionMap('parameter')['numberofpics_test'])
    _foldersizeUpperLimit = int(ConfigSectionMap('parameter')['foldersizeupperlimit_test'])
else:
    _sourceFolder = ConfigSectionMap('folder')['sourcefolder']
    _destinationFolder = ConfigSectionMap('folder')['destinationfolder']
    _logPath = ConfigSectionMap('folder')['logpath']
    _numberOfPics = int(ConfigSectionMap('parameter')['numberofpics']) 
    _foldersizeUpperLimit = int(ConfigSectionMap('parameter')['foldersizeupperlimit'])

_fileType = tuple(dict(config.items('ext')).values())
# _MaxNumberOfPics = int(ConfigSectionMap('parameter')['MaxNumberOfPics'])
_newerPhotos = ConfigSectionMap('parameter')['newerphotos']
_criteria = int(ConfigSectionMap('sort')['criteria'])
# _logLevel = ConfigSectionMap('loglevel')['level']

