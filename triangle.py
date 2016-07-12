"""
    Minimalistic vulkan triangle example powered by asyncio. The demo
    should run on Windows and Linux. For more information see the readme 
    of the project

    To run this demo call:  
    ``python triangle.py``

    @author: Gabriel Dubé
"""

import platform, asyncio, vk
from ctypes import cast, c_char_p, c_uint, pointer, POINTER, byref, c_float

system_name = platform.system()
if system_name == 'Windows':
    from win32 import Win32Window as Window
elif system_name == 'Linux':
    from xlib import XlibWindow as Window
else:
    raise OSError("Platform not supported")

class Swapchain(object):

    def __init__(self, app):
        pass



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
            vk.load_instance_functions(self, instance)
            self.instance = instance
        else:
            raise RuntimeError('Instance creation failed. Error code: {}'.format(result))

    def create_device(self):
        self.gpu = None
        self.main_queue_family = None

        # Enumerate the physical devices
        gpu_count = c_uint(0)
        result = self.EnumeratePhysicalDevices(self.instance, byref(gpu_count), vk.NULL_HANDLE )
        if result != vk.SUCCESS or gpu_count.value == 0:
            raise RuntimeError('Could not fetch the physical devices or there are no devices available')

        buf = (vk.PhysicalDevice*gpu_count.value)()
        self.EnumeratePhysicalDevices(self.instance, byref(gpu_count), cast(buf, POINTER(vk.PhysicalDevice)))

        # For this example use the first available device
        self.gpu = vk.PhysicalDevice(buf[0])

        # Find a graphic queue that supports graphic operation
        queue_families_count = c_uint(0)
        self.GetPhysicalDeviceQueueFamilyProperties(
            self.gpu,
            byref(queue_families_count),
            cast(vk.NULL, POINTER(vk.QueueFamilyProperties))
        )
        if queue_families_count.value == 0:
            raise RuntimeError('No queues families found for the default GPU')

        queue_families = (vk.QueueFamilyProperties*queue_families_count.value)()
        self.GetPhysicalDeviceQueueFamilyProperties(
            self.gpu,
            byref(queue_families_count),
            cast(queue_families, POINTER(vk.QueueFamilyProperties))
        )

        for index, queue in enumerate(queue_families):
            if queue.queue_flags & vk.QUEUE_GRAPHICS_BIT != 0:
                self.main_queue_family = index
                break

        if self.main_queue_family is None:
            raise OSError("Could not find a queue that supports graphics")

        # Create the device
        priorities = (c_float*1)(0.0)
        queue_create_info = vk.DeviceQueueCreateInfo(
            s_type=vk.STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO,
            next=vk.NULL,
            flags=0,
            queue_family_index=self.main_queue_family,
            queue_count=1,
            queue_priorities=priorities
        )

        queue_create_infos = (vk.DeviceQueueCreateInfo*1)(*(queue_create_info,))

        extensions = (b'VK_KHR_swapchain',)
        _extensions = cast((c_char_p*len(extensions))(*extensions), POINTER(c_char_p))
        
        create_info = vk.DeviceCreateInfo(
            s_type=vk.STRUCTURE_TYPE_DEVICE_CREATE_INFO, next=vk.NULL, flags=0,
            queue_create_info_count=1, queue_create_infos=queue_create_infos,
            enabled_layer_count=0, enabled_layer_names=vk.NULL_LAYERS,
            enabled_extension_count=1, enabled_extension_names=_extensions,
            enabled_features=vk.NULL
        )

        device = vk.Device(0)
        result = self.CreateDevice(self.gpu, byref(create_info), vk.NULL, byref(device))
        if result == vk.SUCCESS:
            vk.load_device_functions(self, device, self.GetDeviceProcAddr)
            self.device = device
        else:
            raise RuntimeError('Could not create device.')

    def create_command_pool(self):
        pass

    def __init__(self):
        self.instance = None
        self.device = None
        self.window = Window()

        self.create_instance()
        self.create_device()
        self.swapchain = Swapchain(self)

        self.window.show()

    def __del__(self):
        if self.instance is None:
            return # If initialization failed, there is nothing to free

        if self.device is not None:
            self.DestroyDevice(self.device, vk.NULL)

        self.DestroyInstance(self.instance, vk.NULL)
        print("Application freed!")

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