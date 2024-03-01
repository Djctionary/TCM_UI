import cv2
import numpy as np
import time
from scipy import signal
from signal_processing import Signal_processing

def wrist_detect(img):

    height, width, _ = img.shape
    start_x = width // 2 - 100
    start_y = height // 2 - 100
    end_x = width // 2 + 100
    end_y = height // 2 + 100

    # Recognize the rectangular area of the ROI
    # cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (0, 255, 255), 3)
    cv2.putText(img, 'PUT YOUR WRIST HERE', (start_x, start_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    height = end_y - start_y
    part_height = height // 3

    roi_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
    square_size = (end_x - start_x) // 4

    # 平均分成三份
    roi_parts = []
    for i in range(1, 4):
       
        square_start_x = end_x - square_size
        square_start_y = start_y + part_height * (i-1)
        cv2.rectangle(img, (square_start_x, square_start_y), (square_start_x + square_size, square_start_y + square_size), roi_colors[i-1], 2)
        y = start_y + part_height * i
        cv2.line(img, (start_x, y), (end_x, y), (0, 255, 255), 3)
        roi = img[square_start_y:square_start_y + square_size, square_start_x:square_start_x + square_size]
        roi_parts.append(roi)

    cun_roi, guan_roi, chi_roi = roi_parts
    roi_names = ['cun', 'guan', 'chi']


    for i, img_roi in enumerate([cun_roi, guan_roi, chi_roi]):
        # Color space conversion
        img_HSV = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)
        HSV_mask = cv2.inRange(img_HSV, (0, 15, 0), (17,170,255))
        HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
        img_YCrCb = cv2.cvtColor(img_roi, cv2.COLOR_BGR2YCrCb)
        YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255,180,135))
        YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

        # Merge
        global_mask=cv2.bitwise_and(YCrCb_mask,HSV_mask)
        global_mask=cv2.medianBlur(global_mask,3)
        global_mask = cv2.morphologyEx(global_mask, cv2.MORPH_OPEN, np.ones((4,4), np.uint8))

        # Find the largest contour
        contours, _ = cv2.findContours(global_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ROI = img_roi
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            contour_mask = np.zeros_like(global_mask)
            cv2.drawContours(contour_mask, [max_contour], -1, (255), thickness=cv2.FILLED)
            ROI = cv2.bitwise_and(img_roi, img_roi, mask=contour_mask)

        cv2.rectangle(img, (start_x, start_y + part_height * i), (end_x, start_y + part_height * (i + 1)), roi_colors[i], 3)
        
        # cv2.imshow(roi_names[i], ROI)

    return cun_roi, guan_roi, chi_roi

class Process(object):
    def __init__(self):
        self.frame_in = np.zeros((10, 10, 3), np.uint8)
        self.frame_ROI = np.zeros((10, 10, 3), np.uint8)
        self.frame_out = np.zeros((10, 10, 3), np.uint8)
        self.samples = []
        self.buffer_size = 100
        self.times = [] 
        self.data_buffer = []
        self.fps = 0
        self.fft = []
        self.freqs = []
        self.t0 = time.time()
        self.bpm = 0
        self.bpms = []
        self.peaks = []
        self.sp = Signal_processing()

    def extractColor(self, frame):
        
        #r = np.mean(frame[:,:,0])
        g = np.mean(frame[:,:,1])
        #b = np.mean(frame[:,:,2])
        #return r, g, b
        return g


    def run(self,ROIs):
        frame = self.frame_in

        green_val = self.sp.extract_color(ROIs)                                                                         # 使用了Signal_processing类的方法
        # 从ROIS中提取绿色平均值

        self.frame_out = frame# 将当前输入帧（frame）赋值给输出帧（self.frame_out），用于显示和保存。

        L = len(self.data_buffer)   # data_buffer是一个列表，用于存储绿色平均值的

        g = green_val # 从ROIS中提取绿色平均值（简写）
        
        if(abs(g-np.mean(self.data_buffer))>10 and L>99): # 删除突然变化，如果avg值变化超过10，则使用data_buffer的平均值
            g = self.data_buffer[-1]
        
        self.times.append(time.time() - self.t0)

        #把g添加到data_buffer里去
        self.data_buffer.append(g) # 将从绿色通道提取的平均值（g）添加到数据缓冲区列表中

############################################# 后面的就是利用data_buffer数据来测心率和一系列处理了###################################################

        #只能在固定大小的缓冲区中处理
        if L > self.buffer_size:
            self.data_buffer = self.data_buffer[-self.buffer_size:]
            self.times = self.times[-self.buffer_size:]
            self.bpms = self.bpms[-self.buffer_size//2:]
            L = self.buffer_size
            
        processed = np.array(self.data_buffer)
        
        # start calculating after the first 10 frames
        if L == self.buffer_size:
            
            self.fps = float(L) / (self.times[-1] - self.times[0])#使用计算机处理器的真实fps计算HR，而不是相机提供的fps
            even_times = np.linspace(self.times[0], self.times[-1], L)
            
            processed = signal.detrend(processed)#消除信号的趋势，避免光变化的干扰
            interpolated = np.interp(even_times, self.times, processed) #interpolation by 1
            interpolated = np.hamming(L) * interpolated#使信号更具周期性(避免频谱泄漏)
            #norm = (interpolated - np.mean(interpolated))/np.std(interpolated)#normalization
            norm = interpolated/np.linalg.norm(interpolated)
            raw = np.fft.rfft(norm*30)#do real fft with the normalization multiplied by 10
            
            self.freqs = float(self.fps) / L * np.arange(L / 2 + 1)
            freqs = 60. * self.freqs

            self.fft = np.abs(raw)**2#get amplitude spectrum
        
            idx = np.where((freqs > 50) & (freqs < 180))#the range of frequency that HR is supposed to be within 
            pruned = self.fft[idx]
            pfreq = freqs[idx]
            
            self.freqs = pfreq 
            self.fft = pruned
            
            idx2 = np.argmax(pruned)#max in the range can be HR
            
            self.bpm = self.freqs[idx2]
            self.bpms.append(self.bpm)
            
            processed = self.butter_bandpass_filter(processed,0.8,3,self.fps,order = 3)                   # 调用了Process类中的butter_bandpass_filter方法
            #ifft = np.fft.irfft(raw)
        self.samples = processed # multiply the signal with 5 for easier to see in the plot
        #TODO: find peaks to draw HR-like signal.

        return True
    
    def reset(self):
        self.frame_in = np.zeros((10, 10, 3), np.uint8)
        #self.frame_ROI = np.zeros((10, 10, 3), np.uint8)
        self.frame_out = np.zeros((10, 10, 3), np.uint8)
        self.samples = []
        self.times = [] 
        self.data_buffer = []
        self.fps = 0
        self.fft = []
        self.freqs = []
        self.t0 = time.time()
        #心率
        self.bpm = 0
        self.bpms = []
        
    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = signal.lfilter(b, a, data)
        return y 
