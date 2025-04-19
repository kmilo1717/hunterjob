# utils.py
import logging
import os

def setup_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] File: %(filename)s - Line %(lineno)d: %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_filename = os.path.join(log_directory, "app.log")
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
