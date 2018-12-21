import sys

class Interruptor():
    def __init__(self, logger, stoppableServices):
        self.shutdown = False
        self.logger = logger
        self.stoppableServices = stoppableServices
        
    def abort(self, sig, frame):
        self.shutdown = True
        for service in self.stoppableServices:
            service.gracefullyShutdown()
        self.logger.log(" CCTV SHUT DOWN                                                     :: MAIN")
        sys.exit(0)
