# candy-cctv

Raspberry Pi Camera and Motion Sensor open source code for recording.

# Setting it up

Edit config.py parameters that suit your needs, especially the parameter stdOutputFolder (TODO: better name)

# Starting it up

sudo python3 cctv.py

# Prioritized TODO

- Adding the capability to somehow easily start/stop recording remotely
- Automatic cleanup of old files - DONE fsassistant
- Live streaming
- Manual relevancy files mark so they are garbage collected as soon as possible and not visible to relevant files
- Possibly, avoid the huge amount of files recorded. Maybe not storing files smaller than 2.5 MB, as per the current observed behavior, perhaps no need to something fancier so far.

