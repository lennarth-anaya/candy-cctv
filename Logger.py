import sys

import config

class Logger():
    def debug(self, message):
        if config.logger['level'] == 'DEBUG':
            print(message)
    def log(self, message):
        print(message)
