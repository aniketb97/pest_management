import logging
from django.conf import settings
import os
from datetime import datetime
LOG_FILENAME = datetime.now().strftime('worklog_%d_%m_%Y.log')
logger_path = os.path.join(settings.BASE_DIR, 'logs', LOG_FILENAME)
class Logger():
    def __init__(self, logger_name):
        self.logger_name = logger_name
        os.listdir()
        if not os.path.exists(logger_name):
            # with open(logger_path,'w') as fp:
            #     pass
            fp = open(logger_path,'w')
            fp.close()
        # self.log = logging.basicConfig(filename=logger_path, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
        # self.logger = logging.basicConfig(filename=logger_path, filemode='a',
        #                                format='%(asctime)s - %(levelname)s - %(message)s')

    def set_logger(self,message):
        with open(logger_path,'a') as fp:
            fp.write('\n')
            fp.write('{} - {} - {}'.format(datetime.now(), self.logger_name, message))




# logging.basicConfig(filename=logger_path, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')