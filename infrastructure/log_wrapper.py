import logging
import os

LOG_FORMAT = "%(asctime)s %(message)s"
DEFAULT_LEVEL = logging.DEBUG

class LogWrapper:
    PATH = "./logs"

    def __init__(self, name, mode="w"):
        self.create_directory()
        self.filename = f"{LogWrapper.PATH}/{name}.log"
        self.logger = logging.getLogger(name)
        self.logger.setLevel(DEFAULT_LEVEL)

        file_handler = logging.FileHandler(self.filename, mode=mode)
        formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.logger.info(f"LogWrapper init() {self.filename}")


    def create_directory(self):
        if not os.path.exists(LogWrapper.PATH):
            os.makedirs(LogWrapper.PATH)