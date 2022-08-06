from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import time
import cv2 as cv
import numpy as np
import os
import cv2




class CameraScreen(Screen):
    global camera_id  # 选择摄像头
    camera_id = 0  # 默认摄像头
    global compensation  # 曝光补偿
    compensation = 1  # 默认曝光补偿

    def selectCamera(self, i):
        """切换摄像头"""
        global camera_id  # 声明用到的全局变量
        camera_id = i
        print("selected camera " + str(camera_id))  # print语句只是为了运行的时候看看是否正常运行，后面都是如此
        return camera_id

    def selectCompensation(self, i):
        """设置曝光补偿"""
        global compensation
        compensation = i
        print("selected compensation " + str(compensation))
        return compensation

    def takePicture(self):
        """拍摄函数"""
        global compensation
        global camera_id
        global camera
        pic_list = []  # 由于这个程序是为了实现合成HDR所以需要拍摄多张图片，用pic_list列表保存图片名称
        take_picture_number = 3  # 设置包围曝光拍摄3张照片合成1张HDR
        self.ids['sjnCamera'].play = False  # 尝试关闭预览的相机，后面再打开，以修复bug，但是并没有成功
        cam = cv2.VideoCapture(camera_id)  # 创建相机实例
        exposure_list = self.getExposureList(cam, compensation)  # 调用本类函数，获得快门速度序列，返回成一个列表，保存快门速度
        cwd = os.getcwd()  # 当前工作路径
        cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # 设置为手动曝光
        while take_picture_number:
            for t in exposure_list:
                cam.set(cv2.CAP_PROP_EXPOSURE, t)  # 传入快门速度，拍摄合成HDR所需要的照片
                ret, frame_read = cam.read()
                if ret:
                    time_str = time.strftime("%H%M%S")
                    picture_name = "IMG_{}".format(time_str) + "_" + str(take_picture_number) + ".jpg"  # 图片名称
                    save_path = cwd + "/LDR/" + picture_name  # 拍摄照片保存路径
                    cv2.imwrite(save_path, frame_read)
                    pic_list.append(picture_name)  # 图片名称序列
                    print('保存图像成功')
                    print("camera_id:" + str(camera_id))
                    take_picture_number -= 1
                else:
                    print("获取失败")
                    break
        cam.release()
        cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # 设置回自动曝光

        file_name = self.writeList(cwd, pic_list, exposure_list)  # 调用本类函数，写入txt，这个txt是后面合成HDR需要用到的。
        self.createHDR(cwd, file_name, time_str)  # 调用本类函数，生成HDR，并保存
        self.ids['sjnCamera'].play = True

    def getExposureList(self, cam, compensation):
        """生成快门速度序列"""
        exposure_list = []
        auto_exposure_time = 1 / float(cv2.CAP_PROP_EXPOSURE)  # 获取标准曝光时间
        if compensation == 2:  # 两档曝光补偿，自动测光的快门速度除以4和乘以4
            exposure_time_m = auto_exposure_time / 4
            exposure_time_p = auto_exposure_time * 4
            exposure_list.append(exposure_time_m)  # 曝光时间序列
            exposure_list.append(auto_exposure_time)
            exposure_list.append(exposure_time_p)
        elif compensation == 3:
            exposure_time_m = auto_exposure_time / 8
            exposure_time_p = auto_exposure_time * 8
            exposure_list.append(exposure_time_m)  # 曝光时间序列
            exposure_list.append(auto_exposure_time)
            exposure_list.append(exposure_time_p)
        else:  # 默认一档曝光补偿
            exposure_time_m = auto_exposure_time / 2
            exposure_time_p = auto_exposure_time * 2
            exposure_list.append(exposure_time_m)  # 曝光时间序列
            exposure_list.append(auto_exposure_time)
            exposure_list.append(exposure_time_p)
        return exposure_list

    def loadExposureSeq(self, path, file_name):
        """载入曝光序列"""
        images = []
        times = []
        list_path = path + "/List/"
        LDR_path = path + "/LDR/"
        file_path = os.path.join(list_path, file_name)
        with open(file_path) as f:  # 打开txt文件，按行读入到content
            content = f.readlines()
        for line in content:  # 按行读取
            tokens = line.split()  # 存为数组
            images.append(cv.imread(os.path.join(LDR_path, tokens[0])))
            times.append(1 / float(tokens[1]))
        return images, np.asarray(times, dtype=np.float32)

    def writeList(self, path, frame_list, exposure_list):
        """写入txt文件"""
        path = path + "/List/"
        list_name_index = time.strftime("%H%M%S")
        file = list_name_index + '.txt'
        i = len(frame_list)
        f_path = os.path.join(path, file)
        with open(os.path.join(path, file), 'a') as f:
            while i:
                f.write(str(frame_list[3 - i]) + ' ' + str(exposure_list[3 - i]) + '\n')
                i -= 1
            print("writeList 成功 ---")
        return file

    def createHDR(self, cwd, file_name, time_str):
        images, times = self.loadExposureSeq(cwd, file_name)  # 读取图形名称和曝光时间

        alignMTB = cv2.createAlignMTB()  # 对齐图像，创建中值阈值位图
        alignMTB.process(images, images)

        calibrate = cv.createCalibrateDebevec()  # 获得响应曲线
        response = calibrate.process(images, times)

        merge_debevec = cv.createMergeDebevec()  # 合并图像
        hdr = merge_debevec.process(images, times, response)

        tonemap = cv.createTonemap(2.2)  # 映射
        ldr = tonemap.process(hdr)
        merge_mertens = cv.createMergeMertens()
        fusion = merge_mertens.process(images)
        fusion_picture_name = "fusion_{}".format(time_str) + ".png"

        save_path = cwd + "/HDR/" + fusion_picture_name
        cv.imwrite(save_path, fusion * 255)  # 保存图片
        print("HDR创建成功---")

        file = "HDR_list" + '.txt'  # 每生成一张HDR图片，就在HDR_list中插入名字
        HDR_list_path = cwd + "/HDR/" + file
        with open(HDR_list_path, 'a') as f:
            f.write(str(fusion_picture_name) + '\n')


