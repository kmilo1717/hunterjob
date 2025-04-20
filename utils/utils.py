# utils.py
from config import HIGHLIGHTS
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

import re

def salary_to_int(text):
    try:
        text = text.lower()
        if text == 'no especificado':
            return 0
        text = text.split(',')[0]
        numbers_only = re.sub(r'[^0-9]', '', text)
        return int(numbers_only) if numbers_only else 0
    except Exception as e:
        return 0

def highlights(texto):
    for palabra in HIGHLIGHTS:
        texto = re.sub(
            fr'({re.escape(palabra)})',
            r'<b>\1</b>',
            texto,
            flags=re.IGNORECASE
        )
    return texto
