"""
    Minimalistic vulkan triangle example powered by asyncio. The demo
    should run on Windows and Linux. For more information see the readme 
    of the project

    To run this demo call:  
    ``python triangle.py``

    @author: Gabriel Dubé
"""

import platform, asyncio, vk
from ctypes import cast, c_char_p, pointer, POINTER, byref

system_name = platform.system()
if system_name == 'Windows':
    from win32 import Win32Window as Window
elif system_name == 'Linux':
    from xlib import XlibWindow as Window
else:
    raise OSError("Platform not supported")

class Application(object):

    def create_instance(self):
        """
            Setup the vulkan instance
        """
        app_info = vk.ApplicationInfo(
            s_type=vk.STRUCTURE_TYPE_APPLICATION_INFO, next=vk.NULL,
            application_name=b'PythonText', application_version=0,
            engine_name=b'test', engine_version=0, api_version=((1<<22) | (0<<12) | (0))
        )

        if system_name == 'Windows':
            extensions = (b'VK_KHR_surface', b'VK_KHR_win32_surface')
        else:
            extensions = (b'VK_KHR_surface', b'VK_KHR_xcb_surface')

        extensions = [c_char_p(x) for x in extensions]
        _extensions = cast((c_char_p*len(extensions))(*extensions), POINTER(c_char_p))

        create_info = vk.InstanceCreateInfo(
            s_type=vk.STRUCTURE_TYPE_INSTANCE_CREATE_INFO, next=vk.NULL, flags=0,
            application_info=pointer(app_info), enabled_layer_count=0,
            enabled_layer_names=vk.NULL_LAYERS, enabled_extension_count=len(extensions),
            enabled_extension_names=_extensions
        )

        instance = vk.Instance(0)
        result = vk.CreateInstance(byref(create_info), vk.NULL, byref(instance))
        if result == vk.SUCCESS:
            print(instance)
            return instance
        else:
            raise RuntimeError('Instance creation failed. Error code: {}'.format(result))

    def __init__(self):
        self.window = Window()
        self.instance = self.create_instance()

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