"""
    Minimalistic vulkan triangle example powered by asyncio. The demo
    was tested and should run on Windows and Linux. 
    For more information see the readme of the project

    To run this demo call:  
    ``python triangle.py``

    @author: Gabriel Dubé
"""

import platform, asyncio, vk
from ctypes import cast, c_char_p, c_uint, pointer, POINTER, byref, c_float, Structure
from xmath import *

system_name = platform.system()
if system_name == 'Windows':
    from win32 import Win32Window as Window, WinSwapchain as BaseSwapchain
elif system_name == 'Linux':
    from xlib import XlibWindow as Window, XlibSwapchain as BaseSwapchain
else:
    raise OSError("Platform not supported")

class Vertex(Structure):
    _fields_ = (('pos', c_float*3), ('col', c_float*3))



class Swapchain(BaseSwapchain):

    def __init__(self, app):
        super().__init__(app)

    def create(self):
        app = self.app()

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

        app.formats['color'] = color_format
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
            if self.swapchain is not None: #Destroy the old swapchain if it exists
                self.destroy_swapchain()
            self.swapchain = swapchain
            self.create_images(swapchain_image_count, color_format)
        else:
            raise RuntimeError('Failed to create the swapchain')
        
    def create_images(self, image_count, color_format):
        self.images = (vk.Image * image_count)()
        self.views = (vk.ImageView * image_count)()
        app = self.app()

        image_count = c_uint(image_count)
        result = app.GetSwapchainImagesKHR(app.device, self.swapchain, byref(image_count), cast(self.images, POINTER(c_uint)))
        if result != vk.SUCCESS:
            raise RuntimeError('Failed to get the swapchain images')

        for index, image in enumerate(self.images):

            components = vk.ComponentMapping(
                r=vk.COMPONENT_SWIZZLE_R, g=vk.COMPONENT_SWIZZLE_G,
                b=vk.COMPONENT_SWIZZLE_B, a=vk.COMPONENT_SWIZZLE_A,
            )

            subresource_range = vk.ImageSubresourceRange(
                aspect_mask=vk.IMAGE_ASPECT_COLOR_BIT, base_mip_level=0,
                level_count=1, base_array_layer=1, layer_count=1,
            )

            view_create_info = vk.ImageViewCreateInfo(
                s_type=vk.STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO,
                next=vk.NULL, flags=0, image=image,
                view_type=vk.IMAGE_VIEW_TYPE_2D, format=color_format,
                components=components, subresource_range=subresource_range
            )

            app.set_image_layout(
                app.setup_buffer, image, 
                vk.IMAGE_ASPECT_COLOR_BIT,
                vk.IMAGE_LAYOUT_UNDEFINED,
                vk.IMAGE_LAYOUT_PRESENT_SRC_KHR)

            view = vk.ImageView(0)
            result = app.CreateImageView(app.device, byref(view_create_info), vk.NULL, byref(view))
            if result == vk.SUCCESS:
                self.views[index] = view
            else:
                raise RuntimeError('Failed to create an image view.')

    def destroy_swapchain(self):
        app = self.app()
        for view in self.views:
            app.DestroyImageView(app.device, view, vk.NULL)
        app.DestroySwapchainKHR(app.device, self.swapchain, vk.NULL)

    def destroy(self):
        app = self.app()
        if self.swapchain is not None:
            self.destroy_swapchain()
        app.DestroySurfaceKHR(app.instance, self.surface, vk.NULL)
        


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

        
        # Get the physical device memory properties.
        self.gpu_mem = vk.PhysicalDeviceMemoryProperties()
        self.GetPhysicalDeviceMemoryProperties(self.gpu, byref(self.gpu_mem))

        # Get the queue that was created with the device
        queue = vk.Queue(0)
        self.GetDeviceQueue(device, self.main_queue_family, 0, byref(queue))
        if queue.value != 0:
            self.queue = queue
        else:
            raise RuntimeError("Could not get device queue")

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

    def create_draw_buffers(self):
        # Create one command buffer per frame buffer
        # in the swap chain
        # Command buffers store a reference to the
        # frame buffer inside their render pass info
        # so for static usage withouth having to rebuild
        # them each frame, we use one per frame buffer
        image_count = len(self.swapchain.images)
        draw_buffers = (vk.CommandBuffer*image_count)()

        alloc_info = vk.CommandBufferAllocateInfo(
            s_type=vk.STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO,
            next=vk.NULL, command_pool=self.cmd_pool, level=vk.COMMAND_BUFFER_LEVEL_PRIMARY,
            command_buffer_count=image_count
        )

        result = self.AllocateCommandBuffers(self.device, byref(alloc_info), cast(draw_buffers, POINTER(vk.CommandBuffer)))
        if result == vk.SUCCESS:
            self.draw_buffers = draw_buffers
        else:
            raise RuntimeError('Failed to drawing buffers')

        # Command buffers for submitting present barriers
        alloc_info.command_buffer_count = 2
        present_buffers = (vk.CommandBuffer*2)()

        result = self.AllocateCommandBuffers(self.device, byref(alloc_info), cast(present_buffers, POINTER(vk.CommandBuffer)))
        if result == vk.SUCCESS:
            self.present_buffers = present_buffers
        else:
            raise RuntimeError('Failed to present buffers')
    
    def create_depth_stencil(self):
        width, height = self.window.dimensions()

        # Find a supported depth format
        depth_format = None
        depth_formats = (
            vk.FORMAT_D32_SFLOAT_S8_UINT,
            vk.FORMAT_D32_SFLOAT,
            vk.FORMAT_D24_UNORM_S8_UINT,
            vk.FORMAT_D16_UNORM_S8_UINT,
            vk.FORMAT_D16_UNORM,
        )

        format_props = vk.FormatProperties()
        for format in depth_formats:
            self.GetPhysicalDeviceFormatProperties(self.gpu, format, byref(format_props));
            if format_props.optimal_tiling_features & vk.FORMAT_FEATURE_DEPTH_STENCIL_ATTACHMENT_BIT != 0:
                depth_format = format
                break

        if depth_format is None:
            raise RuntimeError('Could not find a valid depth format')

        create_info = vk.ImageCreateInfo(
            s_type=vk.STRUCTURE_TYPE_IMAGE_CREATE_INFO, next=vk.NULL, flags=0,
            image_type=vk.IMAGE_TYPE_2D, format=depth_format,
            extent=vk.Extent3D(width, height, 1), mip_levels=1,
            array_layers=1, samples=vk.SAMPLE_COUNT_1_BIT, tiling=vk.IMAGE_TILING_OPTIMAL,
            usage=vk.IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT | vk.IMAGE_USAGE_TRANSFER_SRC_BIT,
        )

        subres_range = vk.ImageSubresourceRange(
            aspect_mask=vk.IMAGE_ASPECT_DEPTH_BIT, base_mip_level=0,
            level_count=1, base_array_layer=1, layer_count=1,
        )

        create_view_info = vk.ImageViewCreateInfo(
            s_type=vk.STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO, next=vk.NULL,
            flags=0, view_type=vk.IMAGE_VIEW_TYPE_2D, format=depth_format,
            subresource_range=subres_range
        )

        mem_alloc_info = vk.MemoryAllocateInfo(
            s_type=vk.STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO, next=vk.NULL,
            allocation_size=0, memory_type_index=0
        )

        depthstencil_image = vk.Image(0)
        result=self.CreateImage(self.device, byref(create_info), vk.NULL, byref(depthstencil_image))
        if result != vk.SUCCESS:
            raise RuntimeError('Failed to create depth stencil image')

        memreq = vk.MemoryRequirements()
        self.GetImageMemoryRequirements(self.device, depthstencil_image, byref(memreq))
        mem_alloc_info.allocation_size = memreq.size
        mem_alloc_info.memory_type_index = self.get_memory_type(memreq.memory_type_bits, vk.MEMORY_PROPERTY_DEVICE_LOCAL_BIT)[1]
        
        depthstencil_mem = vk.DeviceMemory(0)
        result = self.AllocateMemory(self.device, byref(mem_alloc_info), vk.NULL, byref(depthstencil_mem))
        if result != vk.SUCCESS:
            raise RuntimeError('Could not allocate depth stencil image memory')

        result = self.BindImageMemory(self.device, depthstencil_image, depthstencil_mem, 0)
        if result != vk.SUCCESS:
            raise RuntimeError('Could not bind the depth stencil memory to the image')
            
        self.set_image_layout(
            self.setup_buffer, depthstencil_image,
            vk.IMAGE_ASPECT_DEPTH_BIT | vk.IMAGE_ASPECT_STENCIL_BIT,
            vk.IMAGE_LAYOUT_UNDEFINED,
            vk.IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL
        )

        depthstencil_view = vk.ImageView(0)
        create_view_info.image = depthstencil_image
        result = self.CreateImageView(self.device, byref(create_view_info), vk.NULL, byref(depthstencil_view))
        if result != vk.SUCCESS:
            raise RuntimeError('Could not create image view for depth stencil')
            
        
        self.formats['depth'] = depth_format
        self.depth_stencil['image'] = depthstencil_image
        self.depth_stencil['mem'] = depthstencil_mem
        self.depth_stencil['view'] = depthstencil_view

    def create_renderpass(self):
        attachments = (vk.AttachmentDescription*2)()
        color, depth = attachments

        #Color attachment
        color.format = self.formats['color']
        color.samples = vk.SAMPLE_COUNT_1_BIT
        color.load_op = vk.ATTACHMENT_LOAD_OP_CLEAR
        color.store_op = vk.ATTACHMENT_STORE_OP_STORE
        color.stencil_load_op = vk.ATTACHMENT_LOAD_OP_DONT_CARE
        color.stencil_store_op = vk.ATTACHMENT_STORE_OP_DONT_CARE
        color.initial_layout = vk.IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL
        color.final_layout = vk.IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL

        #Depth attachment
        depth.format = self.formats['depth']
        depth.samples = vk.SAMPLE_COUNT_1_BIT
        depth.load_op = vk.ATTACHMENT_LOAD_OP_CLEAR
        depth.store_op = vk.ATTACHMENT_STORE_OP_STORE
        depth.stencil_load_op = vk.ATTACHMENT_LOAD_OP_DONT_CARE
        depth.stencil_store_op = vk.ATTACHMENT_STORE_OP_DONT_CARE
        depth.initial_layout = vk.IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL
        depth.final_layout = vk.IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL

        color_ref = vk.AttachmentReference( attachment=0, layout=vk.IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL )
        depth_ref = vk.AttachmentReference( attachment=1, layout=vk.IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL )

        subpass = vk.SubpassDescription(
            pipeline_bind_point = vk.PIPELINE_BIND_POINT_GRAPHICS,
            flags = 0, input_attachment_count=0, input_attachments=vk.NULL_REF,
            color_attachment_count=1, color_attachments=pointer(color_ref),
            resolve_attachments=vk.NULL_REF, depth_stencil_attachment=pointer(depth_ref),
            preserve_attachment_count=0, preserve_attachments=cast(vk.NULL, POINTER(c_uint))
        )

        create_info = vk.RenderPassCreateInfo(
            s_type=vk.STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO,
            next=vk.NULL, attachment_count=2,
            attachments=cast(attachments, POINTER(vk.AttachmentDescription)),
            subpass_count=1, subpasses=pointer(subpass), dependency_count=0,
            dependencies=vk.NULL
        )

        renderpass = vk.RenderPass(0)
        result = self.CreateRenderPass(self.device, byref(create_info), vk.NULL, byref(renderpass))
        if result != vk.SUCCESS:
            raise RuntimeError('Could not create renderpass')

        self.renderpass = renderpass

    def create_pipeline_cache(self):
        create_info = vk.PipelineCacheCreateInfo(
            s_type=vk.STRUCTURE_TYPE_PIPELINE_CACHE_CREATE_INFO, next=vk.NULL,
            flags=0, initial_data_size=0, initial_data=vk.NULL
        )

        pipeline_cache = vk.PipelineCache(0)
        result = self.CreatePipelineCache(self.device, byref(create_info), vk.NULL, byref(pipeline_cache))
        if result != vk.SUCCESS:
            raise RuntimeError('Failed to create pipeline cache')

        self.pipeline_cache = pipeline_cache

    def create_framebuffer(self):
        attachments = (vk.ImageView*2)()
        attachments[1] = self.depth_stencil['image']

        width, height = self.window.dimensions()

        create_info = vk.FramebufferCreateInfo(
            s_type=vk.STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO,
            next=vk.NULL, flags=0, render_pass=self.renderpass,
            attachment_count=2, attachments=cast(attachments, POINTER(vk.ImageView)),
            width=width, height=height, layers=1
        )

        self.framebuffers = (vk.Framebuffer*len(self.swapchain.images))()
        for index, view in enumerate(self.swapchain.images):
            fb = vk.Framebuffer(0)
            attachments[0] = view
            result = self.CreateFramebuffer(self.device, byref(create_info), vk.NULL, byref(fb))
            if result != vk.SUCCESS:
                raise RuntimeError('Could not create the framebuffers')
            
            

    def flush_setup_buffer(self):
        if self.EndCommandBuffer(self.setup_buffer) != vk.SUCCESS:
            raise RuntimeError('Failed to end setup command buffer')

        submit_info = vk.SubmitInfo(
            s_type=vk.STRUCTURE_TYPE_SUBMIT_INFO, next=vk.NULL,
            wait_semaphore_count=0, wait_semaphores=vk.NULL_HANDLE_PTR,
            wait_dst_stage_mask=vk.NULL_CUINT_PTR, command_buffer_count=1,
            command_buffers=pointer(self.setup_buffer),
            signal_semaphore_count=0, signal_semaphores=vk.NULL_HANDLE_PTR,
        )

        result = self.QueueSubmit(self.queue, 1, byref(submit_info), 0)
        if result != vk.SUCCESS:
            raise RuntimeError("Setup buffer sumbit failed")
        
        result = self.QueueWaitIdle(self.queue)
        if result != vk.SUCCESS:
            raise RuntimeError("Setup execution failed")

        self.FreeCommandBuffers(self.device, self.cmd_pool, 1, byref(self.setup_buffer))
        self.setup_buffer = None

    def set_image_layout(self, cmd, image, aspect_mask, old_layout, new_layout, subres=None):
        
        if subres is None:
            subres = vk.ImageSubresourceRange(
                aspect_mask=aspect_mask, base_mip_level=0,
                level_count=1, base_array_layer=1, layer_count=1,
            )

        barrier = vk.ImageMemoryBarrier(
            s_type=vk.STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER, next=vk.NULL, 
            old_layout=old_layout, new_layout=new_layout,
            src_queue_family_index=vk.QUEUE_FAMILY_IGNORED,
            dst_queue_family_index=vk.QUEUE_FAMILY_IGNORED,
            image=image, subresource_range=subres
        )

        # Source layouts mapping (old)
        old_map = {
            vk.IMAGE_LAYOUT_PREINITIALIZED: vk.ACCESS_HOST_WRITE_BIT | vk.ACCESS_TRANSFER_WRITE_BIT,
            vk.IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL: vk.ACCESS_DEPTH_STENCIL_ATTACHMENT_WRITE_BIT,
            vk.IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL: vk.ACCESS_TRANSFER_READ_BIT,
            vk.IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL: vk.ACCESS_SHADER_READ_BIT
        }
        if old_layout in old_map.values():
            barrier.src_access_mask = old_map[old_layout]
        else:
            barrier.src_access_mask = 0

        # Target layouts
        if new_layout == vk.IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL:
            barrier.dst_access_mask = vk.ACCESS_TRANSFER_WRITE_BIT

        elif new_layout == vk.IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL:
            barrier.src_access_mask |= vk.ACCESS_TRANSFER_READ_BIT
            barrier.dst_access_mask = vk.ACCESS_TRANSFER_READ_BIT

        elif new_layout == vk.IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL:
            barrier.dst_access_mask = vk.ACCESS_COLOR_ATTACHMENT_WRITE_BIT
            barrier.src_access_mask = vk.ACCESS_TRANSFER_READ_BIT

        elif new_layout == vk.IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL:
            barrier.dst_access_mask |= vk.ACCESS_DEPTH_STENCIL_ATTACHMENT_WRITE_BIT
        
        elif new_layout == vk.IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL:
            barrier.src_access_mask = vk.ACCESS_HOST_WRITE_BIT | vk.ACCESS_TRANSFER_WRITE_BIT
            barrier.dst_access_mask = vk.ACCESS_SHADER_READ_BIT

        self.CmdPipelineBarrier(
            cmd,
            vk.PIPELINE_STAGE_TOP_OF_PIPE_BIT,
            vk.PIPELINE_STAGE_TOP_OF_PIPE_BIT,
            0,
            0,vk.NULL,
            0,vk.NULL,
            1, byref(barrier)
        )

    def get_memory_type(self, bits, properties):
        for index, mem_t in enumerate(self.gpu_mem.memory_types):
            if (bits & 1) == 1:
                if mem_t.property_flags & properties == properties:
                    return (True, index)
            bits >>= 1

        return (False, None)

    def __init__(self):
        self.zoom = 0.0
        self.rotation = (c_float*3)()

        self.gpu = None
        self.gpu_mem = None
        self.instance = None
        self.device = None
        self.queue = None
        self.swapchain = None
        self.cmd_pool = None
        self.setup_buffer = None
        self.draw_buffers = None
        self.present_buffers = None
        self.renderpass = None
        self.pipeline_cache = None
        self.framebuffers = None
        self.depth_stencil = {'image':None, 'mem':None, 'view':None}
        self.formats = {'color':None, 'depth':None}
        self.window = Window()

        self.create_instance()
        self.create_swapchain()
        self.create_device()
        self.create_command_pool()

        self.create_setup_buffer()
        self.swapchain.create()
        self.create_draw_buffers()
        self.create_depth_stencil()
        self.create_renderpass()
        self.create_pipeline_cache()
        self.create_framebuffer()
        self.flush_setup_buffer()

        self.window.show()

    def __del__(self):
        if self.instance is None:
            return

        dev = self.device
        if dev is not None:
            if self.swapchain is not None:
                self.swapchain.destroy()

            if self.setup_buffer is not None:
                self.FreeCommandBuffers(dev, self.cmd_pool, 1, byref(self.setup_buffer))

            if self.present_buffers is not None:
                len_draw_buffers = len(self.draw_buffers)
                self.FreeCommandBuffers(dev, self.cmd_pool, len_draw_buffers, cast(self.draw_buffers, POINTER(vk.CommandBuffer)))
                self.FreeCommandBuffers(dev, self.cmd_pool, 2, cast(self.present_buffers, POINTER(vk.CommandBuffer)))

            if self.renderpass is not None:
                self.DestroyRenderPass(self.device, self.renderpass, vk.NULL)
            
            if self.framebuffers is not None:
                for fb in self.framebuffers:
                    self.DestroyFramebuffer(self.device, fb, vk.NULL)

            if self.depth_stencil['view'] is not None:
                self.DestroyImageView(dev, self.depth_stencil['view'], vk.NULL)

            if self.depth_stencil['image'] is not None:
                self.DestroyImage(dev, self.depth_stencil['image'], vk.NULL)

            if self.depth_stencil['mem'] is not None:
                self.FreeMemory(dev, self.depth_stencil['mem'], vk.NULL)
            
            if self.pipeline_cache:
                self.DestroyPipelineCache(self.device, self.pipeline_cache, vk.NULL)

            if self.cmd_pool:
                self.DestroyCommandPool(dev, self.cmd_pool, vk.NULL)

        
            self.DestroyDevice(dev, vk.NULL)

        self.DestroyInstance(self.instance, vk.NULL)
        print('Application freed!')


