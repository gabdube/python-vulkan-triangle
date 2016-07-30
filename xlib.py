"""
    Minimalistic wrapper over the XLIB window api
"""

import weakref

class XlibWindow(object):
    
    def __init__(self, app):
        app = weakref.ref(app)

class XlibSwapchain(object):
    
    def create_surface(self):
        pass
    
    def __init__(self, app):
        self.app = weakref.ref(app)
        self.surface = None
        self.swapchain = None
        self.images = None
        self.views = None
        self.create_surface()