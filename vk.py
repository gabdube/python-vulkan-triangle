# -*- coding: utf-8 -*-
from ctypes import (c_void_p, c_float, c_uint8, c_uint, c_uint64, c_int, c_size_t, c_char, c_char_p, cast, Structure, Union, POINTER)
from platform import system


# Sysem initialization
system_name = system()
if system_name == 'Windows':
    from ctypes import WINFUNCTYPE, windll
    FUNCTYPE = WINFUNCTYPE
    vk = windll.LoadLibrary('vulkan-1')
elif system_name == 'Linux':
    from ctypes import CFUNCTYPE, cdll
    FUNCTYPE = CFUNCTYPE
    vk = cdll.LoadLibrary('libvulkan.so.1')

# System types
HINSTANCE = c_void_p
HWND = c_void_p
xcb_connection_t = c_void_p
xcb_window_t = c_uint
xcb_visualid_t = c_uint
MirConnection = c_void_p
MirSurface = c_void_p
wl_display = c_void_p
wl_surface = c_void_p
Display = c_void_p
Window = c_uint
VisualID = c_uint
ANativeWindow = c_void_p

def MAKE_VERSION(major, minor, patch):
    return (major<<22) | (minor<<12) | patch

def define_structure(name, *args):
    return type(name, (Structure,), {'_fields_': args})

def define_union(name, *args):
    return type(name, (Union,), {'_fields_': args})

def load_functions(vk_object, functions_list, loader):
    functions = []
    for name, return_type, *args in functions_list:
        py_name = name.decode()[2::]
        fn_ptr = loader(vk_object, name)
        fn_ptr = cast(fn_ptr, c_void_p)
        if fn_ptr:
            fn = (FUNCTYPE(return_type, *args))(fn_ptr.value)
            functions.append((py_name, fn))
        elif __debug__ == True:
            print('Function {} could not be loaded. (__debug__ == True)'.format(py_name))
    return functions

API_VERSION_1_0 = MAKE_VERSION(1,0,0)


# BASETYPES

SampleMask = c_uint
Bool32 = c_uint
Flags = c_uint
DeviceSize = c_uint64


# HANDLES

Instance = c_size_t
PhysicalDevice = c_size_t
Device = c_size_t
Queue = c_size_t
CommandBuffer = c_size_t
DeviceMemory = c_uint64
CommandPool = c_uint64
Buffer = c_uint64
BufferView = c_uint64
Image = c_uint64
ImageView = c_uint64
ShaderModule = c_uint64
Pipeline = c_uint64
PipelineLayout = c_uint64
Sampler = c_uint64
DescriptorSet = c_uint64
DescriptorSetLayout = c_uint64
DescriptorPool = c_uint64
Fence = c_uint64
Semaphore = c_uint64
Event = c_uint64
QueryPool = c_uint64
Framebuffer = c_uint64
RenderPass = c_uint64
PipelineCache = c_uint64
DisplayKHR = c_uint64
DisplayModeKHR = c_uint64
SurfaceKHR = c_uint64
SwapchainKHR = c_uint64
DebugReportCallbackEXT = c_uint64


# FLAGS

FramebufferCreateFlags = c_uint
QueryPoolCreateFlags = c_uint
RenderPassCreateFlags = c_uint
SamplerCreateFlags = c_uint
PipelineLayoutCreateFlags = c_uint
PipelineCacheCreateFlags = c_uint
PipelineDepthStencilStateCreateFlags = c_uint
PipelineDynamicStateCreateFlags = c_uint
PipelineColorBlendStateCreateFlags = c_uint
PipelineMultisampleStateCreateFlags = c_uint
PipelineRasterizationStateCreateFlags = c_uint
PipelineViewportStateCreateFlags = c_uint
PipelineTessellationStateCreateFlags = c_uint
PipelineInputAssemblyStateCreateFlags = c_uint
PipelineVertexInputStateCreateFlags = c_uint
PipelineShaderStageCreateFlags = c_uint
DescriptorSetLayoutCreateFlags = c_uint
BufferViewCreateFlags = c_uint
InstanceCreateFlags = c_uint
DeviceCreateFlags = c_uint
DeviceQueueCreateFlags = c_uint
QueueFlags = c_uint
MemoryPropertyFlags = c_uint
MemoryHeapFlags = c_uint
AccessFlags = c_uint
BufferUsageFlags = c_uint
BufferCreateFlags = c_uint
ShaderStageFlags = c_uint
ImageUsageFlags = c_uint
ImageCreateFlags = c_uint
ImageViewCreateFlags = c_uint
PipelineCreateFlags = c_uint
ColorComponentFlags = c_uint
FenceCreateFlags = c_uint
SemaphoreCreateFlags = c_uint
FormatFeatureFlags = c_uint
QueryControlFlags = c_uint
QueryResultFlags = c_uint
ShaderModuleCreateFlags = c_uint
EventCreateFlags = c_uint
CommandPoolCreateFlags = c_uint
CommandPoolResetFlags = c_uint
CommandBufferResetFlags = c_uint
CommandBufferUsageFlags = c_uint
QueryPipelineStatisticFlags = c_uint
MemoryMapFlags = c_uint
ImageAspectFlags = c_uint
SparseMemoryBindFlags = c_uint
SparseImageFormatFlags = c_uint
SubpassDescriptionFlags = c_uint
PipelineStageFlags = c_uint
SampleCountFlags = c_uint
AttachmentDescriptionFlags = c_uint
StencilFaceFlags = c_uint
CullModeFlags = c_uint
DescriptorPoolCreateFlags = c_uint
DescriptorPoolResetFlags = c_uint
DependencyFlags = c_uint
CompositeAlphaFlagsKHR = c_uint
DisplayPlaneAlphaFlagsKHR = c_uint
SurfaceTransformFlagsKHR = c_uint
SwapchainCreateFlagsKHR = c_uint
DisplayModeCreateFlagsKHR = c_uint
DisplaySurfaceCreateFlagsKHR = c_uint
AndroidSurfaceCreateFlagsKHR = c_uint
MirSurfaceCreateFlagsKHR = c_uint
WaylandSurfaceCreateFlagsKHR = c_uint
Win32SurfaceCreateFlagsKHR = c_uint
XlibSurfaceCreateFlagsKHR = c_uint
XcbSurfaceCreateFlagsKHR = c_uint
DebugReportFlagsEXT = c_uint

# ENUMS

API_Constants = c_uint
MAX_PHYSICAL_DEVICE_NAME_SIZE = 256
UUID_SIZE = 16
MAX_EXTENSION_NAME_SIZE = 256
MAX_DESCRIPTION_SIZE = 256
MAX_MEMORY_TYPES = 32
MAX_MEMORY_HEAPS = 16
LOD_CLAMP_NONE = c_float(1000.0)
REMAINING_MIP_LEVELS = c_uint(~0)
REMAINING_ARRAY_LAYERS = c_uint(~0)
WHOLE_SIZE = c_uint64(~0)
ATTACHMENT_UNUSED = c_uint(~0)
TRUE = 1
FALSE = 0
QUEUE_FAMILY_IGNORED = c_uint(~0)
SUBPASS_EXTERNAL = c_uint(~0)

ImageLayout = c_uint
IMAGE_LAYOUT_UNDEFINED = 0
IMAGE_LAYOUT_GENERAL = 1
IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL = 2
IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL = 3
IMAGE_LAYOUT_DEPTH_STENCIL_READ_ONLY_OPTIMAL = 4
IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL = 5
IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL = 6
IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL = 7
IMAGE_LAYOUT_PREINITIALIZED = 8

AttachmentLoadOp = c_uint
ATTACHMENT_LOAD_OP_LOAD = 0
ATTACHMENT_LOAD_OP_CLEAR = 1
ATTACHMENT_LOAD_OP_DONT_CARE = 2

AttachmentStoreOp = c_uint
ATTACHMENT_STORE_OP_STORE = 0
ATTACHMENT_STORE_OP_DONT_CARE = 1

ImageType = c_uint
IMAGE_TYPE_1D = 0
IMAGE_TYPE_2D = 1
IMAGE_TYPE_3D = 2

ImageTiling = c_uint
IMAGE_TILING_OPTIMAL = 0
IMAGE_TILING_LINEAR = 1

ImageViewType = c_uint
IMAGE_VIEW_TYPE_1D = 0
IMAGE_VIEW_TYPE_2D = 1
IMAGE_VIEW_TYPE_3D = 2
IMAGE_VIEW_TYPE_CUBE = 3
IMAGE_VIEW_TYPE_1D_ARRAY = 4
IMAGE_VIEW_TYPE_2D_ARRAY = 5
IMAGE_VIEW_TYPE_CUBE_ARRAY = 6

CommandBufferLevel = c_uint
COMMAND_BUFFER_LEVEL_PRIMARY = 0
COMMAND_BUFFER_LEVEL_SECONDARY = 1

ComponentSwizzle = c_uint
COMPONENT_SWIZZLE_IDENTITY = 0
COMPONENT_SWIZZLE_ZERO = 1
COMPONENT_SWIZZLE_ONE = 2
COMPONENT_SWIZZLE_R = 3
COMPONENT_SWIZZLE_G = 4
COMPONENT_SWIZZLE_B = 5
COMPONENT_SWIZZLE_A = 6

DescriptorType = c_uint
DESCRIPTOR_TYPE_SAMPLER = 0
DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER = 1
DESCRIPTOR_TYPE_SAMPLED_IMAGE = 2
DESCRIPTOR_TYPE_STORAGE_IMAGE = 3
DESCRIPTOR_TYPE_UNIFORM_TEXEL_BUFFER = 4
DESCRIPTOR_TYPE_STORAGE_TEXEL_BUFFER = 5
DESCRIPTOR_TYPE_UNIFORM_BUFFER = 6
DESCRIPTOR_TYPE_STORAGE_BUFFER = 7
DESCRIPTOR_TYPE_UNIFORM_BUFFER_DYNAMIC = 8
DESCRIPTOR_TYPE_STORAGE_BUFFER_DYNAMIC = 9
DESCRIPTOR_TYPE_INPUT_ATTACHMENT = 10

QueryType = c_uint
QUERY_TYPE_OCCLUSION = 0
QUERY_TYPE_PIPELINE_STATISTICS = 1
QUERY_TYPE_TIMESTAMP = 2

BorderColor = c_uint
BORDER_COLOR_FLOAT_TRANSPARENT_BLACK = 0
BORDER_COLOR_INT_TRANSPARENT_BLACK = 1
BORDER_COLOR_FLOAT_OPAQUE_BLACK = 2
BORDER_COLOR_INT_OPAQUE_BLACK = 3
BORDER_COLOR_FLOAT_OPAQUE_WHITE = 4
BORDER_COLOR_INT_OPAQUE_WHITE = 5

PipelineBindPoint = c_uint
PIPELINE_BIND_POINT_GRAPHICS = 0
PIPELINE_BIND_POINT_COMPUTE = 1

PipelineCacheHeaderVersion = c_uint
PIPELINE_CACHE_HEADER_VERSION_ONE = 1

PrimitiveTopology = c_uint
PRIMITIVE_TOPOLOGY_POINT_LIST = 0
PRIMITIVE_TOPOLOGY_LINE_LIST = 1
PRIMITIVE_TOPOLOGY_LINE_STRIP = 2
PRIMITIVE_TOPOLOGY_TRIANGLE_LIST = 3
PRIMITIVE_TOPOLOGY_TRIANGLE_STRIP = 4
PRIMITIVE_TOPOLOGY_TRIANGLE_FAN = 5
PRIMITIVE_TOPOLOGY_LINE_LIST_WITH_ADJACENCY = 6
PRIMITIVE_TOPOLOGY_LINE_STRIP_WITH_ADJACENCY = 7
PRIMITIVE_TOPOLOGY_TRIANGLE_LIST_WITH_ADJACENCY = 8
PRIMITIVE_TOPOLOGY_TRIANGLE_STRIP_WITH_ADJACENCY = 9
PRIMITIVE_TOPOLOGY_PATCH_LIST = 10

SharingMode = c_uint
SHARING_MODE_EXCLUSIVE = 0
SHARING_MODE_CONCURRENT = 1

IndexType = c_uint
INDEX_TYPE_UINT16 = 0
INDEX_TYPE_UINT32 = 1

Filter = c_uint
FILTER_NEAREST = 0
FILTER_LINEAR = 1

SamplerMipmapMode = c_uint
SAMPLER_MIPMAP_MODE_NEAREST = 0
SAMPLER_MIPMAP_MODE_LINEAR = 1

SamplerAddressMode = c_uint
SAMPLER_ADDRESS_MODE_REPEAT = 0
SAMPLER_ADDRESS_MODE_MIRRORED_REPEAT = 1
SAMPLER_ADDRESS_MODE_CLAMP_TO_EDGE = 2
SAMPLER_ADDRESS_MODE_CLAMP_TO_BORDER = 3

CompareOp = c_uint
COMPARE_OP_NEVER = 0
COMPARE_OP_LESS = 1
COMPARE_OP_EQUAL = 2
COMPARE_OP_LESS_OR_EQUAL = 3
COMPARE_OP_GREATER = 4
COMPARE_OP_NOT_EQUAL = 5
COMPARE_OP_GREATER_OR_EQUAL = 6
COMPARE_OP_ALWAYS = 7

PolygonMode = c_uint
POLYGON_MODE_FILL = 0
POLYGON_MODE_LINE = 1
POLYGON_MODE_POINT = 2

CullModeFlagBits = c_uint
CULL_MODE_NONE = 0
CULL_MODE_FRONT_BIT = 1<<0
CULL_MODE_BACK_BIT = 1<<1
CULL_MODE_FRONT_AND_BACK = 0x00000003

FrontFace = c_uint
FRONT_FACE_COUNTER_CLOCKWISE = 0
FRONT_FACE_CLOCKWISE = 1

BlendFactor = c_uint
BLEND_FACTOR_ZERO = 0
BLEND_FACTOR_ONE = 1
BLEND_FACTOR_SRC_COLOR = 2
BLEND_FACTOR_ONE_MINUS_SRC_COLOR = 3
BLEND_FACTOR_DST_COLOR = 4
BLEND_FACTOR_ONE_MINUS_DST_COLOR = 5
BLEND_FACTOR_SRC_ALPHA = 6
BLEND_FACTOR_ONE_MINUS_SRC_ALPHA = 7
BLEND_FACTOR_DST_ALPHA = 8
BLEND_FACTOR_ONE_MINUS_DST_ALPHA = 9
BLEND_FACTOR_CONSTANT_COLOR = 10
BLEND_FACTOR_ONE_MINUS_CONSTANT_COLOR = 11
BLEND_FACTOR_CONSTANT_ALPHA = 12
BLEND_FACTOR_ONE_MINUS_CONSTANT_ALPHA = 13
BLEND_FACTOR_SRC_ALPHA_SATURATE = 14
BLEND_FACTOR_SRC1_COLOR = 15
BLEND_FACTOR_ONE_MINUS_SRC1_COLOR = 16
BLEND_FACTOR_SRC1_ALPHA = 17
BLEND_FACTOR_ONE_MINUS_SRC1_ALPHA = 18

BlendOp = c_uint
BLEND_OP_ADD = 0
BLEND_OP_SUBTRACT = 1
BLEND_OP_REVERSE_SUBTRACT = 2
BLEND_OP_MIN = 3
BLEND_OP_MAX = 4

StencilOp = c_uint
STENCIL_OP_KEEP = 0
STENCIL_OP_ZERO = 1
STENCIL_OP_REPLACE = 2
STENCIL_OP_INCREMENT_AND_CLAMP = 3
STENCIL_OP_DECREMENT_AND_CLAMP = 4
STENCIL_OP_INVERT = 5
STENCIL_OP_INCREMENT_AND_WRAP = 6
STENCIL_OP_DECREMENT_AND_WRAP = 7

LogicOp = c_uint
LOGIC_OP_CLEAR = 0
LOGIC_OP_AND = 1
LOGIC_OP_AND_REVERSE = 2
LOGIC_OP_COPY = 3
LOGIC_OP_AND_INVERTED = 4
LOGIC_OP_NO_OP = 5
LOGIC_OP_XOR = 6
LOGIC_OP_OR = 7
LOGIC_OP_NOR = 8
LOGIC_OP_EQUIVALENT = 9
LOGIC_OP_INVERT = 10
LOGIC_OP_OR_REVERSE = 11
LOGIC_OP_COPY_INVERTED = 12
LOGIC_OP_OR_INVERTED = 13
LOGIC_OP_NAND = 14
LOGIC_OP_SET = 15

