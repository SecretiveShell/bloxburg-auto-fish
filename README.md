# bloxburg-auto-fish

This is my program for automatically fishing in bloxburg. It runs on python3 and requires you to install the following dependencies.
|library|command|
|---|---|
|[opencv](https://pypi.org/project/opencv-python/)|`pip install opencv-python`|
|[pynput](https://pypi.org/project/pynput/)|`pip install pynput`|
|[mss](https://pypi.org/project/mss/)|`pip install mss`|

You will need to ajust the BBOX inside the script for your monitor size. It is currently setup for my 4k monitor. Make sure it does not include GUI elements like the mood display or you will need to modify the skript to mask them out.

Please understand that the pre-built opencv bindings do not support GPU acceleration so if you have a NVIDEA/AMD GPU you should compile the binary from source.