class PhotoScreen(Screen):  # 相册界面类
    cam = None
    clock_event = None
    path = os.getcwd() + "/HDR/"
    hdr_index = 0
    HDR_images = []

    def __init__(self, **kwargs):
        """初始化"""
        super(PhotoScreen, self).__init__(**kwargs)
        with open(os.path.join(self.path, "HDR_list.txt")) as f:  # 打开txt文件，按行读入到content，相册中所有图片的名称
            self.HDR_images = f.readlines()
        print(self.HDR_images)

    def displayHDR(self, index):
        print(self.HDR_images[index])
        self.display_HDR_image = "HDR/" + self.HDR_images[self.hdr_index].strip('\n')  # 更改全局变量，用来更新source
        self.canvas.ask_update()  # 更新显示

    def right(self):
        self.hdr_index += 1  # 索引加1，下一张
        if self.hdr_index > len(self.HDR_images) - 1:
            self.hdr_index = len(self.HDR_images) - 1
        self.displayHDR(self.hdr_index)  # 调用上面的函数更新图片

    def left(self):
        self.hdr_index -= 1
        if self.hdr_index < 0:
            self.hdr_index = 0
        self.displayHDR(self.hdr_index)

    def exit_display(self):  # 离开相册时，把索引调回第一张
        self.hdr_index = 0


class SjnCamera3App(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(CameraScreen(name='camera_screen'))  # 把两个屏幕类添加到ScreenManager
        sm.add_widget(PhotoScreen(name='photo_screen'))
        return sm


if __name__ == '__main__':
    SjnCamera3App().run()