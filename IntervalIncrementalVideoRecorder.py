from picamera import PiCamera
import threading
import time
import datetime

class IntervalIncrementalVideoRecorder():
    def __init__(self, threadingLock, logger):
        self.threadingLock = threadingLock
        self.logger = logger

        self.camera = PiCamera()
        self.lastRecordingStart = None
        self.recordingStopper = None
        self.status = "STANDBY"

        # TODO configuration
        self.recordingInterval = datetime.timedelta(seconds=20)
        # TODO configuration
        self.recordingPath = '/home/pi/'
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
            self.camera.start_preview()
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
        self.logger.debug("  attempting : stopRecording              :: IntervalIncrementalVideoRecorder")

        self.camera.stop_recording()
        self.camera.stop_preview()
        self.status = "STANDBY"

        self.logger.log("  --- STDBY* [" + str(datetime.datetime.now()) \
            + "]                                                           ---")

        self.threadingLock.release()

    def gracefullyShutdown(self):
        if not self.recordingStopper is None:
            self.recordingStopper.cancel()
        self.stopRecording()

    def isRecording(self):
        return self.status == "RECORDING" \
            and not self.recordingStopper is None \
            and self.recordingStopper.isAlive()
