import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtGui import QPalette, QBrush, QColor
from PyQt5.QtWidgets import QPushButton, QApplication, QComboBox, QLabel, QFileDialog, QStatusBar, QDesktopWidget, \
    QMessageBox, QMainWindow
import pyqtgraph as pg
import sys
from process import *
from webcam import Webcam
from video import Video
from interface import waitKey, plotXY


class GUI(QMainWindow, QThread):
    def __init__(self):
        super(GUI, self).__init__()
        self.initUI()
        self.webcam = Webcam()
        self.video = Video()
        self.input = self.webcam
        self.dirname = ""
        print("Input: webcam")
        self.statusBar.showMessage("Input: webcam", 5000)
        self.btnOpen.setEnabled(False)
        self.process = Process()
        self.status = False
        self.frame = np.zeros((10, 10, 3), np.uint8)
        # self.plot = np.zeros((10,10,3),np.uint8)
        self.bpm = 0
        self.terminate = False


    def initUI(self):

        # set font 字体
        font = QFont()
        font.setPointSize(16)

        # background
        # window_size = self.size()
        pixmap = QPixmap("bk.png")
        pixmap = pixmap.scaled(1880, 1056)
        brush = QBrush(pixmap)
        brush.setColor(QColor(255, 255, 255, 200))
        brush.setStyle(Qt.TexturePattern)
        palette = QPalette()
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)

        # widgets 按钮
        self.btnStart = QPushButton("Start", self)
        self.btnStart.move(440, 420)
        self.btnStart.setFixedWidth(200)
        self.btnStart.setFixedHeight(50)
        self.btnStart.setFont(font)
        self.btnStart.clicked.connect(self.run)

        self.btnOpen = QPushButton("Open", self)
        self.btnOpen.move(230, 420)
        self.btnOpen.setFixedWidth(200)
        self.btnOpen.setFixedHeight(50)
        self.btnOpen.setFont(font)
        self.btnOpen.clicked.connect(self.openFileDialog)

        self.cbbInput = QComboBox(self)
        self.cbbInput.addItem("Webcam")
        self.cbbInput.addItem("Video")
        self.cbbInput.setCurrentIndex(0)
        self.cbbInput.setFixedWidth(200)
        self.cbbInput.setFixedHeight(50)
        self.cbbInput.move(20, 420)
        self.cbbInput.setFont(font)
        self.cbbInput.activated.connect(self.selectInput)
        # -------------------

        # 创建字体对象
        font = QFont("Comic Sans MS", 15, QFont.Bold)

        # 设置标签
        self.lblDisplay = QLabel(self)  # label to show frame from camera 用于显示摄像头帧的标签
        self.lblDisplay.setGeometry(0, 0, 640, 350)
        self.lblDisplay.setStyleSheet("background-color: #000000")

        self.lblROI1 = QLabel(self)  # label to show face with ROIs 用于显示带有ROI的人脸的标签
        self.lblROI1.setGeometry(1200, 200, 50, 50)
        self.lblROI1.setStyleSheet("background-color: #000000")

        self.lblROI2 = QLabel(self)  # label to show face with ROIs 用于显示带有ROI的人脸的标签
        self.lblROI2.setGeometry(1200, 650, 50, 50)
        self.lblROI2.setStyleSheet("background-color: #000000")

        self.lblROI3 = QLabel(self)  # label to show face with ROIs 用于显示带有ROI的人脸的标签
        self.lblROI3.setGeometry(0, 650, 50, 50)
        self.lblROI3.setStyleSheet("background-color: #000000")

        self.lblHR_1 = QLabel(self)  # label to show HR change over time 用于显示随时间变化的心率的标签
        self.lblHR_1.setGeometry(1000, 350, 300, 40)
        self.lblHR_1.setFont(font)
        self.lblHR_1.setText("Frequency: ")

        self.lblHR2_1 = QLabel(self)  # label to show stable HR 用于显示稳定心率的标签
        self.lblHR2_1.setGeometry(1000, 400, 300, 40)
        self.lblHR2_1.setFont(font)
        self.lblHR2_1.setText("Heart rate: ")

        self.lblHR_2 = QLabel(self)  # label to show HR change over time 用于显示随时间变化的心率的标签
        self.lblHR_2.setGeometry(1000, 850, 300, 40)
        self.lblHR_2.setFont(font)
        self.lblHR_2.setText("Frequency: ")

        self.lblHR2_2 = QLabel(self)  # label to show stable HR 用于显示稳定心率的标签
        self.lblHR2_2.setGeometry(1000, 900, 300, 40)
        self.lblHR2_2.setFont(font)
        self.lblHR2_2.setText("Heart rate: ")

        self.lblHR_3 = QLabel(self)  # label to show HR change over time 用于显示随时间变化的心率的标签
        self.lblHR_3.setGeometry(0, 850, 300, 40)
        self.lblHR_3.setFont(font)
        self.lblHR_3.setText("Frequency: ")

        self.lblHR2_3 = QLabel(self)  # label to show stable HR 用于显示稳定心率的标签
        self.lblHR2_3.setGeometry(0, 900, 300, 40)
        self.lblHR2_3.setFont(font)
        self.lblHR2_3.setText("Heart rate: ")

        # dynamic plot 动态绘图
        self.signal_Plt1 = pg.PlotWidget(self)
        self.signal_Plt1.move(1350, 0)
        self.signal_Plt1.resize(480, 192)
        self.signal_Plt1.setLabel('bottom', "寸Signal")
        self.signal_Plt1.setBackground((0, 0, 0, 0))  # 设置背景为透明
        

        self.fft_Plt1 = pg.PlotWidget(self)
        self.fft_Plt1.move(1350, 200)
        self.fft_Plt1.resize(480, 192)
        self.fft_Plt1.setLabel('bottom', "寸FFT")
        self.fft_Plt1.setBackground((0, 0, 0, 0))  # 设置背景为透明

        self.signal_Plt2 = pg.PlotWidget(self)
        self.signal_Plt2.move(1350, 570)
        self.signal_Plt2.resize(480, 192)
        self.signal_Plt2.setLabel('bottom', "关Signal")
        self.signal_Plt2.setBackground((0, 0, 0, 0))  # 设置背景为透明

        self.fft_Plt2 = pg.PlotWidget(self)
        self.fft_Plt2.move(1350, 770)
        self.fft_Plt2.resize(480, 192)
        self.fft_Plt2.setLabel('bottom', "关FFT")
        self.fft_Plt2.setBackground((0, 0, 0, 0))  # 设置背景为透明

        self.signal_Plt3 = pg.PlotWidget(self)
        self.signal_Plt3.move(350, 570)
        self.signal_Plt3.resize(480, 192)
        self.signal_Plt3.setLabel('bottom', "尺Signal")
        self.signal_Plt3.setBackground((0, 0, 0, 0))  # 设置背景为透明

        self.fft_Plt3 = pg.PlotWidget(self)
        self.fft_Plt3.move(350, 770)
        self.fft_Plt3.resize(480, 192)
        self.fft_Plt3.setLabel('bottom', "尺FFT")
        self.fft_Plt3.setBackground((0, 0, 0, 0))  # 设置背景为透明






        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(200)

        self.statusBar = QStatusBar()
        self.statusBar.setFont(font)
        self.setStatusBar(self.statusBar)

        # config main window 配置主窗口
        self.setGeometry(100, 50, 1880, 1056)#1740,960/2088,1152/1914,1056
        # self.center()
        self.setWindowTitle("Heart rate monitor")
        self.show()

    # 初始化用户界面

    def update(self):
        self.signal_Plt1.clear()
        self.signal_Plt1.plot(self.process.samples[20:], pen='g')

        self.fft_Plt1.clear()
        self.fft_Plt1.plot(np.column_stack((self.process.freqs, self.process.fft)), pen='g')

        self.signal_Plt2.clear()
        self.signal_Plt2.plot(self.process.samples[20:], pen='g')

        self.fft_Plt2.clear()
        self.fft_Plt2.plot(np.column_stack((self.process.freqs, self.process.fft)), pen='g')

        self.signal_Plt3.clear()
        self.signal_Plt3.plot(self.process.samples[20:], pen='g')

        self.fft_Plt3.clear()
        self.fft_Plt3.plot(np.column_stack((self.process.freqs, self.process.fft)), pen='g')
    # 更新绘图数据，清除原有数据并绘制新数据。

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    # 窗口居中显示

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Message", "Are you sure want to quit",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
            self.input.stop()
            # cv2.destroyAllWindows()
            self.terminate = True
            sys.exit()

        else:
            event.ignore()
    # 处理关闭事件，弹出确认对话框并根据用户选择执行相应操作。

    def selectInput(self):
        self.reset()
        if self.cbbInput.currentIndex() == 0:
            self.input = self.webcam
            print("Input: webcam")
            self.btnOpen.setEnabled(False)
            # self.statusBar.showMessage("Input: webcam",5000)
        elif self.cbbInput.currentIndex() == 1:
            self.input = self.video
            print("Input: video")
            self.btnOpen.setEnabled(True)
            # self.statusBar.showMessage("Input: video",5000)
    # 根据下拉框选择的输入源重置界面并更新相应设置。

    def key_handler(self):
        """
        cv2 window must be focused for keypresses to be detected.
        """
        self.pressed = waitKey(1) & 255  # wait for keypress for 10 ms
        if self.pressed == 27:  # exit program on 'esc'
            print("[INFO] Exiting")
            self.webcam.stop()
            sys.exit()
    # 摁esc退出

    def openFileDialog(self):
        self.dirname = QFileDialog.getOpenFileName(self, 'OpenFile')
        # self.statusBar.showMessage("File name: " + self.dirname,5000)
    # 打开文件对话框

    def reset(self):
        self.process.reset()
        self.lblDisplay.clear()
        self.lblDisplay.setStyleSheet("background-color: #000000")

    # 重置界面
    def ROI(self):
        frame = self.input.get_frame()
        ROI1, ROI2, ROI3 = wrist_detect(frame)
        return ROI1, ROI2, ROI3

    def main_loop1(self,ROI):
        frame = self.input.get_frame()
        
        self.process.frame_in = frame
        if self.terminate == False:
            ret = self.process.run(ROI)####################

        # cv2.imshow("Processed", frame)
        if ret == True:
            self.frame = self.process.frame_out  # get the frame to show in GUI
            # self.f_fr = self.process.frame_ROI #get the face to show in GUI
            self.f_fr = ROI
            # print(self.f_fr.shape)
            self.bpm = self.process.bpm  # get the bpm change over the time
        else:
            self.frame = frame
            self.f_fr = np.zeros((10, 10, 3), np.uint8)
            self.bpm = 0

        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
        cv2.putText(self.frame, "FPS " + str(float("{:.2f}".format(self.process.fps))),
                    (20, 460), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 2)
        img = QImage(self.frame, self.frame.shape[1], self.frame.shape[0],
                     self.frame.strides[0], QImage.Format_RGB888)
        self.lblDisplay.setPixmap(QPixmap.fromImage(img))

        # 改这里 ################################

        self.f_fr = cv2.cvtColor(self.f_fr, cv2.COLOR_RGB2BGR)
        # self.lblROI.setGeometry(660,10,self.f_fr.shape[1],self.f_fr.shape[0])
        self.f_fr = np.transpose(self.f_fr, (0, 1, 2)).copy()
        f_img = QImage(self.f_fr, self.f_fr.shape[1], self.f_fr.shape[0],
                       self.f_fr.strides[0], QImage.Format_RGB888)
        self.lblROI1.setPixmap(QPixmap.fromImage(f_img))

        self.lblHR_1.setText("Freq: " + str(float("{:.2f}".format(self.bpm))))

        if self.process.bpms.__len__() > 50:
            if (max(self.process.bpms - np.mean(
                    self.process.bpms)) < 5):  # show HR if it is stable -the change is not over 5 bpm- for 3s
                self.lblHR2_1.setText("Heart rate: " + str(float("{:.2f}".format(np.mean(self.process.bpms)))) + " bpm")

        # self.make_bpm_plot()#need to open a cv2.imshow() window to handle a pause
        # QtTest.QTest.qWait(10)#wait for the GUI to respond
        self.key_handler()  # if not the GUI cant show anything

    def main_loop2(self, ROI):
        frame = self.input.get_frame()

        self.process.frame_in = frame
        if self.terminate == False:
            ret = self.process.run(ROI)  ####################

        # cv2.imshow("Processed", frame)
        if ret == True:
            self.frame = self.process.frame_out  # get the frame to show in GUI
            # self.f_fr = self.process.frame_ROI #get the face to show in GUI
            self.f_fr = ROI
            # print(self.f_fr.shape)
            self.bpm = self.process.bpm  # get the bpm change over the time
        else:
            self.frame = frame
            self.f_fr = np.zeros((10, 10, 3), np.uint8)
            self.bpm = 0

        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
        cv2.putText(self.frame, "FPS " + str(float("{:.2f}".format(self.process.fps))),
                    (20, 460), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 2)
        img = QImage(self.frame, self.frame.shape[1], self.frame.shape[0],
                     self.frame.strides[0], QImage.Format_RGB888)
        self.lblDisplay.setPixmap(QPixmap.fromImage(img))

        # 改这里 ################################

        self.f_fr = cv2.cvtColor(self.f_fr, cv2.COLOR_RGB2BGR)
        # self.lblROI.setGeometry(660,10,self.f_fr.shape[1],self.f_fr.shape[0])
        self.f_fr = np.transpose(self.f_fr, (0, 1, 2)).copy()
        f_img = QImage(self.f_fr, self.f_fr.shape[1], self.f_fr.shape[0],
                       self.f_fr.strides[0], QImage.Format_RGB888)
        self.lblROI2.setPixmap(QPixmap.fromImage(f_img))

        self.lblHR_2.setText("Freq: " + str(float("{:.2f}".format(self.bpm))))

        if self.process.bpms.__len__() > 50:
            if (max(self.process.bpms - np.mean(
                    self.process.bpms)) < 5):  # show HR if it is stable -the change is not over 5 bpm- for 3s
                self.lblHR2_2.setText("Heart rate: " + str(float("{:.2f}".format(np.mean(self.process.bpms)))) + " bpm")

        # self.make_bpm_plot()#need to open a cv2.imshow() window to handle a pause
        # QtTest.QTest.qWait(10)#wait for the GUI to respond
        self.key_handler()  # if not the GUI cant show anything

    def main_loop3(self, ROI):
        frame = self.input.get_frame()

        self.process.frame_in = frame
        if self.terminate == False:
            ret = self.process.run(ROI)  ####################

        # cv2.imshow("Processed", frame)
        if ret == True:
            self.frame = self.process.frame_out  # get the frame to show in GUI
            # self.f_fr = self.process.frame_ROI #get the face to show in GUI
            self.f_fr = ROI
            # print(self.f_fr.shape)
            self.bpm = self.process.bpm  # get the bpm change over the time
        else:
            self.frame = frame
            self.f_fr = np.zeros((10, 10, 3), np.uint8)
            self.bpm = 0

        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
        cv2.putText(self.frame, "FPS " + str(float("{:.2f}".format(self.process.fps))),
                    (20, 460), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 2)
        img = QImage(self.frame, self.frame.shape[1], self.frame.shape[0],
                     self.frame.strides[0], QImage.Format_RGB888)
        self.lblDisplay.setPixmap(QPixmap.fromImage(img))

        # 改这里 ################################

        self.f_fr = cv2.cvtColor(self.f_fr, cv2.COLOR_RGB2BGR)
        # self.lblROI.setGeometry(660,10,self.f_fr.shape[1],self.f_fr.shape[0])
        self.f_fr = np.transpose(self.f_fr, (0, 1, 2)).copy()
        f_img = QImage(self.f_fr, self.f_fr.shape[1], self.f_fr.shape[0],
                       self.f_fr.strides[0], QImage.Format_RGB888)
        self.lblROI3.setPixmap(QPixmap.fromImage(f_img))

        self.lblHR_3.setText("Freq: " + str(float("{:.2f}".format(self.bpm))))

        if self.process.bpms.__len__() > 50:
            if (max(self.process.bpms - np.mean(
                    self.process.bpms)) < 5):  # show HR if it is stable -the change is not over 5 bpm- for 3s
                self.lblHR2_3.setText("Heart rate: " + str(float("{:.2f}".format(np.mean(self.process.bpms)))) + " bpm")

        # self.make_bpm_plot()#need to open a cv2.imshow() window to handle a pause
        # QtTest.QTest.qWait(10)#wait for the GUI to respond
        self.key_handler()  # if not the GUI cant show anything

    def run(self, input):
        print("run")
        self.reset()
        input = self.input
        self.input.dirname = self.dirname
        if self.input.dirname == "" and self.input == self.video:
            print("choose a video first")
            # self.statusBar.showMessage("choose a video first",5000)
            return
        if self.status == False:
            self.status = True
            input.start()
            self.btnStart.setText("Stop")
            self.cbbInput.setEnabled(False)
            self.btnOpen.setEnabled(False)
            self.lblHR2_1.clear()
            self.lblHR2_2.clear()
            self.lblHR2_3.clear()
            while self.status == True:
                ROI1, ROI2, ROI3=self.ROI()
                self.main_loop1(ROI1)
                self.main_loop2(ROI2)
                self.main_loop3(ROI3)



        elif self.status == True:
            self.status = False
            input.stop()
            self.btnStart.setText("Start")
            self.cbbInput.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
