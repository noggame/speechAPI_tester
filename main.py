import logging
import os
from datetime import datetime


logging.basicConfig(filename=f'{os.getcwd()}/logs/result_test_{datetime.now().strftime("%Y%d%m%H%M%S")}.log',
                            level=logging.INFO,
                            format='%(asctime)s %(message)s')