InternalAllocationType = c_uint
INTERNAL_ALLOCATION_TYPE_EXECUTABLE = 0

SystemAllocationScope = c_uint
SYSTEM_ALLOCATION_SCOPE_COMMAND = 0
SYSTEM_ALLOCATION_SCOPE_OBJECT = 1
SYSTEM_ALLOCATION_SCOPE_CACHE = 2
SYSTEM_ALLOCATION_SCOPE_DEVICE = 3
SYSTEM_ALLOCATION_SCOPE_INSTANCE = 4

PhysicalDeviceType = c_uint
PHYSICAL_DEVICE_TYPE_OTHER = 0
PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU = 1
PHYSICAL_DEVICE_TYPE_DISCRETE_GPU = 2
PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU = 3
PHYSICAL_DEVICE_TYPE_CPU = 4

VertexInputRate = c_uint
VERTEX_INPUT_RATE_VERTEX = 0
VERTEX_INPUT_RATE_INSTANCE = 1

Format = c_uint
FORMAT_UNDEFINED = 0
FORMAT_R4G4_UNORM_PACK8 = 1
FORMAT_R4G4B4A4_UNORM_PACK16 = 2
FORMAT_B4G4R4A4_UNORM_PACK16 = 3
FORMAT_R5G6B5_UNORM_PACK16 = 4
FORMAT_B5G6R5_UNORM_PACK16 = 5
FORMAT_R5G5B5A1_UNORM_PACK16 = 6
FORMAT_B5G5R5A1_UNORM_PACK16 = 7
FORMAT_A1R5G5B5_UNORM_PACK16 = 8
FORMAT_R8_UNORM = 9
FORMAT_R8_SNORM = 10
FORMAT_R8_USCALED = 11
FORMAT_R8_SSCALED = 12
FORMAT_R8_UINT = 13
FORMAT_R8_SINT = 14
FORMAT_R8_SRGB = 15
FORMAT_R8G8_UNORM = 16
FORMAT_R8G8_SNORM = 17
FORMAT_R8G8_USCALED = 18
FORMAT_R8G8_SSCALED = 19
FORMAT_R8G8_UINT = 20
FORMAT_R8G8_SINT = 21
FORMAT_R8G8_SRGB = 22
FORMAT_R8G8B8_UNORM = 23
FORMAT_R8G8B8_SNORM = 24
FORMAT_R8G8B8_USCALED = 25
FORMAT_R8G8B8_SSCALED = 26
FORMAT_R8G8B8_UINT = 27
FORMAT_R8G8B8_SINT = 28
FORMAT_R8G8B8_SRGB = 29
FORMAT_B8G8R8_UNORM = 30
FORMAT_B8G8R8_SNORM = 31
FORMAT_B8G8R8_USCALED = 32
FORMAT_B8G8R8_SSCALED = 33
FORMAT_B8G8R8_UINT = 34
FORMAT_B8G8R8_SINT = 35
FORMAT_B8G8R8_SRGB = 36
FORMAT_R8G8B8A8_UNORM = 37
FORMAT_R8G8B8A8_SNORM = 38
FORMAT_R8G8B8A8_USCALED = 39
FORMAT_R8G8B8A8_SSCALED = 40
FORMAT_R8G8B8A8_UINT = 41
FORMAT_R8G8B8A8_SINT = 42
FORMAT_R8G8B8A8_SRGB = 43
FORMAT_B8G8R8A8_UNORM = 44
FORMAT_B8G8R8A8_SNORM = 45
FORMAT_B8G8R8A8_USCALED = 46
FORMAT_B8G8R8A8_SSCALED = 47
FORMAT_B8G8R8A8_UINT = 48
FORMAT_B8G8R8A8_SINT = 49
FORMAT_B8G8R8A8_SRGB = 50
FORMAT_A8B8G8R8_UNORM_PACK32 = 51
FORMAT_A8B8G8R8_SNORM_PACK32 = 52
FORMAT_A8B8G8R8_USCALED_PACK32 = 53
FORMAT_A8B8G8R8_SSCALED_PACK32 = 54
FORMAT_A8B8G8R8_UINT_PACK32 = 55
FORMAT_A8B8G8R8_SINT_PACK32 = 56
FORMAT_A8B8G8R8_SRGB_PACK32 = 57
FORMAT_A2R10G10B10_UNORM_PACK32 = 58
FORMAT_A2R10G10B10_SNORM_PACK32 = 59
FORMAT_A2R10G10B10_USCALED_PACK32 = 60
FORMAT_A2R10G10B10_SSCALED_PACK32 = 61
FORMAT_A2R10G10B10_UINT_PACK32 = 62
FORMAT_A2R10G10B10_SINT_PACK32 = 63
FORMAT_A2B10G10R10_UNORM_PACK32 = 64
FORMAT_A2B10G10R10_SNORM_PACK32 = 65
FORMAT_A2B10G10R10_USCALED_PACK32 = 66
FORMAT_A2B10G10R10_SSCALED_PACK32 = 67
FORMAT_A2B10G10R10_UINT_PACK32 = 68
FORMAT_A2B10G10R10_SINT_PACK32 = 69
FORMAT_R16_UNORM = 70
FORMAT_R16_SNORM = 71
FORMAT_R16_USCALED = 72
FORMAT_R16_SSCALED = 73
FORMAT_R16_UINT = 74
FORMAT_R16_SINT = 75
FORMAT_R16_SFLOAT = 76
FORMAT_R16G16_UNORM = 77
FORMAT_R16G16_SNORM = 78
FORMAT_R16G16_USCALED = 79
FORMAT_R16G16_SSCALED = 80
FORMAT_R16G16_UINT = 81
FORMAT_R16G16_SINT = 82
FORMAT_R16G16_SFLOAT = 83
FORMAT_R16G16B16_UNORM = 84
FORMAT_R16G16B16_SNORM = 85
FORMAT_R16G16B16_USCALED = 86
FORMAT_R16G16B16_SSCALED = 87
FORMAT_R16G16B16_UINT = 88
FORMAT_R16G16B16_SINT = 89
FORMAT_R16G16B16_SFLOAT = 90
FORMAT_R16G16B16A16_UNORM = 91
FORMAT_R16G16B16A16_SNORM = 92
FORMAT_R16G16B16A16_USCALED = 93
FORMAT_R16G16B16A16_SSCALED = 94
FORMAT_R16G16B16A16_UINT = 95
FORMAT_R16G16B16A16_SINT = 96
FORMAT_R16G16B16A16_SFLOAT = 97
FORMAT_R32_UINT = 98
FORMAT_R32_SINT = 99
FORMAT_R32_SFLOAT = 100
FORMAT_R32G32_UINT = 101
FORMAT_R32G32_SINT = 102
FORMAT_R32G32_SFLOAT = 103
FORMAT_R32G32B32_UINT = 104
FORMAT_R32G32B32_SINT = 105
FORMAT_R32G32B32_SFLOAT = 106
FORMAT_R32G32B32A32_UINT = 107
FORMAT_R32G32B32A32_SINT = 108
FORMAT_R32G32B32A32_SFLOAT = 109
FORMAT_R64_UINT = 110
FORMAT_R64_SINT = 111
FORMAT_R64_SFLOAT = 112
FORMAT_R64G64_UINT = 113
FORMAT_R64G64_SINT = 114
FORMAT_R64G64_SFLOAT = 115
FORMAT_R64G64B64_UINT = 116
FORMAT_R64G64B64_SINT = 117
FORMAT_R64G64B64_SFLOAT = 118
FORMAT_R64G64B64A64_UINT = 119
FORMAT_R64G64B64A64_SINT = 120
FORMAT_R64G64B64A64_SFLOAT = 121
FORMAT_B10G11R11_UFLOAT_PACK32 = 122
FORMAT_E5B9G9R9_UFLOAT_PACK32 = 123
FORMAT_D16_UNORM = 124
FORMAT_X8_D24_UNORM_PACK32 = 125
FORMAT_D32_SFLOAT = 126
FORMAT_S8_UINT = 127
FORMAT_D16_UNORM_S8_UINT = 128
FORMAT_D24_UNORM_S8_UINT = 129
FORMAT_D32_SFLOAT_S8_UINT = 130
FORMAT_BC1_RGB_UNORM_BLOCK = 131
FORMAT_BC1_RGB_SRGB_BLOCK = 132
FORMAT_BC1_RGBA_UNORM_BLOCK = 133
FORMAT_BC1_RGBA_SRGB_BLOCK = 134
FORMAT_BC2_UNORM_BLOCK = 135
FORMAT_BC2_SRGB_BLOCK = 136
FORMAT_BC3_UNORM_BLOCK = 137
FORMAT_BC3_SRGB_BLOCK = 138
FORMAT_BC4_UNORM_BLOCK = 139
FORMAT_BC4_SNORM_BLOCK = 140
FORMAT_BC5_UNORM_BLOCK = 141
FORMAT_BC5_SNORM_BLOCK = 142
FORMAT_BC6H_UFLOAT_BLOCK = 143
FORMAT_BC6H_SFLOAT_BLOCK = 144
FORMAT_BC7_UNORM_BLOCK = 145
FORMAT_BC7_SRGB_BLOCK = 146
FORMAT_ETC2_R8G8B8_UNORM_BLOCK = 147
FORMAT_ETC2_R8G8B8_SRGB_BLOCK = 148
FORMAT_ETC2_R8G8B8A1_UNORM_BLOCK = 149
FORMAT_ETC2_R8G8B8A1_SRGB_BLOCK = 150
FORMAT_ETC2_R8G8B8A8_UNORM_BLOCK = 151
FORMAT_ETC2_R8G8B8A8_SRGB_BLOCK = 152
FORMAT_EAC_R11_UNORM_BLOCK = 153
FORMAT_EAC_R11_SNORM_BLOCK = 154
FORMAT_EAC_R11G11_UNORM_BLOCK = 155
FORMAT_EAC_R11G11_SNORM_BLOCK = 156
FORMAT_ASTC_4x4_UNORM_BLOCK = 157
FORMAT_ASTC_4x4_SRGB_BLOCK = 158
FORMAT_ASTC_5x4_UNORM_BLOCK = 159
FORMAT_ASTC_5x4_SRGB_BLOCK = 160
FORMAT_ASTC_5x5_UNORM_BLOCK = 161
FORMAT_ASTC_5x5_SRGB_BLOCK = 162
FORMAT_ASTC_6x5_UNORM_BLOCK = 163
FORMAT_ASTC_6x5_SRGB_BLOCK = 164
FORMAT_ASTC_6x6_UNORM_BLOCK = 165
FORMAT_ASTC_6x6_SRGB_BLOCK = 166
FORMAT_ASTC_8x5_UNORM_BLOCK = 167
FORMAT_ASTC_8x5_SRGB_BLOCK = 168
FORMAT_ASTC_8x6_UNORM_BLOCK = 169
FORMAT_ASTC_8x6_SRGB_BLOCK = 170
FORMAT_ASTC_8x8_UNORM_BLOCK = 171
FORMAT_ASTC_8x8_SRGB_BLOCK = 172
FORMAT_ASTC_10x5_UNORM_BLOCK = 173
FORMAT_ASTC_10x5_SRGB_BLOCK = 174
FORMAT_ASTC_10x6_UNORM_BLOCK = 175
FORMAT_ASTC_10x6_SRGB_BLOCK = 176
FORMAT_ASTC_10x8_UNORM_BLOCK = 177
FORMAT_ASTC_10x8_SRGB_BLOCK = 178
FORMAT_ASTC_10x10_UNORM_BLOCK = 179
FORMAT_ASTC_10x10_SRGB_BLOCK = 180
FORMAT_ASTC_12x10_UNORM_BLOCK = 181
FORMAT_ASTC_12x10_SRGB_BLOCK = 182
FORMAT_ASTC_12x12_UNORM_BLOCK = 183
FORMAT_ASTC_12x12_SRGB_BLOCK = 184

StructureType = c_uint
STRUCTURE_TYPE_APPLICATION_INFO = 0
STRUCTURE_TYPE_INSTANCE_CREATE_INFO = 1
STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO = 2
STRUCTURE_TYPE_DEVICE_CREATE_INFO = 3
STRUCTURE_TYPE_SUBMIT_INFO = 4
STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO = 5
STRUCTURE_TYPE_MAPPED_MEMORY_RANGE = 6
STRUCTURE_TYPE_BIND_SPARSE_INFO = 7
STRUCTURE_TYPE_FENCE_CREATE_INFO = 8
STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO = 9
STRUCTURE_TYPE_EVENT_CREATE_INFO = 10
STRUCTURE_TYPE_QUERY_POOL_CREATE_INFO = 11
STRUCTURE_TYPE_BUFFER_CREATE_INFO = 12
STRUCTURE_TYPE_BUFFER_VIEW_CREATE_INFO = 13
STRUCTURE_TYPE_IMAGE_CREATE_INFO = 14
STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO = 15
STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO = 16
STRUCTURE_TYPE_PIPELINE_CACHE_CREATE_INFO = 17
STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO = 18
STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO = 19
STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO = 20
STRUCTURE_TYPE_PIPELINE_TESSELLATION_STATE_CREATE_INFO = 21
STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO = 22
STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO = 23
STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO = 24
STRUCTURE_TYPE_PIPELINE_DEPTH_STENCIL_STATE_CREATE_INFO = 25
STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO = 26
STRUCTURE_TYPE_PIPELINE_DYNAMIC_STATE_CREATE_INFO = 27
STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO = 28
STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO = 29
STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO = 30
STRUCTURE_TYPE_SAMPLER_CREATE_INFO = 31
STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO = 32
STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO = 33
STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO = 34
STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET = 35
STRUCTURE_TYPE_COPY_DESCRIPTOR_SET = 36
STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO = 37
STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO = 38
STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO = 39
STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO = 40
STRUCTURE_TYPE_COMMAND_BUFFER_INHERITANCE_INFO = 41
STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO = 42
STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO = 43
STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER = 44
STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER = 45
STRUCTURE_TYPE_MEMORY_BARRIER = 46
STRUCTURE_TYPE_LOADER_INSTANCE_CREATE_INFO = 47
STRUCTURE_TYPE_LOADER_DEVICE_CREATE_INFO = 48

SubpassContents = c_uint
SUBPASS_CONTENTS_INLINE = 0
SUBPASS_CONTENTS_SECONDARY_COMMAND_BUFFERS = 1

Result = c_uint
SUCCESS = 0
NOT_READY = 1
TIMEOUT = 2
EVENT_SET = 3
EVENT_RESET = 4
INCOMPLETE = 5
ERROR_OUT_OF_HOST_MEMORY = -1
ERROR_OUT_OF_DEVICE_MEMORY = -2
ERROR_INITIALIZATION_FAILED = -3
ERROR_DEVICE_LOST = -4
ERROR_MEMORY_MAP_FAILED = -5
ERROR_LAYER_NOT_PRESENT = -6
ERROR_EXTENSION_NOT_PRESENT = -7
ERROR_FEATURE_NOT_PRESENT = -8
ERROR_INCOMPATIBLE_DRIVER = -9
ERROR_TOO_MANY_OBJECTS = -10
ERROR_FORMAT_NOT_SUPPORTED = -11
ERROR_FRAGMENTED_POOL = -12

DynamicState = c_uint
DYNAMIC_STATE_VIEWPORT = 0
DYNAMIC_STATE_SCISSOR = 1
DYNAMIC_STATE_LINE_WIDTH = 2
DYNAMIC_STATE_DEPTH_BIAS = 3
DYNAMIC_STATE_BLEND_CONSTANTS = 4
DYNAMIC_STATE_DEPTH_BOUNDS = 5
DYNAMIC_STATE_STENCIL_COMPARE_MASK = 6
DYNAMIC_STATE_STENCIL_WRITE_MASK = 7
DYNAMIC_STATE_STENCIL_REFERENCE = 8

