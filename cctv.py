#!/usr/bin/python
from gpiozero import MotionSensor
import signal
import threading

from Interruptor import Interruptor
from IntervalIncrementalVideoRecorder import IntervalIncrementalVideoRecorder
from Splash import Splash
from Logger import Logger

logger = Logger()

logger.debug(" Instantiating threading lock                                       :: MAIN")
threadingLock = threading.Lock()

logger.debug(" Instantiating custom video recorder                                :: MAIN")
videoRecorder = IntervalIncrementalVideoRecorder(threadingLock, logger)

# this same interruptor could be shared by all threads including main one, or not
interruptor = Interruptor(logger, [videoRecorder])

logger.log(" Binding video recorder to motion sensor                            :: MAIN")
motionSensor = MotionSensor(4)
motionSensor.when_motion = videoRecorder.startRecording

# Capture Ctrl+C
signal.signal(signal.SIGINT, interruptor.abort)

splash = Splash()
splash.display()

logger.log(" CCTV IS UP AND RUNNING (CTRL+C to terminate)...                    :: MAIN")
# wait for sensors' data
signal.pause()
