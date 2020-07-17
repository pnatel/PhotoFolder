# main idea from:
# https://aykutakin.wordpress.com/2013/08/06/logging-to-console-and-file-in-python/

# usage:
# logging.debug("debug message")        Detailed information, typically of interest only when diagnosing problems.
# logging.info("info message")          Confirmation that things are working as expected.
# logging.warning("warning message")    An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
# logging.error("error message")        Due to a more serious problem, the software has not been able to perform some function.
# logging.critical("critical message")  A serious error, indicating that the program itself may be unable to continue running.

import logging
import os.path
from distutils.util import strtobool

# Running as standalone or part of the application
# print(__name__)
if __name__ == '__main__' or __name__ == 'loggerinitializer':
    import app_config as cfg
else: 
    import engine.app_config as cfg

# cfg.load_config()

def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    if bool(strtobool(cfg._test.capitalize())): 
        # create console handler and set level to info
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
 
    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "error.log"),"w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "debug.log"),"w")
    handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)