QueueFlagBits = c_uint
QUEUE_GRAPHICS_BIT = 1<<0
QUEUE_COMPUTE_BIT = 1<<1
QUEUE_TRANSFER_BIT = 1<<2
QUEUE_SPARSE_BINDING_BIT = 1<<3

MemoryPropertyFlagBits = c_uint
MEMORY_PROPERTY_DEVICE_LOCAL_BIT = 1<<0
MEMORY_PROPERTY_HOST_VISIBLE_BIT = 1<<1
MEMORY_PROPERTY_HOST_COHERENT_BIT = 1<<2
MEMORY_PROPERTY_HOST_CACHED_BIT = 1<<3
MEMORY_PROPERTY_LAZILY_ALLOCATED_BIT = 1<<4

MemoryHeapFlagBits = c_uint
MEMORY_HEAP_DEVICE_LOCAL_BIT = 1<<0

AccessFlagBits = c_uint
ACCESS_INDIRECT_COMMAND_READ_BIT = 1<<0
ACCESS_INDEX_READ_BIT = 1<<1
ACCESS_VERTEX_ATTRIBUTE_READ_BIT = 1<<2
ACCESS_UNIFORM_READ_BIT = 1<<3
ACCESS_INPUT_ATTACHMENT_READ_BIT = 1<<4
ACCESS_SHADER_READ_BIT = 1<<5
ACCESS_SHADER_WRITE_BIT = 1<<6
ACCESS_COLOR_ATTACHMENT_READ_BIT = 1<<7
ACCESS_COLOR_ATTACHMENT_WRITE_BIT = 1<<8
ACCESS_DEPTH_STENCIL_ATTACHMENT_READ_BIT = 1<<9
ACCESS_DEPTH_STENCIL_ATTACHMENT_WRITE_BIT = 1<<10
ACCESS_TRANSFER_READ_BIT = 1<<11
ACCESS_TRANSFER_WRITE_BIT = 1<<12
ACCESS_HOST_READ_BIT = 1<<13
ACCESS_HOST_WRITE_BIT = 1<<14
ACCESS_MEMORY_READ_BIT = 1<<15
ACCESS_MEMORY_WRITE_BIT = 1<<16

BufferUsageFlagBits = c_uint
BUFFER_USAGE_TRANSFER_SRC_BIT = 1<<0
BUFFER_USAGE_TRANSFER_DST_BIT = 1<<1
BUFFER_USAGE_UNIFORM_TEXEL_BUFFER_BIT = 1<<2
BUFFER_USAGE_STORAGE_TEXEL_BUFFER_BIT = 1<<3
BUFFER_USAGE_UNIFORM_BUFFER_BIT = 1<<4
BUFFER_USAGE_STORAGE_BUFFER_BIT = 1<<5
BUFFER_USAGE_INDEX_BUFFER_BIT = 1<<6
BUFFER_USAGE_VERTEX_BUFFER_BIT = 1<<7
BUFFER_USAGE_INDIRECT_BUFFER_BIT = 1<<8

BufferCreateFlagBits = c_uint
BUFFER_CREATE_SPARSE_BINDING_BIT = 1<<0
BUFFER_CREATE_SPARSE_RESIDENCY_BIT = 1<<1
BUFFER_CREATE_SPARSE_ALIASED_BIT = 1<<2

ShaderStageFlagBits = c_uint
SHADER_STAGE_VERTEX_BIT = 1<<0
SHADER_STAGE_TESSELLATION_CONTROL_BIT = 1<<1
SHADER_STAGE_TESSELLATION_EVALUATION_BIT = 1<<2
SHADER_STAGE_GEOMETRY_BIT = 1<<3
SHADER_STAGE_FRAGMENT_BIT = 1<<4
SHADER_STAGE_COMPUTE_BIT = 1<<5
SHADER_STAGE_ALL_GRAPHICS = 0x0000001F
SHADER_STAGE_ALL = 0x7FFFFFFF

ImageUsageFlagBits = c_uint
IMAGE_USAGE_TRANSFER_SRC_BIT = 1<<0
IMAGE_USAGE_TRANSFER_DST_BIT = 1<<1
IMAGE_USAGE_SAMPLED_BIT = 1<<2
IMAGE_USAGE_STORAGE_BIT = 1<<3
IMAGE_USAGE_COLOR_ATTACHMENT_BIT = 1<<4
IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT = 1<<5
IMAGE_USAGE_TRANSIENT_ATTACHMENT_BIT = 1<<6
IMAGE_USAGE_INPUT_ATTACHMENT_BIT = 1<<7

ImageCreateFlagBits = c_uint
IMAGE_CREATE_SPARSE_BINDING_BIT = 1<<0
IMAGE_CREATE_SPARSE_RESIDENCY_BIT = 1<<1
IMAGE_CREATE_SPARSE_ALIASED_BIT = 1<<2
IMAGE_CREATE_MUTABLE_FORMAT_BIT = 1<<3
IMAGE_CREATE_CUBE_COMPATIBLE_BIT = 1<<4

PipelineCreateFlagBits = c_uint
PIPELINE_CREATE_DISABLE_OPTIMIZATION_BIT = 1<<0
PIPELINE_CREATE_ALLOW_DERIVATIVES_BIT = 1<<1
PIPELINE_CREATE_DERIVATIVE_BIT = 1<<2

ColorComponentFlagBits = c_uint
COLOR_COMPONENT_R_BIT = 1<<0
COLOR_COMPONENT_G_BIT = 1<<1
COLOR_COMPONENT_B_BIT = 1<<2
COLOR_COMPONENT_A_BIT = 1<<3

FenceCreateFlagBits = c_uint
FENCE_CREATE_SIGNALED_BIT = 1<<0

FormatFeatureFlagBits = c_uint
FORMAT_FEATURE_SAMPLED_IMAGE_BIT = 1<<0
FORMAT_FEATURE_STORAGE_IMAGE_BIT = 1<<1
FORMAT_FEATURE_STORAGE_IMAGE_ATOMIC_BIT = 1<<2
FORMAT_FEATURE_UNIFORM_TEXEL_BUFFER_BIT = 1<<3
FORMAT_FEATURE_STORAGE_TEXEL_BUFFER_BIT = 1<<4
FORMAT_FEATURE_STORAGE_TEXEL_BUFFER_ATOMIC_BIT = 1<<5
FORMAT_FEATURE_VERTEX_BUFFER_BIT = 1<<6
FORMAT_FEATURE_COLOR_ATTACHMENT_BIT = 1<<7
FORMAT_FEATURE_COLOR_ATTACHMENT_BLEND_BIT = 1<<8
FORMAT_FEATURE_DEPTH_STENCIL_ATTACHMENT_BIT = 1<<9
FORMAT_FEATURE_BLIT_SRC_BIT = 1<<10
FORMAT_FEATURE_BLIT_DST_BIT = 1<<11
FORMAT_FEATURE_SAMPLED_IMAGE_FILTER_LINEAR_BIT = 1<<12

QueryControlFlagBits = c_uint
QUERY_CONTROL_PRECISE_BIT = 1<<0

QueryResultFlagBits = c_uint
QUERY_RESULT_64_BIT = 1<<0
QUERY_RESULT_WAIT_BIT = 1<<1
QUERY_RESULT_WITH_AVAILABILITY_BIT = 1<<2
QUERY_RESULT_PARTIAL_BIT = 1<<3

CommandBufferUsageFlagBits = c_uint
COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT = 1<<0
COMMAND_BUFFER_USAGE_RENDER_PASS_CONTINUE_BIT = 1<<1
COMMAND_BUFFER_USAGE_SIMULTANEOUS_USE_BIT = 1<<2

QueryPipelineStatisticFlagBits = c_uint
QUERY_PIPELINE_STATISTIC_INPUT_ASSEMBLY_VERTICES_BIT = 1<<0
QUERY_PIPELINE_STATISTIC_INPUT_ASSEMBLY_PRIMITIVES_BIT = 1<<1
QUERY_PIPELINE_STATISTIC_VERTEX_SHADER_INVOCATIONS_BIT = 1<<2
QUERY_PIPELINE_STATISTIC_GEOMETRY_SHADER_INVOCATIONS_BIT = 1<<3
QUERY_PIPELINE_STATISTIC_GEOMETRY_SHADER_PRIMITIVES_BIT = 1<<4
QUERY_PIPELINE_STATISTIC_CLIPPING_INVOCATIONS_BIT = 1<<5
QUERY_PIPELINE_STATISTIC_CLIPPING_PRIMITIVES_BIT = 1<<6
QUERY_PIPELINE_STATISTIC_FRAGMENT_SHADER_INVOCATIONS_BIT = 1<<7
QUERY_PIPELINE_STATISTIC_TESSELLATION_CONTROL_SHADER_PATCHES_BIT = 1<<8
QUERY_PIPELINE_STATISTIC_TESSELLATION_EVALUATION_SHADER_INVOCATIONS_BIT = 1<<9
QUERY_PIPELINE_STATISTIC_COMPUTE_SHADER_INVOCATIONS_BIT = 1<<10

ImageAspectFlagBits = c_uint
IMAGE_ASPECT_COLOR_BIT = 1<<0
IMAGE_ASPECT_DEPTH_BIT = 1<<1
IMAGE_ASPECT_STENCIL_BIT = 1<<2
IMAGE_ASPECT_METADATA_BIT = 1<<3

SparseImageFormatFlagBits = c_uint
SPARSE_IMAGE_FORMAT_SINGLE_MIPTAIL_BIT = 1<<0
SPARSE_IMAGE_FORMAT_ALIGNED_MIP_SIZE_BIT = 1<<1
SPARSE_IMAGE_FORMAT_NONSTANDARD_BLOCK_SIZE_BIT = 1<<2

SparseMemoryBindFlagBits = c_uint
SPARSE_MEMORY_BIND_METADATA_BIT = 1<<0

PipelineStageFlagBits = c_uint
PIPELINE_STAGE_TOP_OF_PIPE_BIT = 1<<0
PIPELINE_STAGE_DRAW_INDIRECT_BIT = 1<<1
PIPELINE_STAGE_VERTEX_INPUT_BIT = 1<<2
PIPELINE_STAGE_VERTEX_SHADER_BIT = 1<<3
PIPELINE_STAGE_TESSELLATION_CONTROL_SHADER_BIT = 1<<4
PIPELINE_STAGE_TESSELLATION_EVALUATION_SHADER_BIT = 1<<5
PIPELINE_STAGE_GEOMETRY_SHADER_BIT = 1<<6
PIPELINE_STAGE_FRAGMENT_SHADER_BIT = 1<<7
PIPELINE_STAGE_EARLY_FRAGMENT_TESTS_BIT = 1<<8
PIPELINE_STAGE_LATE_FRAGMENT_TESTS_BIT = 1<<9
PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT = 1<<10
PIPELINE_STAGE_COMPUTE_SHADER_BIT = 1<<11
PIPELINE_STAGE_TRANSFER_BIT = 1<<12
PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT = 1<<13
PIPELINE_STAGE_HOST_BIT = 1<<14
PIPELINE_STAGE_ALL_GRAPHICS_BIT = 1<<15
PIPELINE_STAGE_ALL_COMMANDS_BIT = 1<<16

CommandPoolCreateFlagBits = c_uint
COMMAND_POOL_CREATE_TRANSIENT_BIT = 1<<0
COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT = 1<<1

CommandPoolResetFlagBits = c_uint
COMMAND_POOL_RESET_RELEASE_RESOURCES_BIT = 1<<0

CommandBufferResetFlagBits = c_uint
COMMAND_BUFFER_RESET_RELEASE_RESOURCES_BIT = 1<<0

SampleCountFlagBits = c_uint
SAMPLE_COUNT_1_BIT = 1<<0
SAMPLE_COUNT_2_BIT = 1<<1
SAMPLE_COUNT_4_BIT = 1<<2
SAMPLE_COUNT_8_BIT = 1<<3
SAMPLE_COUNT_16_BIT = 1<<4
SAMPLE_COUNT_32_BIT = 1<<5
SAMPLE_COUNT_64_BIT = 1<<6

AttachmentDescriptionFlagBits = c_uint
ATTACHMENT_DESCRIPTION_MAY_ALIAS_BIT = 1<<0

StencilFaceFlagBits = c_uint
STENCIL_FACE_FRONT_BIT = 1<<0
STENCIL_FACE_BACK_BIT = 1<<1
STENCIL_FRONT_AND_BACK = 0x00000003

DescriptorPoolCreateFlagBits = c_uint
DESCRIPTOR_POOL_CREATE_FREE_DESCRIPTOR_SET_BIT = 1<<0

DependencyFlagBits = c_uint
DEPENDENCY_BY_REGION_BIT = 1<<0

PresentModeKHR = c_uint
PRESENT_MODE_IMMEDIATE_KHR = 0
PRESENT_MODE_MAILBOX_KHR = 1
PRESENT_MODE_FIFO_KHR = 2
PRESENT_MODE_FIFO_RELAXED_KHR = 3

ColorSpaceKHR = c_uint
COLOR_SPACE_SRGB_NONLINEAR_KHR = 0

DisplayPlaneAlphaFlagBitsKHR = c_uint
DISPLAY_PLANE_ALPHA_OPAQUE_BIT_KHR = 1<<0
DISPLAY_PLANE_ALPHA_GLOBAL_BIT_KHR = 1<<1
DISPLAY_PLANE_ALPHA_PER_PIXEL_BIT_KHR = 1<<2
DISPLAY_PLANE_ALPHA_PER_PIXEL_PREMULTIPLIED_BIT_KHR = 1<<3

CompositeAlphaFlagBitsKHR = c_uint
COMPOSITE_ALPHA_OPAQUE_BIT_KHR = 1<<0
COMPOSITE_ALPHA_PRE_MULTIPLIED_BIT_KHR = 1<<1
COMPOSITE_ALPHA_POST_MULTIPLIED_BIT_KHR = 1<<2
COMPOSITE_ALPHA_INHERIT_BIT_KHR = 1<<3

SurfaceTransformFlagBitsKHR = c_uint
SURFACE_TRANSFORM_IDENTITY_BIT_KHR = 1<<0
SURFACE_TRANSFORM_ROTATE_90_BIT_KHR = 1<<1
SURFACE_TRANSFORM_ROTATE_180_BIT_KHR = 1<<2
SURFACE_TRANSFORM_ROTATE_270_BIT_KHR = 1<<3
SURFACE_TRANSFORM_HORIZONTAL_MIRROR_BIT_KHR = 1<<4
SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_90_BIT_KHR = 1<<5
SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_180_BIT_KHR = 1<<6
SURFACE_TRANSFORM_HORIZONTAL_MIRROR_ROTATE_270_BIT_KHR = 1<<7
SURFACE_TRANSFORM_INHERIT_BIT_KHR = 1<<8

DebugReportFlagBitsEXT = c_uint
DEBUG_REPORT_INFORMATION_BIT_EXT = 1<<0
DEBUG_REPORT_WARNING_BIT_EXT = 1<<1
DEBUG_REPORT_PERFORMANCE_WARNING_BIT_EXT = 1<<2
DEBUG_REPORT_ERROR_BIT_EXT = 1<<3
DEBUG_REPORT_DEBUG_BIT_EXT = 1<<4

