import cv2
import numpy as np
import time


class Webcam(object):
    def __init__(self):
        # print ("WebCamEngine init")
        self.dirname = ""  # for nothing, just to make 2 inputs the same
        self.cap = None

    def start(self):
        print("[INFO] Start webcam")
        time.sleep(1)  # wait for camera to be ready
        self.cap = cv2.VideoCapture(0)
        self.valid = False
        try:
            resp = self.cap.read()
            self.shape = resp[1].shape
            self.valid = True
        except:
            self.shape = None

    def get_frame(self):

        if self.valid:
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            start_x = width // 2 - 100
            start_y = height // 2 - 100
            end_x = width // 2 + 100
            end_y = height // 2 + 100

            # Recognize the rectangular area of the ROI
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 255), 3)
            cv2.putText(frame, 'PUT YOUR WRIST HERE', (start_x, start_y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

            height = end_y - start_y
            part_height = height // 3

            roi_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
            square_size = (end_x - start_x) // 4

            # 平均分成三份
            roi_parts = []
            for i in range(1, 4):
            
                square_start_x = end_x - square_size
                square_start_y = start_y + part_height * (i-1)
                cv2.rectangle(frame, (square_start_x, square_start_y), (square_start_x + square_size, square_start_y + square_size), roi_colors[i-1], 2)
                y = start_y + part_height * i
                cv2.line(frame, (start_x, y), (end_x, y), (0, 255, 255), 3)
                roi = frame[square_start_y:square_start_y + square_size, square_start_x:square_start_x + square_size]
                roi_parts.append(roi)

            # # cun_roi, guan_roi, chi_roi = roi_parts
            # # roi_names = ['cun', 'guan', 'chi']
            # roi_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0)]

        else:
            frame = np.ones((480, 640, 3), dtype=np.uint8)
            col = (0, 256, 256)
            cv2.putText(frame, "(Error: Camera not accessible)",
                        (65, 220), cv2.FONT_HERSHEY_PLAIN, 2, col)
        return frame

    def stop(self):
        if self.cap is not None:
            self.cap.release()
            print("[INFO] Stop webcam")

