#!/usr/bin/env python

system = dict(
    mock = False
)

video = dict(
    stdTimelapseSeconds = 5,
    stdOutputFolder = '/media/pi/video/'
)

sensors = dict(
    motion = dict(
        gpioPort = 4
    )
)

logger = dict(
    # DEBUG or other
    level = 'INFO'
)