DebugReportObjectTypeEXT = c_uint
DEBUG_REPORT_OBJECT_TYPE_UNKNOWN_EXT = 0
DEBUG_REPORT_OBJECT_TYPE_INSTANCE_EXT = 1
DEBUG_REPORT_OBJECT_TYPE_PHYSICAL_DEVICE_EXT = 2
DEBUG_REPORT_OBJECT_TYPE_DEVICE_EXT = 3
DEBUG_REPORT_OBJECT_TYPE_QUEUE_EXT = 4
DEBUG_REPORT_OBJECT_TYPE_SEMAPHORE_EXT = 5
DEBUG_REPORT_OBJECT_TYPE_COMMAND_BUFFER_EXT = 6
DEBUG_REPORT_OBJECT_TYPE_FENCE_EXT = 7
DEBUG_REPORT_OBJECT_TYPE_DEVICE_MEMORY_EXT = 8
DEBUG_REPORT_OBJECT_TYPE_BUFFER_EXT = 9
DEBUG_REPORT_OBJECT_TYPE_IMAGE_EXT = 10
DEBUG_REPORT_OBJECT_TYPE_EVENT_EXT = 11
DEBUG_REPORT_OBJECT_TYPE_QUERY_POOL_EXT = 12
DEBUG_REPORT_OBJECT_TYPE_BUFFER_VIEW_EXT = 13
DEBUG_REPORT_OBJECT_TYPE_IMAGE_VIEW_EXT = 14
DEBUG_REPORT_OBJECT_TYPE_SHADER_MODULE_EXT = 15
DEBUG_REPORT_OBJECT_TYPE_PIPELINE_CACHE_EXT = 16
DEBUG_REPORT_OBJECT_TYPE_PIPELINE_LAYOUT_EXT = 17
DEBUG_REPORT_OBJECT_TYPE_RENDER_PASS_EXT = 18
DEBUG_REPORT_OBJECT_TYPE_PIPELINE_EXT = 19
DEBUG_REPORT_OBJECT_TYPE_DESCRIPTOR_SET_LAYOUT_EXT = 20
DEBUG_REPORT_OBJECT_TYPE_SAMPLER_EXT = 21
DEBUG_REPORT_OBJECT_TYPE_DESCRIPTOR_POOL_EXT = 22
DEBUG_REPORT_OBJECT_TYPE_DESCRIPTOR_SET_EXT = 23
DEBUG_REPORT_OBJECT_TYPE_FRAMEBUFFER_EXT = 24
DEBUG_REPORT_OBJECT_TYPE_COMMAND_POOL_EXT = 25
DEBUG_REPORT_OBJECT_TYPE_SURFACE_KHR_EXT = 26
DEBUG_REPORT_OBJECT_TYPE_SWAPCHAIN_KHR_EXT = 27
DEBUG_REPORT_OBJECT_TYPE_DEBUG_REPORT_EXT = 28

DebugReportErrorEXT = c_uint
DEBUG_REPORT_ERROR_NONE_EXT = 0
DEBUG_REPORT_ERROR_CALLBACK_REF_EXT = 1

RasterizationOrderAMD = c_uint
RASTERIZATION_ORDER_STRICT_AMD = 0
RASTERIZATION_ORDER_RELAXED_AMD = 1


# FUNC POINTERS

fn_InternalAllocationNotification = FUNCTYPE( None, c_void_p, c_size_t, InternalAllocationType, SystemAllocationScope, )
fn_InternalFreeNotification = FUNCTYPE( None, c_void_p, c_size_t, InternalAllocationType, SystemAllocationScope, )
fn_ReallocationFunction = FUNCTYPE( c_void_p, c_void_p, c_void_p, c_size_t, c_size_t, SystemAllocationScope, )
fn_AllocationFunction = FUNCTYPE( c_void_p, c_void_p, c_size_t, c_size_t, SystemAllocationScope, )
fn_FreeFunction = FUNCTYPE( None, c_void_p, c_void_p, )
fn_VoidFunction = FUNCTYPE( None, )
fn_DebugReportCallbackEXT = FUNCTYPE( Bool32, DebugReportFlagsEXT, DebugReportObjectTypeEXT, c_uint64, c_size_t, c_int, c_char_p, c_char_p, c_void_p, )


# STRUCTURES

Offset2D = define_structure('Offset2D',
    ('x', c_int),
    ('y', c_int),
)

Offset3D = define_structure('Offset3D',
    ('x', c_int),
    ('y', c_int),
    ('z', c_int),
)

Extent2D = define_structure('Extent2D',
    ('width', c_uint),
    ('height', c_uint),
)

Extent3D = define_structure('Extent3D',
    ('width', c_uint),
    ('height', c_uint),
    ('depth', c_uint),
)

Viewport = define_structure('Viewport',
    ('x', c_float),
    ('y', c_float),
    ('width', c_float),
    ('height', c_float),
    ('min_depth', c_float),
    ('max_depth', c_float),
)

Rect2D = define_structure('Rect2D',
    ('offset', Offset2D),
    ('extent', Extent2D),
)

Rect3D = define_structure('Rect3D',
    ('offset', Offset3D),
    ('extent', Extent3D),
)

ClearRect = define_structure('ClearRect',
    ('rect', Rect2D),
    ('base_array_layer', c_uint),
    ('layer_count', c_uint),
)

ComponentMapping = define_structure('ComponentMapping',
    ('r', ComponentSwizzle),
    ('g', ComponentSwizzle),
    ('b', ComponentSwizzle),
    ('a', ComponentSwizzle),
)

PhysicalDeviceLimits = define_structure('PhysicalDeviceLimits',
    ('max_image_dimension1_D', c_uint),
    ('max_image_dimension2_D', c_uint),
    ('max_image_dimension3_D', c_uint),
    ('max_image_dimension_cube', c_uint),
    ('max_image_array_layers', c_uint),
    ('max_texel_buffer_elements', c_uint),
    ('max_uniform_buffer_range', c_uint),
    ('max_storage_buffer_range', c_uint),
    ('max_push_constants_size', c_uint),
    ('max_memory_allocation_count', c_uint),
    ('max_sampler_allocation_count', c_uint),
    ('buffer_image_granularity', DeviceSize),
    ('sparse_address_space_size', DeviceSize),
    ('max_bound_descriptor_sets', c_uint),
    ('max_per_stage_descriptor_samplers', c_uint),
    ('max_per_stage_descriptor_uniform_buffers', c_uint),
    ('max_per_stage_descriptor_storage_buffers', c_uint),
    ('max_per_stage_descriptor_sampled_images', c_uint),
    ('max_per_stage_descriptor_storage_images', c_uint),
    ('max_per_stage_descriptor_input_attachments', c_uint),
    ('max_per_stage_resources', c_uint),
    ('max_descriptor_set_samplers', c_uint),
    ('max_descriptor_set_uniform_buffers', c_uint),
    ('max_descriptor_set_uniform_buffers_dynamic', c_uint),
    ('max_descriptor_set_storage_buffers', c_uint),
    ('max_descriptor_set_storage_buffers_dynamic', c_uint),
    ('max_descriptor_set_sampled_images', c_uint),
    ('max_descriptor_set_storage_images', c_uint),
    ('max_descriptor_set_input_attachments', c_uint),
    ('max_vertex_input_attributes', c_uint),
    ('max_vertex_input_bindings', c_uint),
    ('max_vertex_input_attribute_offset', c_uint),
    ('max_vertex_input_binding_stride', c_uint),
    ('max_vertex_output_components', c_uint),
    ('max_tessellation_generation_level', c_uint),
    ('max_tessellation_patch_size', c_uint),
    ('max_tessellation_control_per_vertex_input_components', c_uint),
    ('max_tessellation_control_per_vertex_output_components', c_uint),
    ('max_tessellation_control_per_patch_output_components', c_uint),
    ('max_tessellation_control_total_output_components', c_uint),
    ('max_tessellation_evaluation_input_components', c_uint),
    ('max_tessellation_evaluation_output_components', c_uint),
    ('max_geometry_shader_invocations', c_uint),
    ('max_geometry_input_components', c_uint),
    ('max_geometry_output_components', c_uint),
    ('max_geometry_output_vertices', c_uint),
    ('max_geometry_total_output_components', c_uint),
    ('max_fragment_input_components', c_uint),
    ('max_fragment_output_attachments', c_uint),
    ('max_fragment_dual_src_attachments', c_uint),
    ('max_fragment_combined_output_resources', c_uint),
    ('max_compute_shared_memory_size', c_uint),
    ('max_compute_work_group_count', (c_uint*3)),
    ('max_compute_work_group_invocations', c_uint),
    ('max_compute_work_group_size', (c_uint*3)),
    ('sub_pixel_precision_bits', c_uint),
    ('sub_texel_precision_bits', c_uint),
    ('mipmap_precision_bits', c_uint),
    ('max_draw_indexed_index_value', c_uint),
    ('max_draw_indirect_count', c_uint),
    ('max_sampler_lod_bias', c_float),
    ('max_sampler_anisotropy', c_float),
    ('max_viewports', c_uint),
    ('max_viewport_dimensions', (c_uint*2)),
    ('viewport_bounds_range', (c_float*2)),
    ('viewport_sub_pixel_bits', c_uint),
    ('min_memory_map_alignment', c_size_t),
    ('min_texel_buffer_offset_alignment', DeviceSize),
    ('min_uniform_buffer_offset_alignment', DeviceSize),
    ('min_storage_buffer_offset_alignment', DeviceSize),
    ('min_texel_offset', c_int),
    ('max_texel_offset', c_uint),
    ('min_texel_gather_offset', c_int),
    ('max_texel_gather_offset', c_uint),
    ('min_interpolation_offset', c_float),
    ('max_interpolation_offset', c_float),
    ('sub_pixel_interpolation_offset_bits', c_uint),
    ('max_framebuffer_width', c_uint),
    ('max_framebuffer_height', c_uint),
    ('max_framebuffer_layers', c_uint),
    ('framebuffer_color_sample_counts', SampleCountFlags),
    ('framebuffer_depth_sample_counts', SampleCountFlags),
    ('framebuffer_stencil_sample_counts', SampleCountFlags),
    ('framebuffer_noAttachments_sample_counts', SampleCountFlags),
    ('max_color_attachments', c_uint),
    ('sampled_image_color_sample_counts', SampleCountFlags),
    ('sampled_image_integer_sample_counts', SampleCountFlags),
    ('sampled_image_depth_sample_counts', SampleCountFlags),
    ('sampled_image_stencil_sample_counts', SampleCountFlags),
    ('storage_image_sample_counts', SampleCountFlags),
    ('max_sample_mask_words', c_uint),
    ('timestamp_compute_and_graphics', Bool32),
    ('timestamp_period', c_float),
    ('max_clip_distances', c_uint),
    ('max_cull_distances', c_uint),
    ('max_combined_clip_and_cull_distances', c_uint),
    ('discrete_queue_priorities', c_uint),
    ('point_size_range', (c_float*2)),
    ('line_width_range', (c_float*2)),
    ('point_size_granularity', c_float),
    ('line_width_granularity', c_float),
    ('strict_lines', Bool32),
    ('standard_sample_locations', Bool32),
    ('optimal_buffer_copy_offset_alignment', DeviceSize),
    ('optimal_buffer_copy_row_pitch_alignment', DeviceSize),
    ('non_coherent_atom_size', DeviceSize),
)

PhysicalDeviceSparseProperties = define_structure('PhysicalDeviceSparseProperties',
    ('residency_standard2_DBlock_shape', Bool32),
    ('residency_standard2_DMultisample_block_shape', Bool32),
    ('residency_standard3_DBlock_shape', Bool32),
    ('residency_aligned_mip_size', Bool32),
    ('residency_non_resident_strict', Bool32),
)

PhysicalDeviceProperties = define_structure('PhysicalDeviceProperties',
    ('api_version', c_uint),
    ('driver_version', c_uint),
    ('vendor_ID', c_uint),
    ('device_ID', c_uint),
    ('device_type', PhysicalDeviceType),
    ('device_name', (c_char*MAX_PHYSICAL_DEVICE_NAME_SIZE)),
    ('pipeline_cache_UUID', (c_uint8*UUID_SIZE)),
    ('limits', PhysicalDeviceLimits),
    ('sparse_properties', PhysicalDeviceSparseProperties),
)

ExtensionProperties = define_structure('ExtensionProperties',
    ('extension_name', (c_char*MAX_EXTENSION_NAME_SIZE)),
    ('spec_version', c_uint),
)

LayerProperties = define_structure('LayerProperties',
    ('layer_name', (c_char*MAX_EXTENSION_NAME_SIZE)),
    ('spec_version', c_uint),
    ('implementation_version', c_uint),
    ('description', (c_char*MAX_DESCRIPTION_SIZE)),
)

ApplicationInfo = define_structure('ApplicationInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('application_name', c_char_p),
    ('application_version', c_uint),
    ('engine_name', c_char_p),
    ('engine_version', c_uint),
    ('api_version', c_uint),
)

AllocationCallbacks = define_structure('AllocationCallbacks',
    ('user_data', c_void_p),
    ('allocation', fn_AllocationFunction),
    ('reallocation', fn_ReallocationFunction),
    ('free', fn_FreeFunction),
    ('internal_allocation', fn_InternalAllocationNotification),
    ('internal_free', fn_InternalFreeNotification),
)

DeviceQueueCreateInfo = define_structure('DeviceQueueCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', DeviceQueueCreateFlags),
    ('queue_family_index', c_uint),
    ('queue_count', c_uint),
    ('queue_priorities', POINTER(c_float)),
)

PhysicalDeviceFeatures = define_structure('PhysicalDeviceFeatures',
    ('robust_buffer_access', Bool32),
    ('full_draw_index_uint32', Bool32),
    ('image_cube_array', Bool32),
    ('independent_blend', Bool32),
    ('geometry_shader', Bool32),
    ('tessellation_shader', Bool32),
    ('sample_rate_shading', Bool32),
    ('dual_src_blend', Bool32),
    ('logic_op', Bool32),
    ('multi_draw_indirect', Bool32),
    ('draw_indirect_first_instance', Bool32),
    ('depth_clamp', Bool32),
    ('depth_bias_clamp', Bool32),
    ('fill_mode_non_solid', Bool32),
    ('depth_bounds', Bool32),
    ('wide_lines', Bool32),
    ('large_points', Bool32),
    ('alpha_toOne', Bool32),
    ('multi_viewport', Bool32),
    ('sampler_anisotropy', Bool32),
    ('texture_compression_ETC2', Bool32),
    ('texture_compression_ASTC__LDR', Bool32),
    ('texture_compression_BC', Bool32),
    ('occlusion_query_precise', Bool32),
    ('pipeline_statistics_query', Bool32),
    ('vertex_pipeline_stores_and_atomics', Bool32),
    ('fragment_stores_and_atomics', Bool32),
    ('shader_tessellation_and_geometry_point_size', Bool32),
    ('shader_image_gather_extended', Bool32),
    ('shader_storage_image_extended_formats', Bool32),
    ('shader_storage_image_multisample', Bool32),
    ('shader_storage_image_read_without_format', Bool32),
    ('shader_storage_image_write_without_format', Bool32),
    ('shader_uniform_buffer_array_dynamic_indexing', Bool32),
    ('shader_sampled_image_array_dynamic_indexing', Bool32),
    ('shader_storage_buffer_array_dynamic_indexing', Bool32),
    ('shader_storage_image_array_dynamic_indexing', Bool32),
    ('shader_clip_distance', Bool32),
    ('shader_cull_distance', Bool32),
    ('shader_float64', Bool32),
    ('shader_int64', Bool32),
    ('shader_int16', Bool32),
    ('shader_resource_residency', Bool32),
    ('shader_resource_min_lod', Bool32),
    ('sparse_binding', Bool32),
    ('sparse_residency_buffer', Bool32),
    ('sparse_residency_image2_D', Bool32),
    ('sparse_residency_image3_D', Bool32),
    ('sparse_residency2_samples', Bool32),
    ('sparse_residency4_samples', Bool32),
    ('sparse_residency8_samples', Bool32),
    ('sparse_residency16_samples', Bool32),
    ('sparse_residency_aliased', Bool32),
    ('variable_multisample_rate', Bool32),
    ('inherited_queries', Bool32),
)

DeviceCreateInfo = define_structure('DeviceCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', DeviceCreateFlags),
    ('queue_create_info_count', c_uint),
    ('queue_create_infos', POINTER(DeviceQueueCreateInfo)),
    ('enabled_layer_count', c_uint),
    ('enabled_layer_names', POINTER(c_char_p)),
    ('enabled_extension_count', c_uint),
    ('enabled_extension_names', POINTER(c_char_p)),
    ('enabled_features', POINTER(PhysicalDeviceFeatures)),
)

InstanceCreateInfo = define_structure('InstanceCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', InstanceCreateFlags),
    ('application_info', POINTER(ApplicationInfo)),
    ('enabled_layer_count', c_uint),
    ('enabled_layer_names', POINTER(c_char_p)),
    ('enabled_extension_count', c_uint),
    ('enabled_extension_names', POINTER(c_char_p)),
)

