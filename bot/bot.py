import json
from infrastructure.log_wrapper import LogWrapper

class Bot:

    ERROR_LOG = "error"
    MAIN_LOG = "main"

    def __init__(self):
        self.setup_logs()
        self.log_to_main("Bot Started")
        self.log_to_error("Bot Started")

    def setup_logs(self):
        self.logs = {}
        self.logs[Bot.ERROR_LOG] = LogWrapper(Bot.ERROR_LOG)
        self.logs[Bot.MAIN_LOG] = LogWrapper(Bot.MAIN_LOG)

    def log_message(self, msg, key):
        self.logs[key].logger.debug(msg)

    def log_to_main(self, msg):
        self.log_message(msg, Bot.MAIN_LOG)
    
    def log_to_error(self, msg):
        self.log_message(msg, Bot.ERROR_LOG)


