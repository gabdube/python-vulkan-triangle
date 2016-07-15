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
    from win32 import Win32Window as Window, WinSwapchain as BaseSwapchain
elif system_name == 'Linux':
    from xlib import XlibWindow as Window, XlibSwapchain as BaseSwapchain
else:
    raise OSError("Platform not supported")

class Swapchain(BaseSwapchain):

    def __init__(self, app):
        # Circular dependency is ok because its a demo. Otherwise I would have used weakref
        self.app = app
        self.swapchain = None
        self.images = None

        super().__init__()

    def create(self):
        app = self.app
        
        # Get the physical device surface capabilities (properties and format)
        cap = vk.SurfaceCapabilitiesKHR()
        result = app.GetPhysicalDeviceSurfaceCapabilitiesKHR(app.gpu, self.surface, byref(cap))
        if result != vk.SUCCESS:
            raise RuntimeError('Failed to get surface capabilities')

        # Get the available present mode
        prez_count = c_uint(0)
        result = app.GetPhysicalDeviceSurfacePresentModesKHR(app.gpu, self.surface, byref(prez_count), cast(vk.NULL, POINTER(c_uint)))
        if result != vk.SUCCESS and prez_count.value > 0:
            raise RuntimeError('Failed to get surface presenting mode')
        
        prez = (c_uint*prez_count.value)()
        app.GetPhysicalDeviceSurfacePresentModesKHR(app.gpu, self.surface, byref(prez_count), cast(prez, POINTER(c_uint)) )

        if cap.current_extent.width == -1:
            # If the surface size is undefined, the size is set to the size of the images requested
            width, height = app.window.dimensions()
            swapchain_extent = vk.Extent2D(width=width, height=height)
        else:
            # If the surface size is defined, the swap chain size must match
            # The client most likely uses windowed mode
            swapchain_extent = cap.current_extent
            width = swapchain_extent.width
            height = swapchain_extent.height

        # Prefer mailbox mode if present, it's the lowest latency non-tearing present  mode
        present_mode = vk.PRESENT_MODE_FIFO_KHR
        if vk.PRESENT_MODE_MAILBOX_KHR in prez:
            present_mode = vk.PRESENT_MODE_MAILBOX_KHR
        elif vk.PRESENT_MODE_IMMEDIATE_KHR in prez:
            present_mode = vk.PRESENT_MODE_IMMEDIATE_KHR

        # Get the number of images
        swapchain_image_count = cap.min_image_count + 1
        if cap.max_image_count > 0 and swapchain_image_count > cap.max_image_count:
            swapchain_image_count = cap.max_image_count

        # Default image transformation (use identity if supported)
        transform = cap.current_transform
        if cap.supported_transforms & vk.SURFACE_TRANSFORM_IDENTITY_BIT_KHR != 0:
            transform = vk.SURFACE_TRANSFORM_IDENTITY_BIT_KHR

        # Get the supported image format
        format_count = c_uint(0)
        result = app.GetPhysicalDeviceSurfaceFormatsKHR(app.gpu, self.surface, byref(format_count), cast(vk.NULL, POINTER(vk.SurfaceFormatKHR)))
        if result != vk.SUCCESS and format_count.value > 0:
            raise RuntimeError('Failed to get surface available image format')

        formats = (vk.SurfaceFormatKHR*format_count.value)()
        app.GetPhysicalDeviceSurfaceFormatsKHR(app.gpu, self.surface, byref(format_count), cast(formats, POINTER(vk.SurfaceFormatKHR)))

        # If the surface format list only includes one entry with VK_FORMAT_UNDEFINED,
		# there is no preferered format, so we assume VK_FORMAT_B8G8R8A8_UNORM
        if format_count == 1 and formats[0].format == vk.FORMAT_UNDEFINED:
            color_format = vk.FORMAT_B8G8R8A8_UNORM
        else:
            # Else select the first format
            color_format = formats[0].format

        color_space = formats[0].color_space

        #Create the swapchain
        create_info = vk.SwapchainCreateInfoKHR(
            s_type=vk.STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR, next=vk.NULL, 
            flags=0, surface=self.surface, min_image_count=swapchain_image_count,
            image_format=color_format, image_color_space=color_space, 
            image_extent=swapchain_extent, image_array_layers=1, image_usage=vk.IMAGE_USAGE_COLOR_ATTACHMENT_BIT,
            image_sharing_mode=vk.SHARING_MODE_EXCLUSIVE, queue_family_index_count=0,
            queue_family_indices=cast(vk.NULL, POINTER(c_uint)), pre_transform=transform, 
            composite_alpha=vk.COMPOSITE_ALPHA_OPAQUE_BIT_KHR, present_mode=present_mode,
            clipped=1, old_swapchain=vk.SwapchainKHR(0)
        )

        swapchain = vk.SwapchainKHR(0)
        result = app.CreateSwapchainKHR(app.device, byref(create_info), vk.NULL, byref(swapchain))
        if result == vk.SUCCESS:
            self.swapchain = swapchain
            self.images = (vk.Image * swapchain_image_count )()
            self.create_images()
        else:
            raise RuntimeError('Failed to create the swapchain')
        
    def create_images(self):
        pass


    def destroy_swapchain(self):
        app = self.app
        app.DestroySwapchainKHR(app.device, self.swapchain, vk.NULL)

    def destroy(self):
        app = self.app
        self.destroy_swapchain()
        app.DestroySurfaceKHR(app.instance, self.surface, NULL)
        


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

        # Find a graphic queue that supports graphic operation and presentation into
        # the surface previously created
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

        surface = self.swapchain.surface
        supported = vk.c_uint(0)
        for index, queue in enumerate(queue_families):
            self.GetPhysicalDeviceSurfaceSupportKHR(self.gpu, index, surface, byref(supported))
            if queue.queue_flags & vk.QUEUE_GRAPHICS_BIT != 0 and supported.value == 1:
                self.main_queue_family = index
                break

        if self.main_queue_family is None:
            raise OSError("Could not find a queue that supports graphics and presenting")

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

    def create_swapchain(self):
        self.swapchain = Swapchain(self)

    def create_command_pool(self):
        create_info = vk.CommandPoolCreateInfo(
            s_type=vk.STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO, next= vk.NULL,
            flags=vk.COMMAND_POOL_RESET_RELEASE_RESOURCES_BIT,
            queue_family_index=self.main_queue_family
        )

        pool = vk.CommandPool(0)
        result = self.CreateCommandPool(self.device, byref(create_info), vk.NULL, byref(pool))
        if result == vk.SUCCESS:
            self.cmd_pool = pool
        else:
            raise RuntimeError('Could not create command pool')

    def create_setup_buffer(self):
        create_info = vk.CommandBufferAllocateInfo(
            s_type=vk.STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO,
            next=vk.NULL, command_pool=self.cmd_pool, level=vk.COMMAND_BUFFER_LEVEL_PRIMARY,
            command_buffer_count=1
        )
        begin_info = vk.CommandBufferBeginInfo(
            s_type=vk.STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO,
            next=vk.NULL, flags= 0, inheritance_info=vk.NULL
        )

        buffer = vk.CommandBuffer(0)
        result = self.AllocateCommandBuffers(self.device, byref(create_info), byref(buffer))
        if result == vk.SUCCESS:
            self.setup_buffer = buffer
        else:
            raise RuntimeError('Failed to create setup buffer')

        if self.BeginCommandBuffer(buffer, byref(begin_info)) != vk.SUCCESS:
            raise RuntimeError('Failed to start recording in the setup buffer')

    def flush_setup_buffer(self):
        if self.EndCommandBuffer(self.setup_buffer) != vk.SUCCESS:
            raise RuntimeError('Failed to end setup command buffer')

    def __init__(self):
        self.gpu = None
        self.instance = None
        self.device = None
        self.swapchain = None
        self.cmd_pool = None
        self.setup_buffer = None
        self.window = Window()

        self.create_instance()
        self.create_swapchain()
        self.create_device()
        self.create_command_pool()

        self.create_setup_buffer()
        self.swapchain.create()
        self.flush_setup_buffer()

        self.window.show()

    def __del__(self):
        if self.instance is None:
            return

        if self.swapchain is not None:
            self.swapchain.destroy()

        if self.setup_buffer != None:
            self.vkFreeCommandBuffers(self.device, self.cmd_pool, 1, byref(self.setup_buffer))

        if self.cmd_pool:
            self.DestroyCommandPool(self.device, self.cmd_pool, vk.NULL)

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