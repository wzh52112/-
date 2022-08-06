import time

import numpy as np
from kivy.app import App
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.utils import platform

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([
        Permission.INTERNET,
        Permission.CAMERA,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.INTERNET
    ])


#保存
class CameraClick(BoxLayout):
    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")




class main(App):

    def build(self):
        return CameraClick()


main().run()