QueueFamilyProperties = define_structure('QueueFamilyProperties',
    ('queue_flags', QueueFlags),
    ('queue_count', c_uint),
    ('timestamp_valid_bits', c_uint),
    ('min_image_transfer_granularity', Extent3D),
)

MemoryType = define_structure('MemoryType',
    ('property_flags', MemoryPropertyFlags),
    ('heap_index', c_uint),
)

MemoryHeap = define_structure('MemoryHeap',
    ('size', DeviceSize),
    ('flags', MemoryHeapFlags),
)

PhysicalDeviceMemoryProperties = define_structure('PhysicalDeviceMemoryProperties',
    ('memory_type_count', c_uint),
    ('memory_types', (MemoryType*MAX_MEMORY_TYPES)),
    ('memory_heap_count', c_uint),
    ('memory_heaps', (MemoryHeap*MAX_MEMORY_HEAPS)),
)

MemoryAllocateInfo = define_structure('MemoryAllocateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('allocation_size', DeviceSize),
    ('memory_type_index', c_uint),
)

MemoryRequirements = define_structure('MemoryRequirements',
    ('size', DeviceSize),
    ('alignment', DeviceSize),
    ('memory_type_bits', c_uint),
)

SparseImageFormatProperties = define_structure('SparseImageFormatProperties',
    ('aspect_mask', ImageAspectFlags),
    ('image_granularity', Extent3D),
    ('flags', SparseImageFormatFlags),
)

SparseImageMemoryRequirements = define_structure('SparseImageMemoryRequirements',
    ('format_properties', SparseImageFormatProperties),
    ('image_mip_tail_first_lod', c_uint),
    ('image_mip_tail_size', DeviceSize),
    ('image_mip_tail_offset', DeviceSize),
    ('image_mip_tail_stride', DeviceSize),
)

MappedMemoryRange = define_structure('MappedMemoryRange',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('memory', DeviceMemory),
    ('offset', DeviceSize),
    ('size', DeviceSize),
)

FormatProperties = define_structure('FormatProperties',
    ('linear_tiling_features', FormatFeatureFlags),
    ('optimal_tiling_features', FormatFeatureFlags),
    ('buffer_features', FormatFeatureFlags),
)

ImageFormatProperties = define_structure('ImageFormatProperties',
    ('max_extent', Extent3D),
    ('max_mip_levels', c_uint),
    ('max_array_layers', c_uint),
    ('sample_counts', SampleCountFlags),
    ('max_resource_size', DeviceSize),
)

DescriptorBufferInfo = define_structure('DescriptorBufferInfo',
    ('buffer', Buffer),
    ('offset', DeviceSize),
    ('range', DeviceSize),
)

DescriptorImageInfo = define_structure('DescriptorImageInfo',
    ('sampler', Sampler),
    ('image_view', ImageView),
    ('image_layout', ImageLayout),
)

WriteDescriptorSet = define_structure('WriteDescriptorSet',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('dst_set', DescriptorSet),
    ('dst_binding', c_uint),
    ('dst_array_element', c_uint),
    ('descriptor_count', c_uint),
    ('descriptor_type', DescriptorType),
    ('image_info', POINTER(DescriptorImageInfo)),
    ('buffer_info', POINTER(DescriptorBufferInfo)),
    ('texel_buffer_view', POINTER(BufferView)),
)

CopyDescriptorSet = define_structure('CopyDescriptorSet',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('src_set', DescriptorSet),
    ('src_binding', c_uint),
    ('src_array_element', c_uint),
    ('dst_set', DescriptorSet),
    ('dst_binding', c_uint),
    ('dst_array_element', c_uint),
    ('descriptor_count', c_uint),
)

BufferCreateInfo = define_structure('BufferCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', BufferCreateFlags),
    ('size', DeviceSize),
    ('usage', BufferUsageFlags),
    ('sharing_mode', SharingMode),
    ('queue_family_index_count', c_uint),
    ('queue_family_indices', POINTER(c_uint)),
)

BufferViewCreateInfo = define_structure('BufferViewCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', BufferViewCreateFlags),
    ('buffer', Buffer),
    ('format', Format),
    ('offset', DeviceSize),
    ('range', DeviceSize),
)

ImageSubresource = define_structure('ImageSubresource',
    ('aspect_mask', ImageAspectFlags),
    ('mip_level', c_uint),
    ('array_layer', c_uint),
)

ImageSubresourceLayers = define_structure('ImageSubresourceLayers',
    ('aspect_mask', ImageAspectFlags),
    ('mip_level', c_uint),
    ('base_array_layer', c_uint),
    ('layer_count', c_uint),
)

ImageSubresourceRange = define_structure('ImageSubresourceRange',
    ('aspect_mask', ImageAspectFlags),
    ('base_mip_level', c_uint),
    ('level_count', c_uint),
    ('base_array_layer', c_uint),
    ('layer_count', c_uint),
)

MemoryBarrier = define_structure('MemoryBarrier',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('src_access_mask', AccessFlags),
    ('dst_access_mask', AccessFlags),
)

BufferMemoryBarrier = define_structure('BufferMemoryBarrier',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('src_access_mask', AccessFlags),
    ('dst_access_mask', AccessFlags),
    ('src_queue_family_index', c_uint),
    ('dst_queue_family_index', c_uint),
    ('buffer', Buffer),
    ('offset', DeviceSize),
    ('size', DeviceSize),
)

ImageMemoryBarrier = define_structure('ImageMemoryBarrier',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('src_access_mask', AccessFlags),
    ('dst_access_mask', AccessFlags),
    ('old_layout', ImageLayout),
    ('new_layout', ImageLayout),
    ('src_queue_family_index', c_uint),
    ('dst_queue_family_index', c_uint),
    ('image', Image),
    ('subresource_range', ImageSubresourceRange),
)

ImageCreateInfo = define_structure('ImageCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', ImageCreateFlags),
    ('image_type', ImageType),
    ('format', Format),
    ('extent', Extent3D),
    ('mip_levels', c_uint),
    ('array_layers', c_uint),
    ('samples', SampleCountFlagBits),
    ('tiling', ImageTiling),
    ('usage', ImageUsageFlags),
    ('sharing_mode', SharingMode),
    ('queue_family_index_count', c_uint),
    ('queue_family_indices', POINTER(c_uint)),
    ('initial_layout', ImageLayout),
)

SubresourceLayout = define_structure('SubresourceLayout',
    ('offset', DeviceSize),
    ('size', DeviceSize),
    ('row_pitch', DeviceSize),
    ('array_pitch', DeviceSize),
    ('depth_pitch', DeviceSize),
)

ImageViewCreateInfo = define_structure('ImageViewCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', ImageViewCreateFlags),
    ('image', Image),
    ('view_type', ImageViewType),
    ('format', Format),
    ('components', ComponentMapping),
    ('subresource_range', ImageSubresourceRange),
)

BufferCopy = define_structure('BufferCopy',
    ('src_offset', DeviceSize),
    ('dst_offset', DeviceSize),
    ('size', DeviceSize),
)

SparseMemoryBind = define_structure('SparseMemoryBind',
    ('resource_offset', DeviceSize),
    ('size', DeviceSize),
    ('memory', DeviceMemory),
    ('memory_offset', DeviceSize),
    ('flags', SparseMemoryBindFlags),
)

SparseImageMemoryBind = define_structure('SparseImageMemoryBind',
    ('subresource', ImageSubresource),
    ('offset', Offset3D),
    ('extent', Extent3D),
    ('memory', DeviceMemory),
    ('memory_offset', DeviceSize),
    ('flags', SparseMemoryBindFlags),
)

SparseBufferMemoryBindInfo = define_structure('SparseBufferMemoryBindInfo',
    ('buffer', Buffer),
    ('bind_count', c_uint),
    ('binds', POINTER(SparseMemoryBind)),
)

SparseImageOpaqueMemoryBindInfo = define_structure('SparseImageOpaqueMemoryBindInfo',
    ('image', Image),
    ('bind_count', c_uint),
    ('binds', POINTER(SparseMemoryBind)),
)

SparseImageMemoryBindInfo = define_structure('SparseImageMemoryBindInfo',
    ('image', Image),
    ('bind_count', c_uint),
    ('binds', POINTER(SparseImageMemoryBind)),
)

BindSparseInfo = define_structure('BindSparseInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('wait_semaphore_count', c_uint),
    ('wait_semaphores', POINTER(Semaphore)),
    ('buffer_bind_count', c_uint),
    ('buffer_binds', POINTER(SparseBufferMemoryBindInfo)),
    ('image_opaque_bind_count', c_uint),
    ('image_opaque_binds', POINTER(SparseImageOpaqueMemoryBindInfo)),
    ('image_bind_count', c_uint),
    ('image_binds', POINTER(SparseImageMemoryBindInfo)),
    ('signal_semaphore_count', c_uint),
    ('signal_semaphores', POINTER(Semaphore)),
)

ImageCopy = define_structure('ImageCopy',
    ('src_subresource', ImageSubresourceLayers),
    ('src_offset', Offset3D),
    ('dst_subresource', ImageSubresourceLayers),
    ('dst_offset', Offset3D),
    ('extent', Extent3D),
)

ImageBlit = define_structure('ImageBlit',
    ('src_subresource', ImageSubresourceLayers),
    ('src_offsets', (Offset3D*2)),
    ('dst_subresource', ImageSubresourceLayers),
    ('dst_offsets', (Offset3D*2)),
)

BufferImageCopy = define_structure('BufferImageCopy',
    ('buffer_offset', DeviceSize),
    ('buffer_row_length', c_uint),
    ('buffer_image_height', c_uint),
    ('image_subresource', ImageSubresourceLayers),
    ('image_offset', Offset3D),
    ('image_extent', Extent3D),
)

ImageResolve = define_structure('ImageResolve',
    ('src_subresource', ImageSubresourceLayers),
    ('src_offset', Offset3D),
    ('dst_subresource', ImageSubresourceLayers),
    ('dst_offset', Offset3D),
    ('extent', Extent3D),
)

ShaderModuleCreateInfo = define_structure('ShaderModuleCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', ShaderModuleCreateFlags),
    ('code_size', c_size_t),
    ('code', POINTER(c_uint)),
)

DescriptorSetLayoutBinding = define_structure('DescriptorSetLayoutBinding',
    ('binding', c_uint),
    ('descriptor_type', DescriptorType),
    ('descriptor_count', c_uint),
    ('stage_flags', ShaderStageFlags),
    ('immutable_samplers', POINTER(Sampler)),
)

DescriptorSetLayoutCreateInfo = define_structure('DescriptorSetLayoutCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', DescriptorSetLayoutCreateFlags),
    ('binding_count', c_uint),
    ('bindings', POINTER(DescriptorSetLayoutBinding)),
)

DescriptorPoolSize = define_structure('DescriptorPoolSize',
    ('type', DescriptorType),
    ('descriptor_count', c_uint),
)

DescriptorPoolCreateInfo = define_structure('DescriptorPoolCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', DescriptorPoolCreateFlags),
    ('max_sets', c_uint),
    ('pool_size_count', c_uint),
    ('pool_sizes', POINTER(DescriptorPoolSize)),
)

DescriptorSetAllocateInfo = define_structure('DescriptorSetAllocateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('descriptor_pool', DescriptorPool),
    ('descriptor_set_count', c_uint),
    ('set_layouts', POINTER(DescriptorSetLayout)),
)

SpecializationMapEntry = define_structure('SpecializationMapEntry',
    ('constant_ID', c_uint),
    ('offset', c_uint),
    ('size', c_size_t),
)

SpecializationInfo = define_structure('SpecializationInfo',
    ('map_entry_count', c_uint),
    ('map_entries', POINTER(SpecializationMapEntry)),
    ('data_size', c_size_t),
    ('data', c_void_p),
)

PipelineShaderStageCreateInfo = define_structure('PipelineShaderStageCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineShaderStageCreateFlags),
    ('stage', ShaderStageFlagBits),
    ('module', ShaderModule),
    ('name', c_char_p),
    ('specialization_info', POINTER(SpecializationInfo)),
)

ComputePipelineCreateInfo = define_structure('ComputePipelineCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineCreateFlags),
    ('stage', PipelineShaderStageCreateInfo),
    ('layout', PipelineLayout),
    ('base_pipeline_handle', Pipeline),
    ('base_pipeline_index', c_int),
)

VertexInputBindingDescription = define_structure('VertexInputBindingDescription',
    ('binding', c_uint),
    ('stride', c_uint),
    ('input_rate', VertexInputRate),
)

VertexInputAttributeDescription = define_structure('VertexInputAttributeDescription',
    ('location', c_uint),
    ('binding', c_uint),
    ('format', Format),
    ('offset', c_uint),
)

PipelineVertexInputStateCreateInfo = define_structure('PipelineVertexInputStateCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineVertexInputStateCreateFlags),
    ('vertex_binding_description_count', c_uint),
    ('vertex_binding_descriptions', POINTER(VertexInputBindingDescription)),
    ('vertex_attribute_description_count', c_uint),
    ('vertex_attribute_descriptions', POINTER(VertexInputAttributeDescription)),
)

PipelineInputAssemblyStateCreateInfo = define_structure('PipelineInputAssemblyStateCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineInputAssemblyStateCreateFlags),
    ('topology', PrimitiveTopology),
    ('primitive_restart_enable', Bool32),
)

PipelineTessellationStateCreateInfo = define_structure('PipelineTessellationStateCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineTessellationStateCreateFlags),
    ('patch_control_points', c_uint),
)

PipelineViewportStateCreateInfo = define_structure('PipelineViewportStateCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineViewportStateCreateFlags),
    ('viewport_count', c_uint),
    ('viewports', POINTER(Viewport)),
    ('scissor_count', c_uint),
    ('scissors', POINTER(Rect2D)),
)

PipelineRasterizationStateCreateInfo = define_structure('PipelineRasterizationStateCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineRasterizationStateCreateFlags),
    ('depth_clamp_enable', Bool32),
    ('rasterizer_discard_enable', Bool32),
    ('polygon_mode', PolygonMode),
    ('cull_mode', CullModeFlags),
    ('front_face', FrontFace),
    ('depth_bias_enable', Bool32),
    ('depth_bias_constant_factor', c_float),
    ('depth_bias_clamp', c_float),
    ('depth_bias_slope_factor', c_float),
    ('line_width', c_float),
)

PipelineMultisampleStateCreateInfo = define_structure('PipelineMultisampleStateCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineMultisampleStateCreateFlags),
    ('rasterization_samples', SampleCountFlagBits),
    ('sample_shading_enable', Bool32),
    ('min_sample_shading', c_float),
    ('sample_mask', POINTER(SampleMask)),
    ('alpha_toCoverage_enable', Bool32),
    ('alpha_toOne_enable', Bool32),
)

PipelineColorBlendAttachmentState = define_structure('PipelineColorBlendAttachmentState',
    ('blend_enable', Bool32),
    ('src_color_blend_factor', BlendFactor),
    ('dst_color_blend_factor', BlendFactor),
    ('color_blend_op', BlendOp),
    ('src_alpha_blend_factor', BlendFactor),
    ('dst_alpha_blend_factor', BlendFactor),
    ('alpha_blend_op', BlendOp),
    ('color_write_mask', ColorComponentFlags),
)

PipelineColorBlendStateCreateInfo = define_structure('PipelineColorBlendStateCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineColorBlendStateCreateFlags),
    ('logic_opEnable', Bool32),
    ('logic_op', LogicOp),
    ('attachment_count', c_uint),
    ('attachments', POINTER(PipelineColorBlendAttachmentState)),
    ('blend_constants', (c_float*4)),
)

PipelineDynamicStateCreateInfo = define_structure('PipelineDynamicStateCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineDynamicStateCreateFlags),
    ('dynamic_state_count', c_uint),
    ('dynamic_states', POINTER(DynamicState)),
)

StencilOpState = define_structure('StencilOpState',
    ('fail_op', StencilOp),
    ('pass_op', StencilOp),
    ('depth_fail_op', StencilOp),
    ('compare_op', CompareOp),
    ('compare_mask', c_uint),
    ('write_mask', c_uint),
    ('reference', c_uint),
)

