# candy-cctv

Raspberry Pi Camera and Motion Sensor open source code for recording.

# Setting it up

Edit config.py parameters that suit your needs, especially the parameter stdOutputFolder (TODO: better name)

# Starting it up

sudo python3 cctv.py

# TODO

- Automatic cleanup of old files
- Manual relevancy files mark so they are garbage collected as soon as possible and not visible to relevant files
- Live streaming
- Possibly, avoid the huge amount of files recorded by accumulating more motion events, or perhaps keeping it and just analyzing the videos with image analisys to diacard them once recorded, which would be more interesting.
