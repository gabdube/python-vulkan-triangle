# Vulkan in Python

This project use python and vulkan to draw a triangle in a window using ctypes for bindings.  
The program is stand-alone, you don't have to install anything.  
It was tested on Windows 10 and windows 10 using a A-10-7300 Radeon R6 (an APU). All configuration are using the lastest available drivers.

To run the program, simple call  
`python triangle.py`

The program is kind of a port of the vulkan example by Sascha Willems (at <https://github.com/SaschaWillems/Vulkan> ). All credits to him.

## Requirements

**Python 3.5** (I use asyncio to handle the system events and the rendering phase asynchronously)  
The latest Vulkan driver  
Windows **or** Linux (only tested on Ubuntu 16.04 LTS)  
XCB (only on linux)  

Also make sure that the vulkan library is visible to the program. If the program can't find it and error about "libvulkan.so" being not found will be raised.


## Performances

Keep in mind that the program is not a 1:1 copy of the original example.

Windows 10 / R9 380 / i7 3770 @ 3.4 GHZ : ~ 4000 fps (python/no debugger)  VS ~4300 fps (c++/Release build)  
Windows 10 / A-10-7300 Radeon R6 : ~ 750 fps (python/no debugging) VS 750 fps (c++)  
Ubuntu 16.04 LTS/ R9 380 / i7 3770 @ 3.4 GHZ : ~4800 fps (python no debugger) VS SEGFAULT (c++)  

Not much of a suprise, the c++ version is faster, but not my much. Also while the c++ framerate stays relatively stable ~[+-100], the python framerate
 is much less stable ~(+-300). This is mostly due to the GC I guess.  

On my shitty laptop, the python script is as fast as the c++ release build.  

Suprise. On ubuntu, the python script is faster than the c++ example on Windows. Sadly, I coudn't test the c++ build as it segfault when I try to run it. :(  

## Screenshots

![Alt text](/images/win.png "Image")  
![Alt text](/images/ubuntu.png "Image")  