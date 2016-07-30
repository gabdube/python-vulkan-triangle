# Vulkan in Python

This project use python and vulkan to draw a triangle in a window using ctypes for bindings.  
The program is stand-alone, you don't have to install anything.  
It was tested on Windows 10 and Ubuntu 16.04 LTS using a R9 380, windows 10 using a A-10-7300 Radeon R6 (integrated GPU). All configuration using the kastest available drivers.

To run the program, simple call  
`python triangle.py`

The program is kind of a port of the vulkan example by Sascha Willems (at <https://github.com/SaschaWillems/Vulkan> ). All credits to him.

## Its not over

I still need to code the window for linux and create a good wrapper generator for python. I might also try to use a C extension to run the render loop before jumping to something more advanced.

## Performances

Windows 10 / R9 380 / i7 3770 @ 3.4 GHZ : ~ 4000 fps (python/no debugger) VS 2700 fps (python debugger on) VS ~4300 fps (c++/Release build)  
Windows 10 / A-10-7300 Radeon R6 : ~ 1500 fps (python) VS TBD  
Ubuntu 16.04 LTS/ R9 380 / i7 3770 @ 3.4 GHZ : TBD  

Not much of a suprise, the c++ version is faster, but not my much. Also while the c++ framerate stays relatively stable ~[+-100], the python framerate
 is much less stable ~(+-300). This is mostly due to the GC I guess.  
On my shitty laptop, the framerate starts at 800 but steadyly grows to reach 1500 fps. Again the framerate is not very stable ~(+-200).

## Screenshots

![Alt text](/images/win.png "Image")  