PipelineDepthStencilStateCreateInfo = define_structure('PipelineDepthStencilStateCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineDepthStencilStateCreateFlags),
    ('depth_test_enable', Bool32),
    ('depth_write_enable', Bool32),
    ('depth_compare_op', CompareOp),
    ('depth_bounds_test_enable', Bool32),
    ('stencil_test_enable', Bool32),
    ('front', StencilOpState),
    ('back', StencilOpState),
    ('min_depth_bounds', c_float),
    ('max_depth_bounds', c_float),
)

GraphicsPipelineCreateInfo = define_structure('GraphicsPipelineCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineCreateFlags),
    ('stage_count', c_uint),
    ('stages', POINTER(PipelineShaderStageCreateInfo)),
    ('vertex_input_state', POINTER(PipelineVertexInputStateCreateInfo)),
    ('input_assembly_state', POINTER(PipelineInputAssemblyStateCreateInfo)),
    ('tessellation_state', POINTER(PipelineTessellationStateCreateInfo)),
    ('viewport_state', POINTER(PipelineViewportStateCreateInfo)),
    ('rasterization_state', POINTER(PipelineRasterizationStateCreateInfo)),
    ('multisample_state', POINTER(PipelineMultisampleStateCreateInfo)),
    ('depth_stencil_state', POINTER(PipelineDepthStencilStateCreateInfo)),
    ('color_blend_state', POINTER(PipelineColorBlendStateCreateInfo)),
    ('dynamic_state', POINTER(PipelineDynamicStateCreateInfo)),
    ('layout', PipelineLayout),
    ('render_pass', RenderPass),
    ('subpass', c_uint),
    ('base_pipeline_handle', Pipeline),
    ('base_pipeline_index', c_int),
)

PipelineCacheCreateInfo = define_structure('PipelineCacheCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineCacheCreateFlags),
    ('initial_data_size', c_size_t),
    ('initial_data', c_void_p),
)

PushConstantRange = define_structure('PushConstantRange',
    ('stage_flags', ShaderStageFlags),
    ('offset', c_uint),
    ('size', c_uint),
)

PipelineLayoutCreateInfo = define_structure('PipelineLayoutCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', PipelineLayoutCreateFlags),
    ('set_layout_count', c_uint),
    ('set_layouts', POINTER(DescriptorSetLayout)),
    ('push_constant_range_count', c_uint),
    ('push_constant_ranges', POINTER(PushConstantRange)),
)

SamplerCreateInfo = define_structure('SamplerCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', SamplerCreateFlags),
    ('mag_filter', Filter),
    ('min_filter', Filter),
    ('mipmap_mode', SamplerMipmapMode),
    ('address_mode_U', SamplerAddressMode),
    ('address_mode_V', SamplerAddressMode),
    ('address_mode_W', SamplerAddressMode),
    ('mip_lod_bias', c_float),
    ('anisotropy_enable', Bool32),
    ('max_anisotropy', c_float),
    ('compare_enable', Bool32),
    ('compare_op', CompareOp),
    ('min_lod', c_float),
    ('max_lod', c_float),
    ('border_color', BorderColor),
    ('unnormalized_coordinates', Bool32),
)

CommandPoolCreateInfo = define_structure('CommandPoolCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', CommandPoolCreateFlags),
    ('queue_family_index', c_uint),
)

CommandBufferAllocateInfo = define_structure('CommandBufferAllocateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('command_pool', CommandPool),
    ('level', CommandBufferLevel),
    ('command_buffer_count', c_uint),
)

CommandBufferInheritanceInfo = define_structure('CommandBufferInheritanceInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('render_pass', RenderPass),
    ('subpass', c_uint),
    ('framebuffer', Framebuffer),
    ('occlusion_query_enable', Bool32),
    ('query_flags', QueryControlFlags),
    ('pipeline_statistics', QueryPipelineStatisticFlags),
)

CommandBufferBeginInfo = define_structure('CommandBufferBeginInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', CommandBufferUsageFlags),
    ('inheritance_info', POINTER(CommandBufferInheritanceInfo)),
)

ClearColorValue = define_union('ClearColorValue',
    ('float32', (c_float*4)),
    ('int32', (c_int*4)),
    ('uint32', (c_uint*4)),
)

ClearDepthStencilValue = define_structure('ClearDepthStencilValue',
    ('depth', c_float),
    ('stencil', c_uint),
)

ClearValue = define_union('ClearValue',
    ('color', ClearColorValue),
    ('depth_stencil', ClearDepthStencilValue),
)

RenderPassBeginInfo = define_structure('RenderPassBeginInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('render_pass', RenderPass),
    ('framebuffer', Framebuffer),
    ('render_area', Rect2D),
    ('clear_value_count', c_uint),
    ('clear_values', POINTER(ClearValue)),
)

ClearAttachment = define_structure('ClearAttachment',
    ('aspect_mask', ImageAspectFlags),
    ('color_attachment', c_uint),
    ('clear_value', ClearValue),
)

AttachmentDescription = define_structure('AttachmentDescription',
    ('flags', AttachmentDescriptionFlags),
    ('format', Format),
    ('samples', SampleCountFlagBits),
    ('load_op', AttachmentLoadOp),
    ('store_op', AttachmentStoreOp),
    ('stencil_load_op', AttachmentLoadOp),
    ('stencil_store_op', AttachmentStoreOp),
    ('initial_layout', ImageLayout),
    ('final_layout', ImageLayout),
)

AttachmentReference = define_structure('AttachmentReference',
    ('attachment', c_uint),
    ('layout', ImageLayout),
)

SubpassDescription = define_structure('SubpassDescription',
    ('flags', SubpassDescriptionFlags),
    ('pipeline_bind_point', PipelineBindPoint),
    ('input_attachment_count', c_uint),
    ('input_attachments', POINTER(AttachmentReference)),
    ('color_attachment_count', c_uint),
    ('color_attachments', POINTER(AttachmentReference)),
    ('resolve_attachments', POINTER(AttachmentReference)),
    ('depth_stencil_attachment', POINTER(AttachmentReference)),
    ('preserve_attachment_count', c_uint),
    ('preserve_attachments', POINTER(c_uint)),
)

SubpassDependency = define_structure('SubpassDependency',
    ('src_subpass', c_uint),
    ('dst_subpass', c_uint),
    ('src_stage_mask', PipelineStageFlags),
    ('dst_stage_mask', PipelineStageFlags),
    ('src_access_mask', AccessFlags),
    ('dst_access_mask', AccessFlags),
    ('dependency_flags', DependencyFlags),
)

RenderPassCreateInfo = define_structure('RenderPassCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', RenderPassCreateFlags),
    ('attachment_count', c_uint),
    ('attachments', POINTER(AttachmentDescription)),
    ('subpass_count', c_uint),
    ('subpasses', POINTER(SubpassDescription)),
    ('dependency_count', c_uint),
    ('dependencies', POINTER(SubpassDependency)),
)

EventCreateInfo = define_structure('EventCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', EventCreateFlags),
)

FenceCreateInfo = define_structure('FenceCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', FenceCreateFlags),
)

SemaphoreCreateInfo = define_structure('SemaphoreCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', SemaphoreCreateFlags),
)

QueryPoolCreateInfo = define_structure('QueryPoolCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', QueryPoolCreateFlags),
    ('query_type', QueryType),
    ('query_count', c_uint),
    ('pipeline_statistics', QueryPipelineStatisticFlags),
)

FramebufferCreateInfo = define_structure('FramebufferCreateInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', FramebufferCreateFlags),
    ('render_pass', RenderPass),
    ('attachment_count', c_uint),
    ('attachments', POINTER(ImageView)),
    ('width', c_uint),
    ('height', c_uint),
    ('layers', c_uint),
)

DrawIndirectCommand = define_structure('DrawIndirectCommand',
    ('vertex_count', c_uint),
    ('instance_count', c_uint),
    ('first_vertex', c_uint),
    ('first_instance', c_uint),
)

DrawIndexedIndirectCommand = define_structure('DrawIndexedIndirectCommand',
    ('index_count', c_uint),
    ('instance_count', c_uint),
    ('first_index', c_uint),
    ('vertex_offset', c_int),
    ('first_instance', c_uint),
)

DispatchIndirectCommand = define_structure('DispatchIndirectCommand',
    ('x', c_uint),
    ('y', c_uint),
    ('z', c_uint),
)

SubmitInfo = define_structure('SubmitInfo',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('wait_semaphore_count', c_uint),
    ('wait_semaphores', POINTER(Semaphore)),
    ('wait_dst_stage_mask', POINTER(PipelineStageFlags)),
    ('command_buffer_count', c_uint),
    ('command_buffers', POINTER(CommandBuffer)),
    ('signal_semaphore_count', c_uint),
    ('signal_semaphores', POINTER(Semaphore)),
)

DisplayPropertiesKHR = define_structure('DisplayPropertiesKHR',
    ('display', DisplayKHR),
    ('display_name', c_char_p),
    ('physical_dimensions', Extent2D),
    ('physical_resolution', Extent2D),
    ('supported_transforms', SurfaceTransformFlagsKHR),
    ('plane_reorder_possible', Bool32),
    ('persistent_content', Bool32),
)

DisplayPlanePropertiesKHR = define_structure('DisplayPlanePropertiesKHR',
    ('current_display', DisplayKHR),
    ('current_stack_index', c_uint),
)

DisplayModeParametersKHR = define_structure('DisplayModeParametersKHR',
    ('visible_region', Extent2D),
    ('refresh_rate', c_uint),
)

DisplayModePropertiesKHR = define_structure('DisplayModePropertiesKHR',
    ('display_mode', DisplayModeKHR),
    ('parameters', DisplayModeParametersKHR),
)

DisplayModeCreateInfoKHR = define_structure('DisplayModeCreateInfoKHR',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', DisplayModeCreateFlagsKHR),
    ('parameters', DisplayModeParametersKHR),
)

DisplayPlaneCapabilitiesKHR = define_structure('DisplayPlaneCapabilitiesKHR',
    ('supported_alpha', DisplayPlaneAlphaFlagsKHR),
    ('min_src_position', Offset2D),
    ('max_src_position', Offset2D),
    ('min_src_extent', Extent2D),
    ('max_src_extent', Extent2D),
    ('min_dst_position', Offset2D),
    ('max_dst_position', Offset2D),
    ('min_dst_extent', Extent2D),
    ('max_dst_extent', Extent2D),
)

DisplaySurfaceCreateInfoKHR = define_structure('DisplaySurfaceCreateInfoKHR',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', DisplaySurfaceCreateFlagsKHR),
    ('display_mode', DisplayModeKHR),
    ('plane_index', c_uint),
    ('plane_stack_index', c_uint),
    ('transform', SurfaceTransformFlagBitsKHR),
    ('global_alpha', c_float),
    ('alpha_mode', DisplayPlaneAlphaFlagBitsKHR),
    ('image_extent', Extent2D),
)

DisplayPresentInfoKHR = define_structure('DisplayPresentInfoKHR',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('src_rect', Rect2D),
    ('dst_rect', Rect2D),
    ('persistent', Bool32),
)

SurfaceCapabilitiesKHR = define_structure('SurfaceCapabilitiesKHR',
    ('min_image_count', c_uint),
    ('max_image_count', c_uint),
    ('current_extent', Extent2D),
    ('min_image_extent', Extent2D),
    ('max_image_extent', Extent2D),
    ('max_image_array_layers', c_uint),
    ('supported_transforms', SurfaceTransformFlagsKHR),
    ('current_transform', SurfaceTransformFlagBitsKHR),
    ('supported_composite_alpha', CompositeAlphaFlagsKHR),
    ('supported_usage_flags', ImageUsageFlags),
)

AndroidSurfaceCreateInfoKHR = define_structure('AndroidSurfaceCreateInfoKHR',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', AndroidSurfaceCreateFlagsKHR),
    ('window', ANativeWindow),
)

MirSurfaceCreateInfoKHR = define_structure('MirSurfaceCreateInfoKHR',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', MirSurfaceCreateFlagsKHR),
    ('connection', MirConnection),
    ('mir_surface', MirSurface),
)

WaylandSurfaceCreateInfoKHR = define_structure('WaylandSurfaceCreateInfoKHR',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', WaylandSurfaceCreateFlagsKHR),
    ('display', wl_display),
    ('surface', wl_surface),
)

Win32SurfaceCreateInfoKHR = define_structure('Win32SurfaceCreateInfoKHR',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', Win32SurfaceCreateFlagsKHR),
    ('hinstance', HINSTANCE),
    ('hwnd', HWND),
)

XlibSurfaceCreateInfoKHR = define_structure('XlibSurfaceCreateInfoKHR',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', XlibSurfaceCreateFlagsKHR),
    ('dpy', Display),
    ('window', Window),
)

XcbSurfaceCreateInfoKHR = define_structure('XcbSurfaceCreateInfoKHR',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', XcbSurfaceCreateFlagsKHR),
    ('connection', xcb_connection_t),
    ('window', xcb_window_t),
)

SurfaceFormatKHR = define_structure('SurfaceFormatKHR',
    ('format', Format),
    ('color_space', ColorSpaceKHR),
)

SwapchainCreateInfoKHR = define_structure('SwapchainCreateInfoKHR',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', SwapchainCreateFlagsKHR),
    ('surface', SurfaceKHR),
    ('min_image_count', c_uint),
    ('image_format', Format),
    ('image_color_space', ColorSpaceKHR),
    ('image_extent', Extent2D),
    ('image_array_layers', c_uint),
    ('image_usage', ImageUsageFlags),
    ('image_sharing_mode', SharingMode),
    ('queue_family_index_count', c_uint),
    ('queue_family_indices', POINTER(c_uint)),
    ('pre_transform', SurfaceTransformFlagBitsKHR),
    ('composite_alpha', CompositeAlphaFlagBitsKHR),
    ('present_mode', PresentModeKHR),
    ('clipped', Bool32),
    ('old_swapchain', SwapchainKHR),
)

PresentInfoKHR = define_structure('PresentInfoKHR',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('wait_semaphore_count', c_uint),
    ('wait_semaphores', POINTER(Semaphore)),
    ('swapchain_count', c_uint),
    ('swapchains', POINTER(SwapchainKHR)),
    ('image_indices', POINTER(c_uint)),
    ('results', POINTER(Result)),
)

DebugReportCallbackCreateInfoEXT = define_structure('DebugReportCallbackCreateInfoEXT',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('flags', DebugReportFlagsEXT),
    ('callback', fn_DebugReportCallbackEXT),
    ('user_data', c_void_p),
)

PipelineRasterizationStateRasterizationOrderAMD = define_structure('PipelineRasterizationStateRasterizationOrderAMD',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('rasterization_order', RasterizationOrderAMD),
)

DebugMarkerObjectNameInfoEXT = define_structure('DebugMarkerObjectNameInfoEXT',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('object_type', DebugReportObjectTypeEXT),
    ('object', c_uint64),
    ('object_name', c_char_p),
)

DebugMarkerObjectTagInfoEXT = define_structure('DebugMarkerObjectTagInfoEXT',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('object_type', DebugReportObjectTypeEXT),
    ('object', c_uint64),
    ('tag_name', c_uint64),
    ('tag_size', c_size_t),
    ('tag', c_void_p),
)

DebugMarkerMarkerInfoEXT = define_structure('DebugMarkerMarkerInfoEXT',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('marker_name', c_char_p),
    ('color', (c_float*4)),
)

DedicatedAllocationImageCreateInfoNV = define_structure('DedicatedAllocationImageCreateInfoNV',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('dedicated_allocation', Bool32),
)

DedicatedAllocationBufferCreateInfoNV = define_structure('DedicatedAllocationBufferCreateInfoNV',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('dedicated_allocation', Bool32),
)

DedicatedAllocationMemoryAllocateInfoNV = define_structure('DedicatedAllocationMemoryAllocateInfoNV',
    ('s_type', StructureType),
    ('next', c_void_p),
    ('image', Image),
    ('buffer', Buffer),
)


# FUNCTIONS 

