from picamera import PiCamera
import threading
import time
import datetime

import config

class IntervalIncrementalVideoRecorder():
    def __init__(self, threadingLock, logger):
        self.threadingLock = threadingLock
        self.logger = logger

        self.camera = PiCamera()
        self.lastRecordingStart = None
        self.recordingStopper = None
        self.status = "STANDBY"
        self.recordingsFileNames = []

        self.recordingInterval = datetime.timedelta(seconds=config.video['stdTimelapseSeconds'])
        self.recordingPath = config.video['stdOutputFolder']
        if not self.recordingPath.endswith("/"):
            self.recordingPath = self.recordingPath + "/"

    def calculateRecordingInterval(self):
        self.logger.debug("  calculateRecordingInterval              :: IntervalIncrementalVideoRecorder")
        self.lastRecordingStart = datetime.datetime.now()
        self.logger.debug("  " + format(self.recordingInterval.seconds) \
                          + "          :: calculateRecordingInterval :: IntervalIncrementalVideoRecorder")
        return self.recordingInterval.seconds

    def calculateVideoFileName(self):
        now = datetime.datetime.now()
        fileName = format(now.year, "04") + format(now.month, "02") + format(now.day, "02") + \
            "_" + format(now.hour, "02") + format(now.minute, "02") + format(now.second, "02")
        return self.recordingPath + fileName + ".h264"

    def startRecording(self):
        self.threadingLock.acquire()
        self.logger.debug("  attempting : startRecording             :: IntervalIncrementalVideoRecorder")

        curRecordingInterval = self.calculateRecordingInterval()

        if not self.isRecording():
            fileName = self.calculateVideoFileName()
            self.logger.log("  --- REC* " + fileName + " [" + str(datetime.datetime.now()) + "] " \
                + " :: startRecording :: IntervalIncrementalVideoRecorder")
            self.status = "RECORDING"
            
            if not config.system['mock']:
                self.recordingsFileNames.append(fileName)
                self.camera.start_recording(fileName)
        else:
            self.logger.log("  --- REC* EXTENSION [" + str(datetime.datetime.now()) \
                + "]                                                    ---")

        if not self.recordingStopper is None:
            self.logger.debug("  cancelling previous stopper :: startRecording :: IntervalIncrementalVideoRecorder")
            self.recordingStopper.cancel()

        self.recordingStopper = threading.Timer(curRecordingInterval, self.stopRecording)
        self.logger.debug("  programming next stopper :: startRecording :: IntervalIncrementalVideoRecorder")

        self.recordingStopper.start()

        self.logger.debug("  done : startRecording                   :: IntervalIncrementalVideoRecorder")

        self.threadingLock.release()

    def stopRecording(self):
        self.threadingLock.acquire()
        
        if self.status != "RECORDING":
            self.threadingLock.release()
            return
        
        self.logger.debug("  attempting : stopRecording              :: IntervalIncrementalVideoRecorder")

        if not config.system['mock']:
            self.camera.stop_recording()
        
        self.status = "STANDBY"

        self.logger.log("  --- STDBY* [" + str(datetime.datetime.now()) \
            + "]                                                           ---")

        self.threadingLock.release()

    def gracefullyShutdown(self):
        self.threadingLock.acquire()
        
        self.logger.log("Shut down in progress...")
        
        if not self.recordingStopper is None:
            self.logger.debug("   stopping in-progress video recording")
            self.recordingStopper.cancel()
            
        # release lock since stopRecording will acquire it
        self.threadingLock.release()
        
        self.stopRecording()
        
        self.logger.log("     Files recorded " + str(len(self.recordingsFileNames)) + ": ")
        for fileName in self.recordingsFileNames:
            self.logger.log("     * " + fileName)
        self.logger.log("     listed " + str(len(self.recordingsFileNames)) + " files.")

    def isRecording(self):
        return self.status == "RECORDING" \
            and not self.recordingStopper is None \
            and self.recordingStopper.isAlive()
