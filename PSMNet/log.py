import logging
import logging.config
import time

logfile = 'log/submission.log'

# write to file
# logging.basicConfig(filename=logfile,
#                     filemode='a',
#                     format='%(asctime)s-%(levelname)s-%(message)s',
#                     datefmt='%y%m%d:%H:%M:%S',
#                     level=logging.DEBUG)

# no write to file
# logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s',
#                     datefmt='%y%m%d:%H:%M:%S',
#                     level=logging.DEBUG)                    

def writelog(logfile, msg):
    f = open(logfile, "w")
    f.write(msg)
    f.close()

def trace(msg = "trace here!",key="debug",  _exit = False):

    dictKey = { 'debug': 'DEBUG',
                'err': 'ERROR',
                'info': 'INFO'
                }

    print("{}-[{}]-{}".format(time.strftime("%y%m%d:%H:%M:%S"),dictKey[key], str(msg)))
    if _exit:
        exit()
logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')