DeviceFunctions = (
    (b'vkDestroyDevice', None, Device, POINTER(AllocationCallbacks), ),
    (b'vkGetDeviceQueue', None, Device, c_uint, c_uint, POINTER(Queue), ),
    (b'vkDeviceWaitIdle', Result, Device, ),
    (b'vkAllocateMemory', Result, Device, POINTER(MemoryAllocateInfo), POINTER(AllocationCallbacks), POINTER(DeviceMemory), ),
    (b'vkFreeMemory', None, Device, DeviceMemory, POINTER(AllocationCallbacks), ),
    (b'vkMapMemory', Result, Device, DeviceMemory, DeviceSize, DeviceSize, MemoryMapFlags, c_void_p, ),
    (b'vkUnmapMemory', None, Device, DeviceMemory, ),
    (b'vkFlushMappedMemoryRanges', Result, Device, c_uint, POINTER(MappedMemoryRange), ),
    (b'vkInvalidateMappedMemoryRanges', Result, Device, c_uint, POINTER(MappedMemoryRange), ),
    (b'vkGetDeviceMemoryCommitment', None, Device, DeviceMemory, POINTER(DeviceSize), ),
    (b'vkGetBufferMemoryRequirements', None, Device, Buffer, POINTER(MemoryRequirements), ),
    (b'vkBindBufferMemory', Result, Device, Buffer, DeviceMemory, DeviceSize, ),
    (b'vkGetImageMemoryRequirements', None, Device, Image, POINTER(MemoryRequirements), ),
    (b'vkBindImageMemory', Result, Device, Image, DeviceMemory, DeviceSize, ),
    (b'vkGetImageSparseMemoryRequirements', None, Device, Image, POINTER(c_uint), POINTER(SparseImageMemoryRequirements), ),
    (b'vkCreateFence', Result, Device, POINTER(FenceCreateInfo), POINTER(AllocationCallbacks), POINTER(Fence), ),
    (b'vkDestroyFence', None, Device, Fence, POINTER(AllocationCallbacks), ),
    (b'vkResetFences', Result, Device, c_uint, POINTER(Fence), ),
    (b'vkGetFenceStatus', Result, Device, Fence, ),
    (b'vkWaitForFences', Result, Device, c_uint, POINTER(Fence), Bool32, c_uint64, ),
    (b'vkCreateSemaphore', Result, Device, POINTER(SemaphoreCreateInfo), POINTER(AllocationCallbacks), POINTER(Semaphore), ),
    (b'vkDestroySemaphore', None, Device, Semaphore, POINTER(AllocationCallbacks), ),
    (b'vkCreateEvent', Result, Device, POINTER(EventCreateInfo), POINTER(AllocationCallbacks), POINTER(Event), ),
    (b'vkDestroyEvent', None, Device, Event, POINTER(AllocationCallbacks), ),
    (b'vkGetEventStatus', Result, Device, Event, ),
    (b'vkSetEvent', Result, Device, Event, ),
    (b'vkResetEvent', Result, Device, Event, ),
    (b'vkCreateQueryPool', Result, Device, POINTER(QueryPoolCreateInfo), POINTER(AllocationCallbacks), POINTER(QueryPool), ),
    (b'vkDestroyQueryPool', None, Device, QueryPool, POINTER(AllocationCallbacks), ),
    (b'vkGetQueryPoolResults', Result, Device, QueryPool, c_uint, c_uint, c_size_t, c_void_p, DeviceSize, QueryResultFlags, ),
    (b'vkCreateBuffer', Result, Device, POINTER(BufferCreateInfo), POINTER(AllocationCallbacks), POINTER(Buffer), ),
    (b'vkDestroyBuffer', None, Device, Buffer, POINTER(AllocationCallbacks), ),
    (b'vkCreateBufferView', Result, Device, POINTER(BufferViewCreateInfo), POINTER(AllocationCallbacks), POINTER(BufferView), ),
    (b'vkDestroyBufferView', None, Device, BufferView, POINTER(AllocationCallbacks), ),
    (b'vkCreateImage', Result, Device, POINTER(ImageCreateInfo), POINTER(AllocationCallbacks), POINTER(Image), ),
    (b'vkDestroyImage', None, Device, Image, POINTER(AllocationCallbacks), ),
    (b'vkGetImageSubresourceLayout', None, Device, Image, POINTER(ImageSubresource), POINTER(SubresourceLayout), ),
    (b'vkCreateImageView', Result, Device, POINTER(ImageViewCreateInfo), POINTER(AllocationCallbacks), POINTER(ImageView), ),
    (b'vkDestroyImageView', None, Device, ImageView, POINTER(AllocationCallbacks), ),
    (b'vkCreateShaderModule', Result, Device, POINTER(ShaderModuleCreateInfo), POINTER(AllocationCallbacks), POINTER(ShaderModule), ),
    (b'vkDestroyShaderModule', None, Device, ShaderModule, POINTER(AllocationCallbacks), ),
    (b'vkCreatePipelineCache', Result, Device, POINTER(PipelineCacheCreateInfo), POINTER(AllocationCallbacks), POINTER(PipelineCache), ),
    (b'vkDestroyPipelineCache', None, Device, PipelineCache, POINTER(AllocationCallbacks), ),
    (b'vkGetPipelineCacheData', Result, Device, PipelineCache, POINTER(c_size_t), c_void_p, ),
    (b'vkMergePipelineCaches', Result, Device, PipelineCache, c_uint, POINTER(PipelineCache), ),
    (b'vkCreateGraphicsPipelines', Result, Device, PipelineCache, c_uint, POINTER(GraphicsPipelineCreateInfo), POINTER(AllocationCallbacks), POINTER(Pipeline), ),
    (b'vkCreateComputePipelines', Result, Device, PipelineCache, c_uint, POINTER(ComputePipelineCreateInfo), POINTER(AllocationCallbacks), POINTER(Pipeline), ),
    (b'vkDestroyPipeline', None, Device, Pipeline, POINTER(AllocationCallbacks), ),
    (b'vkCreatePipelineLayout', Result, Device, POINTER(PipelineLayoutCreateInfo), POINTER(AllocationCallbacks), POINTER(PipelineLayout), ),
    (b'vkDestroyPipelineLayout', None, Device, PipelineLayout, POINTER(AllocationCallbacks), ),
    (b'vkCreateSampler', Result, Device, POINTER(SamplerCreateInfo), POINTER(AllocationCallbacks), POINTER(Sampler), ),
    (b'vkDestroySampler', None, Device, Sampler, POINTER(AllocationCallbacks), ),
    (b'vkCreateDescriptorSetLayout', Result, Device, POINTER(DescriptorSetLayoutCreateInfo), POINTER(AllocationCallbacks), POINTER(DescriptorSetLayout), ),
    (b'vkDestroyDescriptorSetLayout', None, Device, DescriptorSetLayout, POINTER(AllocationCallbacks), ),
    (b'vkCreateDescriptorPool', Result, Device, POINTER(DescriptorPoolCreateInfo), POINTER(AllocationCallbacks), POINTER(DescriptorPool), ),
    (b'vkDestroyDescriptorPool', None, Device, DescriptorPool, POINTER(AllocationCallbacks), ),
    (b'vkResetDescriptorPool', Result, Device, DescriptorPool, DescriptorPoolResetFlags, ),
    (b'vkAllocateDescriptorSets', Result, Device, POINTER(DescriptorSetAllocateInfo), POINTER(DescriptorSet), ),
    (b'vkFreeDescriptorSets', Result, Device, DescriptorPool, c_uint, POINTER(DescriptorSet), ),
    (b'vkUpdateDescriptorSets', None, Device, c_uint, POINTER(WriteDescriptorSet), c_uint, POINTER(CopyDescriptorSet), ),
    (b'vkCreateFramebuffer', Result, Device, POINTER(FramebufferCreateInfo), POINTER(AllocationCallbacks), POINTER(Framebuffer), ),
    (b'vkDestroyFramebuffer', None, Device, Framebuffer, POINTER(AllocationCallbacks), ),
    (b'vkCreateRenderPass', Result, Device, POINTER(RenderPassCreateInfo), POINTER(AllocationCallbacks), POINTER(RenderPass), ),
    (b'vkDestroyRenderPass', None, Device, RenderPass, POINTER(AllocationCallbacks), ),
    (b'vkGetRenderAreaGranularity', None, Device, RenderPass, POINTER(Extent2D), ),
    (b'vkCreateCommandPool', Result, Device, POINTER(CommandPoolCreateInfo), POINTER(AllocationCallbacks), POINTER(CommandPool), ),
    (b'vkDestroyCommandPool', None, Device, CommandPool, POINTER(AllocationCallbacks), ),
    (b'vkResetCommandPool', Result, Device, CommandPool, CommandPoolResetFlags, ),
    (b'vkAllocateCommandBuffers', Result, Device, POINTER(CommandBufferAllocateInfo), POINTER(CommandBuffer), ),
    (b'vkFreeCommandBuffers', None, Device, CommandPool, c_uint, POINTER(CommandBuffer), ),
    (b'vkCreateSharedSwapchainsKHR', Result, Device, c_uint, POINTER(SwapchainCreateInfoKHR), POINTER(AllocationCallbacks), POINTER(SwapchainKHR), ),
    (b'vkCreateSwapchainKHR', Result, Device, POINTER(SwapchainCreateInfoKHR), POINTER(AllocationCallbacks), POINTER(SwapchainKHR), ),
    (b'vkDestroySwapchainKHR', None, Device, SwapchainKHR, POINTER(AllocationCallbacks), ),
    (b'vkGetSwapchainImagesKHR', Result, Device, SwapchainKHR, POINTER(c_uint), POINTER(Image), ),
    (b'vkAcquireNextImageKHR', Result, Device, SwapchainKHR, c_uint64, Semaphore, Fence, POINTER(c_uint), ),
    (b'vkDebugMarkerSetObjectNameEXT', Result, Device, POINTER(DebugMarkerObjectNameInfoEXT), ),
    (b'vkDebugMarkerSetObjectTagEXT', Result, Device, POINTER(DebugMarkerObjectTagInfoEXT), ),
)

LoaderFunctions = (
    (b'vkCreateInstance', Result, POINTER(InstanceCreateInfo), POINTER(AllocationCallbacks), POINTER(Instance), ),
    (b'vkEnumerateInstanceLayerProperties', Result, POINTER(c_uint), POINTER(LayerProperties), ),
    (b'vkEnumerateInstanceExtensionProperties', Result, c_char_p, POINTER(c_uint), POINTER(ExtensionProperties), ),
)

QueueFunctions = (
    (b'vkQueueSubmit', Result, Queue, c_uint, POINTER(SubmitInfo), Fence, ),
    (b'vkQueueWaitIdle', Result, Queue, ),
    (b'vkQueueBindSparse', Result, Queue, c_uint, POINTER(BindSparseInfo), Fence, ),
    (b'vkQueuePresentKHR', Result, Queue, POINTER(PresentInfoKHR), ),
)

PhysicalDeviceFunctions = (
    (b'vkGetPhysicalDeviceProperties', None, PhysicalDevice, POINTER(PhysicalDeviceProperties), ),
    (b'vkGetPhysicalDeviceQueueFamilyProperties', None, PhysicalDevice, POINTER(c_uint), POINTER(QueueFamilyProperties), ),
    (b'vkGetPhysicalDeviceMemoryProperties', None, PhysicalDevice, POINTER(PhysicalDeviceMemoryProperties), ),
    (b'vkGetPhysicalDeviceFeatures', None, PhysicalDevice, POINTER(PhysicalDeviceFeatures), ),
    (b'vkGetPhysicalDeviceFormatProperties', None, PhysicalDevice, Format, POINTER(FormatProperties), ),
    (b'vkGetPhysicalDeviceImageFormatProperties', Result, PhysicalDevice, Format, ImageType, ImageTiling, ImageUsageFlags, ImageCreateFlags, POINTER(ImageFormatProperties), ),
    (b'vkCreateDevice', Result, PhysicalDevice, POINTER(DeviceCreateInfo), POINTER(AllocationCallbacks), POINTER(Device), ),
    (b'vkEnumerateDeviceLayerProperties', Result, PhysicalDevice, POINTER(c_uint), POINTER(LayerProperties), ),
    (b'vkEnumerateDeviceExtensionProperties', Result, PhysicalDevice, c_char_p, POINTER(c_uint), POINTER(ExtensionProperties), ),
    (b'vkGetPhysicalDeviceSparseImageFormatProperties', None, PhysicalDevice, Format, ImageType, SampleCountFlagBits, ImageUsageFlags, ImageTiling, POINTER(c_uint), POINTER(SparseImageFormatProperties), ),
    (b'vkGetPhysicalDeviceDisplayPropertiesKHR', Result, PhysicalDevice, POINTER(c_uint), POINTER(DisplayPropertiesKHR), ),
    (b'vkGetPhysicalDeviceDisplayPlanePropertiesKHR', Result, PhysicalDevice, POINTER(c_uint), POINTER(DisplayPlanePropertiesKHR), ),
    (b'vkGetDisplayPlaneSupportedDisplaysKHR', Result, PhysicalDevice, c_uint, POINTER(c_uint), POINTER(DisplayKHR), ),
    (b'vkGetDisplayModePropertiesKHR', Result, PhysicalDevice, DisplayKHR, POINTER(c_uint), POINTER(DisplayModePropertiesKHR), ),
    (b'vkCreateDisplayModeKHR', Result, PhysicalDevice, DisplayKHR, POINTER(DisplayModeCreateInfoKHR), POINTER(AllocationCallbacks), POINTER(DisplayModeKHR), ),
    (b'vkGetDisplayPlaneCapabilitiesKHR', Result, PhysicalDevice, DisplayModeKHR, c_uint, POINTER(DisplayPlaneCapabilitiesKHR), ),
    (b'vkGetPhysicalDeviceMirPresentationSupportKHR', Bool32, PhysicalDevice, c_uint, MirConnection, ),
    (b'vkGetPhysicalDeviceSurfaceSupportKHR', Result, PhysicalDevice, c_uint, SurfaceKHR, POINTER(Bool32), ),
    (b'vkGetPhysicalDeviceSurfaceCapabilitiesKHR', Result, PhysicalDevice, SurfaceKHR, POINTER(SurfaceCapabilitiesKHR), ),
    (b'vkGetPhysicalDeviceSurfaceFormatsKHR', Result, PhysicalDevice, SurfaceKHR, POINTER(c_uint), POINTER(SurfaceFormatKHR), ),
    (b'vkGetPhysicalDeviceSurfacePresentModesKHR', Result, PhysicalDevice, SurfaceKHR, POINTER(c_uint), POINTER(PresentModeKHR), ),
    (b'vkGetPhysicalDeviceWaylandPresentationSupportKHR', Bool32, PhysicalDevice, c_uint, wl_display, ),
    (b'vkGetPhysicalDeviceWin32PresentationSupportKHR', Bool32, PhysicalDevice, c_uint, ),
    (b'vkGetPhysicalDeviceXlibPresentationSupportKHR', Bool32, PhysicalDevice, c_uint, Display, VisualID, ),
    (b'vkGetPhysicalDeviceXcbPresentationSupportKHR', Bool32, PhysicalDevice, c_uint, xcb_connection_t, xcb_visualid_t, ),
)

