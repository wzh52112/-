from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from time import strftime
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.base import runTouchApp
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
import requests
import urllib
import certifi
import chardet
import urllib3
from bs4 import BeautifulSoup
import re
import time
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.camera import Camera


class MyFileChooser(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class BoxLayoutWidget(BoxLayout):
    loadfile = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_start(self):
        Clock.schedule_interval(self.update_time, 0)

    loadfile = ObjectProperty(None)

    def show_load(self):
        content = MyFileChooser(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="select image", content=content,
                            size_hint=(0.9, 0.9))  # ,background_color=[40,40,40,1]
        self._popup.open()

    def load(self, path, filename):
        filename = str(filename).replace("[", " ")
        filename = str(filename).replace("]", " ")
        filename = str(filename).replace(" ", "")
        filename = str(filename).replace("\\\\", "\\")
        filename = str(filename).replace("'", "")
        filename = str(filename).replace("/", "//")
        upload_url = "http://36.139.166.71:5000/"
        file = {"file": open(filename, "rb")}  # filename
        upload_res = requests.post(url=upload_url, files=file)
        soup = BeautifulSoup(upload_res.text, 'html.parser')
        l = soup.find('img').get("src").strip()

        shuru = "http://36.139.166.71:5000" + l
        shuchu = "http://36.139.166.71:5000" + "/result" + l
        title = soup.select('h5')

        h5 = soup.find('h5', class_="h5 mb-3 font-weight-normal").encode_contents().decode('utf-8')

        h6 = soup.find('h5', class_="h6 mb-3 font-weight-normal").encode_contents().decode('utf-8')
        h5 = h5.replace("检测到： ", " ")
        h5 = h5.replace(",  ", "")
        h5 = h5.replace(",", "")
        h5 = h5.replace(" ", "")
        h6 = h6.replace("检测时间： (", "")
        h6 = h6.replace(") ", "")
        self.clear_widgets()

        la3 = AsyncImage(source=shuru)
        self.add_widget(la3)
        la4 = AsyncImage(source=shuchu)
        self.add_widget(la4)

        la = Button(text="name:" + h5, italic=True, background_color=[.0, 1, 1, .0], size_hint=[1, .15],
                    color=[188, 188, 183, 1])
        self.add_widget(la)
        la2 = Button(text="time:" + h6, italic=True, background_color=[.0, 1, 1, .0], size_hint=[1, .15],
                     color=[188, 188, 183, 1])
        self.add_widget(la2)
        btn = Button(text="return",
                     size_hint=[1, .15], height=100, halign='center', valign='center', background_down="Pressed.jpg",
                     background_normal="Default.jpg")
        btn.bind(on_release=self.changeLayout)
        self.add_widget(btn)




class BoxApp(App):
  def build(self):
    return BoxLayoutWidget()

if __name__ == '__main__':
  BoxApp().run()
