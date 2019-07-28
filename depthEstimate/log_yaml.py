#!/usr/bin/env python3

import logging
import logging.config
import yaml
import os
try:
    if not os.path.exists(".log"):
        os.makedirs(".log")
    with open('logconfig.yaml', 'r') as f:
        log_cfg = yaml.safe_load(f.read())
    logging.config.dictConfig(log_cfg)
    logger = logging.getLogger('dev')
    logger.setLevel(logging.DEBUG)

except Exception as identifier:
    logging.error(identifier)
# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')