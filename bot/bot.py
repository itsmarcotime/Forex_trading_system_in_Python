import json
from infrastructure.log_wrapper import LogWrapper

class Bot:

    ERROR_LOG = "error"
    MAIN_LOG = "main"

    def __init__(self):
        self.setup_logs()

    def setup_logs(self):
        self.logs = {}
        self.logs[Bot.ERROR_LOG] = LogWrapper(Bot.ERROR_LOG)
        self.logs[Bot.MAIN_LOG] = LogWrapper(Bot.MAIN_LOG)


