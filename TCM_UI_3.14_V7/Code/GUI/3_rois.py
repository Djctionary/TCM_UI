import cv2
import numpy as np

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
        
        cv2.imshow(roi_names[i], ROI)

    return cun_roi, guan_roi, chi_roi

# test
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if ret:
        ROI = wrist_detect(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break