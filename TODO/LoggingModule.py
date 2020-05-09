import logging
import time
 
from logging.handlers import RotatingFileHandler
 
#----------------------------------------------------------------------
def create_rotating_log(path, level=logging.INFO):
    """
    Creates a rotating log
    """
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(level)
 
    # add a rotating handler
    handler = RotatingFileHandler(path, maxBytes=20,
                                  backupCount=5)
    logger.addHandler(handler)
 
    for i in range(10):
        logger.info("This is test log line %s" % i)
        time.sleep(1.5)
 
#----------------------------------------------------------------------
def create_log_file(file_name, level): 
    logging.basicConfig(filename=file_name, level=level)

#----------------------------------------------------------------------

def info(message):
    logging.info(message)

#----------------------------------------------------------------------
if __name__ == "__main__":
    from os import path
    log_file = "logs/test.log"
    
    level = logging.INFO
    if path.isfile(log_file):
        create_rotating_log(log_file)
    else:
        create_log_file(log_file, level)
        create_rotating_log(log_file)
        