class TriangleApplication(Application):

    def create_semaphores(self):
        create_info = vk.SemaphoreCreateInfo(
            s_type=vk.STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO,
            next=vk.NULL, flags=0
        )

        present = vk.Semaphore(0)
        render = vk.Semaphore(0)

        result1 = self.CreateSemaphore(self.device, byref(create_info), vk.NULL, byref(present))
        result2 = self.CreateSemaphore(self.device, byref(create_info), vk.NULL, byref(render))
        if vk.SUCCESS not in (result1, result2):
            raise RuntimeError('Failed to create the semaphores')

        self.render_semaphores['present'] = present
        self.render_semaphores['render'] = render

    def describe_bindings(self):
        bindings = (vk.VertexInputBindingDescription*1)()
        attributes = (vk.VertexInputAttributeDescription*2)()

        bindings[0].binding = 0
        bindings[0].stride = vk.sizeof(Vertex)
        bindings[0].input_rate = vk.VERTEX_INPUT_RATE_VERTEX

        # Attribute descriptions
		# Describes memory layout and shader attribute locations

        # Location 0: Position
        attributes[0].binding = 0
        attributes[0].location = 0
        attributes[0].format = vk.FORMAT_R32G32B32_SFLOAT
        attributes[0].offset = 0

        # Location 1: Color
        attributes[1].binding = 0
        attributes[1].location = 1
        attributes[1].format = vk.FORMAT_R32G32B32_SFLOAT
        attributes[1].offset = vk.sizeof(c_float)*3

        self.triangle['bindings'] = bindings
        self.triangle['attributes'] = attributes

    def create_triangle(self):
        data = vk.c_void_p(0)
        memreq = vk.MemoryRequirements()
        memalloc = vk.MemoryAllocateInfo(
            s_type=vk.STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO, next=vk.NULL,
            allocation_size=0, memory_type_index=0
        )

        # Setup vertices
        vertices_data = (Vertex*3)(
            Vertex(pos=(1.0, 1.0, 0.0), col=(1.0, 0.0,0.0)),
            Vertex(pos=(-1.0, 1.0, 0.0), col=(0.0, 1.0,0.0)),
            Vertex(pos=(0.0, -1.0, 0.0), col=(0.0, 0.0,1.0)),
        )

        vertices_size = vk.sizeof(Vertex)*3

        # Setup indices
        indices_data = (c_uint*3)(0,1,2)
        indices_size = vk.sizeof(c_uint)*3

        #
        # Store the vertices in the device memory
        #

        # 1 Create a staging buffer
        vertex = {'buffer': vk.Buffer(0), 'memory': vk.DeviceMemory(0)}
        indices = {'buffer': vk.Buffer(0), 'memory': vk.DeviceMemory(0)}

        # 2 Create the vertex buffer
        vertex_info = vk.BufferCreateInfo(
            s_type=vk.STRUCTURE_TYPE_BUFFER_CREATE_INFO, next=vk.NULL,
            flags=0, size=vertices_size, usage=vk.BUFFER_USAGE_TRANSFER_SRC_BIT,
            sharing_mode=0, queue_family_index_count=0, queue_family_indices=vk.NULL_CUINT_PTR
        )

        result = self.CreateBuffer(self.device, byref(vertex_info), vk.NULL, byref(vertex['buffer']))
        if result != vk.SUCCESS:
            raise 'Could not create a buffer'

        # 3 Allocate memory for the vertex buffer
        self.GetBufferMemoryRequirements(self.device, vertex['buffer'], byref(memreq))
        memalloc.allocation_size = memreq.size
        memalloc.memory_type_index = self.get_memory_type(memreq.memory_type_bits, vk.MEMORY_PROPERTY_HOST_VISIBLE_BIT)[1]
        result = self.AllocateMemory(self.device, byref(memalloc), vk.NULL, byref(vertex['memory']))
        if result != vk.SUCCESS:
            raise 'Could not allocate buffer memory'

        # 4  Map the buffer memory and write the data
        result = self.MapMemory(self.device, vertex['memory'], 0, memalloc.allocation_size, 0, byref(data))
        if result != vk.SUCCESS:
            raise 'Could not map memory to local'
        vk.memmove(vertices_data, data, vertices_size)
        self.UnmapMemory(self.device, vertex['memory'])

        # 5 Bind the memory and the buffer together
        result = self.BindBufferMemory(self.device, vertex['buffer'], vertex['memory'], 0)
        if result != vk.SUCCESS:
            raise 'Could not bind buffer memory'

        # 6 Create a destination buffer with device only visibility and allocate its memory
        vertex_info.usage = vk.BUFFER_USAGE_VERTEX_BUFFER_BIT | vk.BUFFER_USAGE_TRANSFER_DST_BIT
        result = self.CreateBuffer(self.device, byref(vertex_info), vk.NULL, byref(self.triangle['buffer']))
        if result != vk.SUCCESS:
            raise 'Could not create triangle buffer'

        # 7 Allocate the buffer memory and bind the allocated memory to the buffer
        self.GetBufferMemoryRequirements(self.device, self.triangle['buffer'], byref(memreq))
        memalloc.allocation_size = memreq.size
        memalloc.memory_type_index = self.get_memory_type(memreq.memory_type_bits, vk.MEMORY_PROPERTY_DEVICE_LOCAL_BIT)[1]
        result = self.AllocateMemory(self.device, byref(memalloc), vk.NULL, self.triangle['memory'])
        if result != vk.SUCCESS:
            raise 'Could not allocate the triangle memory'
        result = self.BindBufferMemory(self.device, self.triangle['buffer'], self.triangle['memory'], 0)
        if result != vk.SUCCESS:
            raise 'Could not bind the triangle memory'

        #
        # Store the indices in the device memory
        #

        # Same steps as 1,2,3,4,5
        indices_info = vertex_info
        indices_info.size = indices_size
        indices_info.usage = vk.BUFFER_USAGE_TRANSFER_SRC_BIT

        assert(self.CreateBuffer(self.device, byref(indices_info), vk.NULL, byref(indices['buffer'])) == vk.SUCCESS)
        self.GetBufferMemoryRequirements(self.device, indices['buffer'], byref(memreq))
        memalloc.allocation_size = memreq.size
        memalloc.memory_type_index = self.get_memory_type(memreq.memory_type_bits, vk.MEMORY_PROPERTY_HOST_VISIBLE_BIT)[1]
        assert(self.AllocateMemory(self.device, byref(memalloc), vk.NULL, byref(indices['memory'])) == vk.SUCCESS)
        assert(self.MapMemory(self.device, indices['memory'], 0, indices_size, 0, byref(data)) == vk.SUCCESS)
        vk.memmove(vertices_data, data, vertices_size)
        self.UnmapMemory(self.device, vertex['memory'])
        assert(self.BindBufferMemory(self.device, indices['buffer'], indices['memory'], 0) == vk.SUCCESS)
        
        # Same steps as 5, 7 (with the exception for the usage flags)
        indices_info.usage =  vk.BUFFER_USAGE_INDEX_BUFFER_BIT | vk.BUFFER_USAGE_TRANSFER_DST_BIT
        assert(self.CreateBuffer(self.device, byref(indices_info), vk.NULL, self.triangle['indices_buffer']) == vk.SUCCESS)
        self.GetBufferMemoryRequirements(self.device, self.triangle['indices_buffer'], byref(memreq))
        memalloc.allocation_size = memreq.size
        memalloc.memory_type_index = self.get_memory_type(memreq.memory_type_bits, vk.MEMORY_PROPERTY_DEVICE_LOCAL_BIT)[1]
        assert(self.AllocateMemory(self.device, byref(memalloc), vk.NULL, byref(self.triangle['indices_memory']))==vk.SUCCESS)
        assert(self.BindBufferMemory(self.device, self.triangle['indices_buffer'], self.triangle['indices_memory'], 0) ==vk.SUCCESS)
       
        # Copy the staging buffer memory into the final buffers
        cmd_info = vk.CommandBufferAllocateInfo(
            s_type = vk.STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO,
            command_pool=self.cmd_pool,
            level=vk.COMMAND_BUFFER_LEVEL_PRIMARY,
            command_buffer_count=1
        )
        begin_info = vk.CommandBufferBeginInfo(
            s_type=vk.STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO, next=vk.NULL,
            flags=0, inheritance_info=vk.NULL
        )
        copy_region = vk.BufferCopy(src_offset=0, dst_offset=0, size=0)
        copy_command = vk.CommandBuffer(0)

        assert(self.AllocateCommandBuffers(self.device, byref(cmd_info), byref(copy_command)) == vk.SUCCESS)
        assert(self.BeginCommandBuffer(copy_command, byref(begin_info)) == vk.SUCCESS)
        
        #Vertex Buffer
        copy_region.size = vertices_size
        self.CmdCopyBuffer(
            copy_command, vertex['buffer'],
            self.triangle['buffer'],
            1,
            byref(copy_region)
        )

        #Index Buffer
        copy_region.size = indices_size
        self.CmdCopyBuffer(
            copy_command, indices['buffer'],
            self.triangle['indices_buffer'],
            1,
            byref(copy_region)
        )

        assert(self.EndCommandBuffer(copy_command) == vk.SUCCESS)

        # Submit commands to the queue
        submit_info = vk.SubmitInfo(
            s_type=vk.STRUCTURE_TYPE_SUBMIT_INFO, next=vk.NULL,
            wait_semaphore_count=0, wait_semaphores=vk.NULL_HANDLE_PTR,
            wait_dst_stage_mask=vk.NULL_CUINT_PTR, command_buffer_count=1,
            command_buffers=pointer(copy_command),
            signal_semaphore_count=0, signal_semaphores=vk.NULL_HANDLE_PTR,
        )

        assert(self.QueueSubmit(self.queue, 1, byref(submit_info), 0)==vk.SUCCESS)
        assert(self.QueueWaitIdle(self.queue)==vk.SUCCESS)

        # Free temporary ressources
        self.FreeCommandBuffers(self.device, self.cmd_pool, 1, byref(copy_command))

        self.DestroyBuffer(self.device, vertex['buffer'], vk.NULL)
        self.FreeMemory(self.device, vertex['memory'], vk.NULL)

        self.DestroyBuffer(self.device, indices['buffer'], vk.NULL)
        self.FreeMemory(self.device, indices['memory'], vk.NULL)

        self.describe_bindings()

    def create_uniform_buffers(self):
        memreq = vk.MemoryRequirements()

        # Vertex shader uniform buffer block
        buffer_info = vk.BufferCreateInfo(
            s_type=vk.STRUCTURE_TYPE_BUFFER_CREATE_INFO, next=vk.NULL,
            flags=0, size=vk.sizeof(Mat4)*3, usage=vk.BUFFER_USAGE_UNIFORM_BUFFER_BIT,
            sharing_mode=0, queue_family_index_count=0, queue_family_indices=vk.NULL_CUINT_PTR
        )

        alloc_info = vk.MemoryAllocateInfo(
            s_type=vk.STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO, next=vk.NULL,
            allocation_size=0, memory_type_index=0
        )

        result = self.CreateBuffer(self.device, byref(buffer_info), vk.NULL, self.uniform_data['buffer'])
        if result != vk.SUCCESS:
            raise RuntimeError('Could not create the uniform buffer')

        self.GetBufferMemoryRequirements(self.device, self.uniform_data['buffer'], byref(memreq))
        alloc_info.allocation_size = memreq.size
        alloc_info.memory_type_index = self.get_memory_type(memreq.memory_type_bits, vk.MEMORY_PROPERTY_HOST_VISIBLE_BIT)[1]

        result = self.AllocateMemory(self.device, byref(alloc_info), vk.NULL, byref(self.uniform_data['memory']))
        if result != vk.SUCCESS:
            raise RuntimeError('Failed to allocate the uniform buffer memory')

        result = self.BindBufferMemory(self.device, self.uniform_data['buffer'], self.uniform_data['memory'], 0)
        if result != vk.SUCCESS:
            raise RuntimeError('Failed to bind the uniform buffer memory')

        # Store information in the uniform's descriptor
        self.uniform_data['descriptor'].buffer = self.uniform_data['buffer']
        self.uniform_data['descriptor'].offset = 0
        self.uniform_data['descriptor'].range = vk.sizeof(self.matrices)

        self.update_uniform_buffers()

    def update_uniform_buffers(self):
        data = vk.c_void_p(0)
        matsize = vk.sizeof(Mat4)*3

        # Projection 
        width, height = self.window.dimensions()
        self.matrices[0].set_data(perspective(60.0, width/height, 0.1, 256.0))

        # View
        self.matrices[1].set_data(translate(None, (0.0, 0.0, self.zoom)))

        # Model
        mod_mat = rotate(None, self.rotation[0], (1.0, 0.0, 0.0))
        mod_mat = rotate(mod_mat, self.rotation[1], (0.0, 1.0, 0.0))
        self.matrices[2].set_data(rotate(mod_mat, self.rotation[2], (0.0, 0.0, 1.0)))

        self.MapMemory(self.device, self.uniform_data['memory'], 0, matsize, 0, byref(data))
        vk.memmove(self.matrices, data, matsize)
        self.UnmapMemory(self.device, self.uniform_data['memory'])
      
    def __init__(self):
        Application.__init__(self)

        self.render_semaphores = {'present': None, 'render': None}
        self.matrices = (Mat4*3)(Mat4(), Mat4(), Mat4()) # 0: Projection, 1: Model, 2: View
        self.uniform_data = {
            'buffer': vk.Buffer(0),
            'memory': vk.DeviceMemory(0),
            'descriptor': vk.DescriptorBufferInfo()
        }
        self.triangle = {
            'buffer': vk.Buffer(0),
            'memory': vk.DeviceMemory(0),
            'indices_buffer': vk.Buffer(0),
            'indices_memory': vk.DeviceMemory(0),
            'bindings': None,
            'attributes': None
        }

        self.create_semaphores()
        self.create_triangle()
        self.create_uniform_buffers()

    def __del__(self):

        if self.render_semaphores['present'] is not None:

            if self.triangle['buffer'].value != 0:
                self.DestroyBuffer(self.device, self.triangle['buffer'], vk.NULL)
                self.FreeMemory(self.device, self.triangle['memory'], vk.NULL)

            if self.triangle['indices_buffer'].value != 0:
                self.DestroyBuffer(self.device, self.triangle['indices_buffer'], vk.NULL)
                self.FreeMemory(self.device, self.triangle['indices_memory'], vk.NULL)

            if self.uniform_data['buffer'] != 0:
                self.DestroyBuffer(self.device, self.uniform_data['buffer'], vk.NULL)
                self.FreeMemory(self.device, self.uniform_data['memory'], vk.NULL)

            self.DestroySemaphore(self.device, self.render_semaphores['present'], vk.NULL)
            self.DestroySemaphore(self.device, self.render_semaphores['render'], vk.NULL)

        Application.__del__(self)

def main():
    app = TriangleApplication()

    loop = asyncio.get_event_loop()
    loop.run_forever()



if __name__ == '__main__':
    main()