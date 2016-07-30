# Vulkan in Python

This project use python and vulkan to draw a triangle in a window using ctypes for bindings.  
The program is stand-alone, you don't have to install anything.  
It was tested on Windows 10 and windows 10 using a A-10-7300 Radeon R6 (an APU). All configuration are using the lastest available drivers.

To run the program, simple call  
`python triangle.py`

The program is kind of a port of the vulkan example by Sascha Willems (at <https://github.com/SaschaWillems/Vulkan> ). All credits to him.

## Its not over

I still need to code the window for linux and create a good wrapper generator for python. I might also try to use a C extension to run the render loop before jumping to something more advanced.

## Performances

Keep in mind that the program is not a 1:1 copy of the original example.

Windows 10 / R9 380 / i7 3770 @ 3.4 GHZ : ~ 4000 fps (python/no debugger) VS 2700 fps (python debugger on) VS ~4300 fps (c++/Release build)  
Windows 10 / A-10-7300 Radeon R6 : ~ 750 fps (python/no debugging) VS 750 fps (c++)  (python with debugging enabled do not start)
Ubuntu 16.04 LTS/ R9 380 / i7 3770 @ 3.4 GHZ : TBD  

Not much of a suprise, the c++ version is faster, but not my much. Also while the c++ framerate stays relatively stable ~[+-100], the python framerate
 is much less stable ~(+-300). This is mostly due to the GC I guess.  

On my shitty laptop, the python script is as fast as the c++ release build.


## Screenshots

![Alt text](/images/win.png "Image")  