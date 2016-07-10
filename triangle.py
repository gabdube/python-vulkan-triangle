"""
    Minimalistic vulkan triangle example powered by asyncio. The demo
    should run on Windows and Linux. For more information see the readme 
    of the project

    To run this demo call:  
    ``python triangle.py``

    @author: Gabriel Dubé
"""

import platform, asyncio

system_name = platform.system()
if system_name == 'Windows':
    from win32 import Win32Window as Window
elif system_name == 'Linux':
    from xlib import XlibWindow as Window
else:
    raise OSError("Platform not supported")

class Application(object):

    def __init__(self):
        
        self.window = Window()

def main():
    # I never execute my code in the global scope of the project to make sure
    # that every ressources will be deallocated before the EOF is reached.
    # In this case "app" (and all the ressources associated) will be freed once
    # main return.
    app = Application()

    loop = asyncio.get_event_loop()
    loop.run_forever()


if __name__ == '__main__':
    main()