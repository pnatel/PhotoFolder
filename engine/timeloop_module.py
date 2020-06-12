# built from example in:
# https://pypi.org/project/timeloop/
# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679


import time, logging, os
from timeloop import Timeloop
from datetime import timedelta
# Running as standalone or part of the application
if __name__ == '__main__' or __name__ == 'timeloop_module':
    from FileModule import main
    import app_config as cfg
    from loggerinitializer import initialize_logger
else: 
    import engine.app_config as cfg
    from engine.loggerinitializer import initialize_logger 
    from engine.FileModule import main

initialize_logger(cfg._logPath)

cfg.load_config()
tl = Timeloop()

@tl.job(interval=timedelta(seconds=cfg._jobInterval))
def copy_job():
    logging.info("Auto job running every {} seconds".format(cfg._jobInterval))
    logging.info("Auto job current time : {}".format(time.ctime()))
    main()
    notification()
    # time.sleep(15)
    
# @tl.job(interval=timedelta(seconds=5))
# def sample_job_every_5s():
#     print ("5s job current time : {}".format(time.ctime()))
    
# @tl.job(interval=timedelta(seconds=10))
# def sample_job_every_10s():
#     print ("10s job current time : {}".format(time.ctime()))

def notification():
    command = cfg._command
    # if os.name == "nt":
    #     command = "dir" 
    # else:
    #     command = "ls -l"
    os.system(command)

if __name__ == "__main__":
    tl.start(block=True)
    