CommandBufferFunctions = (
    (b'vkBeginCommandBuffer', Result, CommandBuffer, POINTER(CommandBufferBeginInfo), ),
    (b'vkEndCommandBuffer', Result, CommandBuffer, ),
    (b'vkResetCommandBuffer', Result, CommandBuffer, CommandBufferResetFlags, ),
    (b'vkCmdBindPipeline', None, CommandBuffer, PipelineBindPoint, Pipeline, ),
    (b'vkCmdSetViewport', None, CommandBuffer, c_uint, c_uint, POINTER(Viewport), ),
    (b'vkCmdSetScissor', None, CommandBuffer, c_uint, c_uint, POINTER(Rect2D), ),
    (b'vkCmdSetLineWidth', None, CommandBuffer, c_float, ),
    (b'vkCmdSetDepthBias', None, CommandBuffer, c_float, c_float, c_float, ),
    (b'vkCmdSetBlendConstants', None, CommandBuffer, c_float, ),
    (b'vkCmdSetDepthBounds', None, CommandBuffer, c_float, c_float, ),
    (b'vkCmdSetStencilCompareMask', None, CommandBuffer, StencilFaceFlags, c_uint, ),
    (b'vkCmdSetStencilWriteMask', None, CommandBuffer, StencilFaceFlags, c_uint, ),
    (b'vkCmdSetStencilReference', None, CommandBuffer, StencilFaceFlags, c_uint, ),
    (b'vkCmdBindDescriptorSets', None, CommandBuffer, PipelineBindPoint, PipelineLayout, c_uint, c_uint, POINTER(DescriptorSet), c_uint, POINTER(c_uint), ),
    (b'vkCmdBindIndexBuffer', None, CommandBuffer, Buffer, DeviceSize, IndexType, ),
    (b'vkCmdBindVertexBuffers', None, CommandBuffer, c_uint, c_uint, POINTER(Buffer), POINTER(DeviceSize), ),
    (b'vkCmdDraw', None, CommandBuffer, c_uint, c_uint, c_uint, c_uint, ),
    (b'vkCmdDrawIndexed', None, CommandBuffer, c_uint, c_uint, c_uint, c_int, c_uint, ),
    (b'vkCmdDrawIndirect', None, CommandBuffer, Buffer, DeviceSize, c_uint, c_uint, ),
    (b'vkCmdDrawIndexedIndirect', None, CommandBuffer, Buffer, DeviceSize, c_uint, c_uint, ),
    (b'vkCmdDispatch', None, CommandBuffer, c_uint, c_uint, c_uint, ),
    (b'vkCmdDispatchIndirect', None, CommandBuffer, Buffer, DeviceSize, ),
    (b'vkCmdCopyBuffer', None, CommandBuffer, Buffer, Buffer, c_uint, POINTER(BufferCopy), ),
    (b'vkCmdCopyImage', None, CommandBuffer, Image, ImageLayout, Image, ImageLayout, c_uint, POINTER(ImageCopy), ),
    (b'vkCmdBlitImage', None, CommandBuffer, Image, ImageLayout, Image, ImageLayout, c_uint, POINTER(ImageBlit), Filter, ),
    (b'vkCmdCopyBufferToImage', None, CommandBuffer, Buffer, Image, ImageLayout, c_uint, POINTER(BufferImageCopy), ),
    (b'vkCmdCopyImageToBuffer', None, CommandBuffer, Image, ImageLayout, Buffer, c_uint, POINTER(BufferImageCopy), ),
    (b'vkCmdUpdateBuffer', None, CommandBuffer, Buffer, DeviceSize, DeviceSize, c_void_p, ),
    (b'vkCmdFillBuffer', None, CommandBuffer, Buffer, DeviceSize, DeviceSize, c_uint, ),
    (b'vkCmdClearColorImage', None, CommandBuffer, Image, ImageLayout, POINTER(ClearColorValue), c_uint, POINTER(ImageSubresourceRange), ),
    (b'vkCmdClearDepthStencilImage', None, CommandBuffer, Image, ImageLayout, POINTER(ClearDepthStencilValue), c_uint, POINTER(ImageSubresourceRange), ),
    (b'vkCmdClearAttachments', None, CommandBuffer, c_uint, POINTER(ClearAttachment), c_uint, POINTER(ClearRect), ),
    (b'vkCmdResolveImage', None, CommandBuffer, Image, ImageLayout, Image, ImageLayout, c_uint, POINTER(ImageResolve), ),
    (b'vkCmdSetEvent', None, CommandBuffer, Event, PipelineStageFlags, ),
    (b'vkCmdResetEvent', None, CommandBuffer, Event, PipelineStageFlags, ),
    (b'vkCmdWaitEvents', None, CommandBuffer, c_uint, POINTER(Event), PipelineStageFlags, PipelineStageFlags, c_uint, POINTER(MemoryBarrier), c_uint, POINTER(BufferMemoryBarrier), c_uint, POINTER(ImageMemoryBarrier), ),
    (b'vkCmdPipelineBarrier', None, CommandBuffer, PipelineStageFlags, PipelineStageFlags, DependencyFlags, c_uint, POINTER(MemoryBarrier), c_uint, POINTER(BufferMemoryBarrier), c_uint, POINTER(ImageMemoryBarrier), ),
    (b'vkCmdBeginQuery', None, CommandBuffer, QueryPool, c_uint, QueryControlFlags, ),
    (b'vkCmdEndQuery', None, CommandBuffer, QueryPool, c_uint, ),
    (b'vkCmdResetQueryPool', None, CommandBuffer, QueryPool, c_uint, c_uint, ),
    (b'vkCmdWriteTimestamp', None, CommandBuffer, PipelineStageFlagBits, QueryPool, c_uint, ),
    (b'vkCmdCopyQueryPoolResults', None, CommandBuffer, QueryPool, c_uint, c_uint, Buffer, DeviceSize, DeviceSize, QueryResultFlags, ),
    (b'vkCmdPushConstants', None, CommandBuffer, PipelineLayout, ShaderStageFlags, c_uint, c_uint, c_void_p, ),
    (b'vkCmdBeginRenderPass', None, CommandBuffer, POINTER(RenderPassBeginInfo), SubpassContents, ),
    (b'vkCmdNextSubpass', None, CommandBuffer, SubpassContents, ),
    (b'vkCmdEndRenderPass', None, CommandBuffer, ),
    (b'vkCmdExecuteCommands', None, CommandBuffer, c_uint, POINTER(CommandBuffer), ),
    (b'vkCmdDebugMarkerBeginEXT', None, CommandBuffer, POINTER(DebugMarkerMarkerInfoEXT), ),
    (b'vkCmdDebugMarkerEndEXT', None, CommandBuffer, ),
    (b'vkCmdDebugMarkerInsertEXT', None, CommandBuffer, POINTER(DebugMarkerMarkerInfoEXT), ),
)

InstanceFunctions = (
    (b'vkDestroyInstance', None, Instance, POINTER(AllocationCallbacks), ),
    (b'vkEnumeratePhysicalDevices', Result, Instance, POINTER(c_uint), POINTER(PhysicalDevice), ),
    (b'vkGetDeviceProcAddr', fn_VoidFunction, Device, c_char_p, ),
    (b'vkCreateAndroidSurfaceKHR', Result, Instance, POINTER(AndroidSurfaceCreateInfoKHR), POINTER(AllocationCallbacks), POINTER(SurfaceKHR), ),
    (b'vkCreateDisplayPlaneSurfaceKHR', Result, Instance, POINTER(DisplaySurfaceCreateInfoKHR), POINTER(AllocationCallbacks), POINTER(SurfaceKHR), ),
    (b'vkCreateMirSurfaceKHR', Result, Instance, POINTER(MirSurfaceCreateInfoKHR), POINTER(AllocationCallbacks), POINTER(SurfaceKHR), ),
    (b'vkDestroySurfaceKHR', None, Instance, SurfaceKHR, POINTER(AllocationCallbacks), ),
    (b'vkCreateWaylandSurfaceKHR', Result, Instance, POINTER(WaylandSurfaceCreateInfoKHR), POINTER(AllocationCallbacks), POINTER(SurfaceKHR), ),
    (b'vkCreateWin32SurfaceKHR', Result, Instance, POINTER(Win32SurfaceCreateInfoKHR), POINTER(AllocationCallbacks), POINTER(SurfaceKHR), ),
    (b'vkCreateXlibSurfaceKHR', Result, Instance, POINTER(XlibSurfaceCreateInfoKHR), POINTER(AllocationCallbacks), POINTER(SurfaceKHR), ),
    (b'vkCreateXcbSurfaceKHR', Result, Instance, POINTER(XcbSurfaceCreateInfoKHR), POINTER(AllocationCallbacks), POINTER(SurfaceKHR), ),
    (b'vkCreateDebugReportCallbackEXT', Result, Instance, POINTER(DebugReportCallbackCreateInfoEXT), POINTER(AllocationCallbacks), POINTER(DebugReportCallbackEXT), ),
    (b'vkDestroyDebugReportCallbackEXT', None, Instance, DebugReportCallbackEXT, POINTER(AllocationCallbacks), ),
    (b'vkDebugReportMessageEXT', None, Instance, DebugReportFlagsEXT, DebugReportObjectTypeEXT, c_uint64, c_size_t, c_int, c_char_p, c_char_p, ),
)

GetInstanceProcAddr = vk.vkGetInstanceProcAddr
GetInstanceProcAddr.restype = fn_VoidFunction
GetInstanceProcAddr.argtypes = (Instance, c_char_p, )

# EXTENSIONS 

#VK_KHR_surface
KHR_SURFACE_SPEC_VERSION = 25
KHR_SURFACE_EXTENSION_NAME = "VK_KHR_surface"
ERROR_SURFACE_LOST_KHR = -1000000000
ERROR_NATIVE_WINDOW_IN_USE_KHR = -1000000001
COLORSPACE_SRGB_NONLINEAR_KHR = COLOR_SPACE_SRGB_NONLINEAR_KHR

#VK_KHR_swapchain
KHR_SWAPCHAIN_SPEC_VERSION = 68
KHR_SWAPCHAIN_EXTENSION_NAME = "VK_KHR_swapchain"
STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR = 1000001000
STRUCTURE_TYPE_PRESENT_INFO_KHR = 1000001001
IMAGE_LAYOUT_PRESENT_SRC_KHR = 1000001002
SUBOPTIMAL_KHR = 1000001003
ERROR_OUT_OF_DATE_KHR = -1000001004

#VK_KHR_display
KHR_DISPLAY_SPEC_VERSION = 21
KHR_DISPLAY_EXTENSION_NAME = "VK_KHR_display"
STRUCTURE_TYPE_DISPLAY_MODE_CREATE_INFO_KHR = 1000002000
STRUCTURE_TYPE_DISPLAY_SURFACE_CREATE_INFO_KHR = 1000002001

#VK_KHR_display_swapchain
KHR_DISPLAY_SWAPCHAIN_SPEC_VERSION = 9
KHR_DISPLAY_SWAPCHAIN_EXTENSION_NAME = "VK_KHR_display_swapchain"
STRUCTURE_TYPE_DISPLAY_PRESENT_INFO_KHR = 1000003000
ERROR_INCOMPATIBLE_DISPLAY_KHR = -1000003001

#VK_KHR_xlib_surface
KHR_XLIB_SURFACE_SPEC_VERSION = 6
KHR_XLIB_SURFACE_EXTENSION_NAME = "VK_KHR_xlib_surface"
STRUCTURE_TYPE_XLIB_SURFACE_CREATE_INFO_KHR = 1000004000

#VK_KHR_xcb_surface
KHR_XCB_SURFACE_SPEC_VERSION = 6
KHR_XCB_SURFACE_EXTENSION_NAME = "VK_KHR_xcb_surface"
STRUCTURE_TYPE_XCB_SURFACE_CREATE_INFO_KHR = 1000005000

#VK_KHR_wayland_surface
KHR_WAYLAND_SURFACE_SPEC_VERSION = 5
KHR_WAYLAND_SURFACE_EXTENSION_NAME = "VK_KHR_wayland_surface"
STRUCTURE_TYPE_WAYLAND_SURFACE_CREATE_INFO_KHR = 1000006000

#VK_KHR_mir_surface
KHR_MIR_SURFACE_SPEC_VERSION = 4
KHR_MIR_SURFACE_EXTENSION_NAME = "VK_KHR_mir_surface"
STRUCTURE_TYPE_MIR_SURFACE_CREATE_INFO_KHR = 1000007000

#VK_KHR_android_surface
KHR_ANDROID_SURFACE_SPEC_VERSION = 6
KHR_ANDROID_SURFACE_EXTENSION_NAME = "VK_KHR_android_surface"
STRUCTURE_TYPE_ANDROID_SURFACE_CREATE_INFO_KHR = 1000008000

#VK_KHR_win32_surface
KHR_WIN32_SURFACE_SPEC_VERSION = 5
KHR_WIN32_SURFACE_EXTENSION_NAME = "VK_KHR_win32_surface"
STRUCTURE_TYPE_WIN32_SURFACE_CREATE_INFO_KHR = 1000009000

#VK_ANDROID_native_buffer
ANDROID_NATIVE_BUFFER_SPEC_VERSION = 4
ANDROID_NATIVE_BUFFER_NUMBER = 11
ANDROID_NATIVE_BUFFER_NAME = "VK_ANDROID_native_buffer"

#VK_EXT_debug_report
EXT_DEBUG_REPORT_SPEC_VERSION = 3
EXT_DEBUG_REPORT_EXTENSION_NAME = "VK_EXT_debug_report"
STRUCTURE_TYPE_DEBUG_REPORT_CALLBACK_CREATE_INFO_EXT = 1000011000
ERROR_VALIDATION_FAILED_EXT = -1000011001
STRUCTURE_TYPE_DEBUG_REPORT_CREATE_INFO_EXT = STRUCTURE_TYPE_DEBUG_REPORT_CALLBACK_CREATE_INFO_EXT

#VK_NV_glsl_shader
NV_GLSL_SHADER_SPEC_VERSION = 1
NV_GLSL_SHADER_EXTENSION_NAME = "VK_NV_glsl_shader"
ERROR_INVALID_SHADER_NV = -1000012000

#VK_KHR_sampler_mirror_clamp_to_edge
KHR_SAMPLER_MIRROR_CLAMP_TO_EDGE_SPEC_VERSION = 1
KHR_SAMPLER_MIRROR_CLAMP_TO_EDGE_EXTENSION_NAME = "VK_KHR_sampler_mirror_clamp_to_edge"
SAMPLER_ADDRESS_MODE_MIRROR_CLAMP_TO_EDGE = 4

#VK_IMG_filter_cubic
IMG_FILTER_CUBIC_SPEC_VERSION = 1
IMG_FILTER_CUBIC_EXTENSION_NAME = "VK_IMG_filter_cubic"
FILTER_CUBIC_IMG = 1000015000
FORMAT_FEATURE_SAMPLED_IMAGE_FILTER_CUBIC_BIT_IMG = 1<<13

#VK_AMD_rasterization_order
AMD_RASTERIZATION_ORDER_SPEC_VERSION = 1
AMD_RASTERIZATION_ORDER_EXTENSION_NAME = "VK_AMD_rasterization_order"
STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_RASTERIZATION_ORDER_AMD = 1000018000

#VK_AMD_shader_trinary_minmax
AMD_SHADER_TRINARY_MINMAX_SPEC_VERSION = 1
AMD_SHADER_TRINARY_MINMAX_EXTENSION_NAME = "VK_AMD_shader_trinary_minmax"

#VK_AMD_shader_explicit_vertex_parameter
AMD_SHADER_EXPLICIT_VERTEX_PARAMETER_SPEC_VERSION = 1
AMD_SHADER_EXPLICIT_VERTEX_PARAMETER_EXTENSION_NAME = "VK_AMD_shader_explicit_vertex_parameter"

#VK_EXT_debug_marker
EXT_DEBUG_MARKER_SPEC_VERSION = 3
EXT_DEBUG_MARKER_EXTENSION_NAME = "VK_EXT_debug_marker"
STRUCTURE_TYPE_DEBUG_MARKER_OBJECT_NAME_INFO_EXT = 1000022000
STRUCTURE_TYPE_DEBUG_MARKER_OBJECT_TAG_INFO_EXT = 1000022001
STRUCTURE_TYPE_DEBUG_MARKER_MARKER_INFO_EXT = 1000022002

#VK_AMD_gcn_shader
AMD_GCN_SHADER_SPEC_VERSION = 1
AMD_GCN_SHADER_EXTENSION_NAME = "VK_AMD_gcn_shader"

#VK_NV_dedicated_allocation
NV_DEDICATED_ALLOCATION_SPEC_VERSION = 1
NV_DEDICATED_ALLOCATION_EXTENSION_NAME = "VK_NV_dedicated_allocation"
STRUCTURE_TYPE_DEDICATED_ALLOCATION_IMAGE_CREATE_INFO_NV = 1000026000
STRUCTURE_TYPE_DEDICATED_ALLOCATION_BUFFER_CREATE_INFO_NV = 1000026001
STRUCTURE_TYPE_DEDICATED_ALLOCATION_MEMORY_ALLOCATE_INFO_NV = 1000026002



# Load the loader functions in the module namespace
loc = locals()
for name, fnptr in load_functions(Instance(0), LoaderFunctions, GetInstanceProcAddr):
    loc[name] = fnptr
del loc

