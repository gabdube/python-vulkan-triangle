# Vulkan in Python

This project use python and vulkan to draw a triangle in a window using ctypes for bindings.  
The program is stand-alone, you don't have to install anything.  
It was tested on Windows 10 and Ubuntu 16.04 LTS using a R9 380, windows 10 using a A-10-7300 Radeon R6 (integrated GPU). All configuration using the kastest available drivers.

To run the program, simple call  
`python triangle.py`

The program is kind of a port of the vulkan example by Sascha Willems (at <https://github.com/SaschaWillems/Vulkan> ). All credits to him.

## Performances

Windows 10 / R9 380 / i7 3770 @ 3.4 GHZ : ~ 2700 fps (python) VS ~4000 fps (c++)  
Windows 10 / A-10-7300 Radeon R6 : ~ 1500 fps (python) VS TBD  
Ubuntu 16.04 LTS/ R9 380 / i7 3770 @ 3.4 GHZ : TBD  