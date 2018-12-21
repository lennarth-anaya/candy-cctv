import sys

class Logger():
    def debug(self, message):
        if 'LOG_LEVEL=DEBUG' in sys.argv:
            print(message)
    def log(self, message):
        print(message)
