# built from example in:
# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679


import time, logging
from timeloop import Timeloop
from datetime import timedelta
# Running as standalone or part of the application
if __name__ == '__main__' or __name__ == 'timeloop_module':
    from FileModule import main
    import app_config as cfg
    from loggerinitializer import initialize_logger
    initialize_logger(cfg._logPath)
else: 
    import engine.app_config as cfg
    # from engine.loggerinitializer import initialize_logger 
    from engine.FileModule import main

tl = Timeloop()

@tl.job(interval=timedelta(seconds=10))
def copy_job():
    logging.info("Auto job current time : {}".format(time.ctime()))
    main()
    time.sleep(15)
    return "Auto job running every 10 seconds"
    
# @tl.job(interval=timedelta(seconds=5))
# def sample_job_every_5s():
#     print ("5s job current time : {}".format(time.ctime()))
    
# @tl.job(interval=timedelta(seconds=10))
# def sample_job_every_10s():
#     print ("10s job current time : {}".format(time.ctime()))


def timed_copy():
    try:
        tl.stop()
        time.sleep(5)
        return 'Stopping running job... in 5s', 'warning'
    except RuntimeError as e:
        return e, 'error'
    finally:
        try:
            # tl.start()
            tl.start(block=True)
            return 'Auto copy job successfully enabled'
        except RuntimeError as e:
            return e, 'critical'
        else:
            return 'Auto Copy failed. Reverting to manual', 'error'
            copy_job()
        finally:
            return 'Copy Job triggers on-demand and resets timed copy.', 'warning'

if __name__ == "__main__":
    # tl.start(block=True)
    print(timed_copy())