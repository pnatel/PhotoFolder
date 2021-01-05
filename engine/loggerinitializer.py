# main idea from:
# https://aykutakin.wordpress.com/2013/08/06/logging-to-console-and-file-in-python/

# usage:
# logging.debug("debug message")        Detailed information, typically of
#                                       interest only when diagnosing problems.
# logging.info("info message")          Confirmation that things are working
#                                       as expected.
# logging.warning("warning message")    An indication that something unexpected
#                                       happened, or indicative of some problem
#                                       in the near future (e.g. ‘disk space
#                                       low’). The software is still working as
#                                       expected.
# logging.error("error message")        Due to a more serious problem, the
#                                       software has not been able to perform
#                                       some function.
# logging.critical("critical message")  A serious error, indicating that the
#                                       program itself may be unable to keep
#                                       running.

import logging
import os.path
# from distutils.util import strtobool

# Running as standalone or part of the application
# print(__name__)
if __name__ == '__main__' or __name__ == 'loggerinitializer':
    import app_config as cfg
    cfg.load_config()
else:
    import engine.app_config as cfg


def initialize_logger(output_dir):
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    if cfg._test:
        logger.setLevel(logging.DEBUG)
        # create console handler and set level to DEBUG
        # handler = logging.StreamHandler()
        # handler.setLevel(logging.DEBUG)
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        logging.info(f'Loaded DEMO mode. All logs will be recorded in \
                     {output_dir} folder')
    elif cfg._logLevel == 1:
        logger.setLevel(logging.DEBUG)
    elif cfg._logLevel == 2:
        logger.setLevel(logging.INFO)
    elif cfg._logLevel == 3:
        logger.setLevel(logging.WARNING)
    elif cfg._logLevel == 4:
        logger.setLevel(logging.ERROR)
    elif cfg._logLevel == 5:
        logger.setLevel(logging.CRITICAL)
    else:
        logging.critical(f'Error!!! Unable to setup logging level for \
                         {output_dir} folder')
        print(f'\nError! \
              Unable to setup logging level for {output_dir} folder')

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "error.log"), "w",
                                  encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.error(f'Error log file created. \
                  All Errors will be recorded in {output_dir} folder')

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "debug.log"), "w")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.debug(f'DEBUG log file created. All debug level info will be \
                  recorded in {output_dir} folder')


if __name__ == '__main__':
    initialize_logger(cfg._logPath)
    print(cfg._logPath)
