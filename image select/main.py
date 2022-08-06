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
from kivy.utils import platform
if platform == "android":
  from android.permissions import request_permissions, Permission
  request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET,Permission.CAMERA])
  from android.storage import app_storage_path
  settings_path = app_storage_path()
#from android.permissions import request_permissions, Permission

#request_permissions([
#   Permission.INTERNET,
#   Permission.WRITE_EXTERNAL_STORAGE,
#   Permission.READ_EXTERNAL_STORAGE,
#   Permission.ACCESS_NETWORK_STATE,
#   Permission.ACCESS_NOTIFICATION_POLICY,
#   Permission.MOUNT_UNMOUNT_FILESYSTEMS,
#   Permission.WRITE_EXTERNAL_STORAGE
#])


 #  Permission.READ_MEDIA_VIDEO,
 #  Permission.ACCESS_MEDIA_LOCATION,
 #  Permission.READ_HOME_APP_SEARCH_DATA,
 #  Permission.WRITE_GSERVICES



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
    self._popup = Popup(title="select image", content=content, size_hint=(0.9, 0.9))  #,background_color=[40,40,40,1]
    self._popup.open()

  def load(self, path, filename):
    filename = str(filename).replace("[", " ")
    filename = str(filename).replace("]", " ")
    filename = str(filename).replace(" ", "")
    filename = str(filename).replace("\\\\", "\\")
    filename = str(filename).replace("'", "")
    filename = str(filename).replace("/", "//")
    upload_url = "http://36.139.166.71:5000/"
    file = {"file": open(filename, "rb")}  #filename
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


    la = Button(text="name:"+h5, italic=True,background_color= [.0, 1, 1, .0],size_hint=[ 1, .15],color=[188,188,183,1])
    self.add_widget(la)
    la2 = Button(text="time:"+h6, italic=True,background_color= [.0, 1, 1, .0],size_hint=[ 1, .15],color=[188,188,183,1])
    self.add_widget(la2)
    btn = Button(text="return",
                 size_hint=[ 1, .15], height=100,halign='center',valign='center',background_down="Pressed.jpg",background_normal="Default.jpg")
    btn.bind(on_release=self.changeLayout)
    self.add_widget(btn)



    self.dismiss_popup()



  def dismiss_popup(self):
    self._popup.dismiss()

  def Press(self):
    self.clear_widgets()
    self.add_widget(CameraClick())


  def changeLayout(self, instance):
    self.clear_widgets()
    self.add_widget(LayoutTest2())








class LayoutTest2(BoxLayout):
  def __init__(self, **kwargs):
    super().__init__(**kwargs,orientation="vertical",spacing= 0)
    #GridLayout.__init__(self, cols=1,orientation="lr-tb",spacing= 0)




    btn3 = Button(text="ture?",
                 font_size=35, color=[43,43,43,1], bold=True, background_color=[0, 1, 1, .0])
    self.add_widget(btn3)

    btn = Button(text="ture",
                   font_size=35, bold=True,background_color=[1, 1, 1, 1],background_down="Pressed.jpg",background_normal="Default.jpg",size_hint=[ 1, 0.2])
    btn.bind(on_release=self.changeLayout)
    self.add_widget(btn)



  def changeLayout(self, instance):
    self.clear_widgets()
    self.add_widget(BoxLayoutWidget())




class CameraClick(BoxLayout):
  orientation= 'vertical'
  loadfile = ObjectProperty(None)
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    btn4 = Button(text="Play",size_hint_y= None,height= '48dp',background_down="Pressed.jpg",background_normal="Default.jpg")
    btn4.bind(on_release=self.load)
    self.add_widget(btn4)

    btn = Button(text="return",size_hint_y= None,height= '48dp',background_down="Pressed.jpg",background_normal="Default.jpg")
    btn.bind(on_release=self.changeLayout)
    self.add_widget(btn)

  def capture(self):
    camera = self.ids['camera']
    #timestr = time.strftime("%Y%m%d_%H%M%S")
    camera.export_to_png("//storage//emulated//0//IMG.png") #.format(timestr)  #_{}

  def load(self, filename):
    filename = "//storage//emulated//0//IMG.png" #_{}
    upload_url = "http://36.139.166.71:5000/"
    file = {"file": open(filename, "rb")}  #filename
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

    la = Button(text="name:"+h5, italic=True,background_color= [.0, 1, 1, .0],size_hint=[ 1, .15],color=[188,188,183,1])
    self.add_widget(la)
    la2 = Button(text="time:"+h6, italic=True,background_color= [.0, 1, 1, .0],size_hint=[ 1, .15],color=[188,188,183,1])
    self.add_widget(la2)
    btn = Button(text="return",
                 size_hint=[ 1, .15], height=100,halign='center',valign='center',background_down="Pressed.jpg",background_normal="Default.jpg")
    btn.bind(on_release=self.changeLayout)
    self.add_widget(btn)



  def changeLayout(self, instance):
    self.clear_widgets()
    self.add_widget(LayoutTest2())


class FileChooserApp(App):
  def build(self):
    return FileChooserBox()


class BoxApp(App):
  def build(self):
    return BoxLayoutWidget()

if __name__ == '__main__':
  BoxApp().run()
