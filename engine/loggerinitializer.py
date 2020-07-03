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
 
def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
     
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "error_{}.log".format(__name__)),"w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "debug_{}.log".format(__name__)),"w")
    handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)