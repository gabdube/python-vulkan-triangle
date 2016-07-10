"""
    Minimalistic vulkan triangle example powered by asyncio. The demo
    should run on Windows and Linux. For more information see the readme 
    of the project

    To run this demo call:  
    ``python triangle.py``

    @author: Gabriel Dubé
"""

import platform

system_name = platform.system()
if system_name == 'Windows':
    from win32 import Win32Window as Window
elif system_name == 'Linux':
    from xlib import XlibWindow as Window
else:
    raise OSError("Platform not supported")
