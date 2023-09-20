import numpy as np
import time
import cv2
import pyrealsense2 as rs
from wrist_marker_filter import markerFilter as mf


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(cali_pts) < 4:
            cali_pts.append((x, y))
        else:
            if len(wrist_pts) < 3:
                wrist_pts.append((x, y))
        print(x,y)
        # print(wrist_pts[-1])


cali_pts = []
wrist_pts = []
# Setup Realsense Pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# Start video streaming
pipeline.start(config)
init = True
img_init = True


try:
    while True:
        while img_init:
            frames = pipeline.wait_for_frames()

            color_frame = frames.get_color_frame()
            if not color_frame:
                    continue
            
            print("Prespective Transformation Init")
            color_img = np.asanyarray(color_frame.get_data())

            cv2.namedWindow("manual_calibration")
            cv2.setMouseCallback("manual_calibration", click_event)
            cv2.imshow("manual_calibration", color_img)
            cv2.waitKey(0)
            if (len(cali_pts) == 4):
                    cv2.destroyAllWindows()
                    height, width = color_img.shape[:2]
                  
                    i, j = 100, 100
                    dst_pts = np.array([
                        [0+i, 0+j],
                        [400+i, 0+j],
                        [400+i, 300+j],
                        [0+i, 300+j]
                    ], dtype='float32')
                
                    M = cv2.getPerspectiveTransform(np.array(cali_pts, dtype='float32'), dst_pts)
                    img_init = False

            img_warpped = cv2.warpPerspective(color_img, M, (width, height))
            print('Pixel to Real Scaling Init')
            cv2.namedWindow("scaling_finder")
            cv2.setMouseCallback("scaling_finder", click_event)
            cv2.imshow("scaling_finder", img_warpped)
            cv2.waitKey(0)
            if (len(wrist_pts) == 3):
                cv2.destroyAllWindows()
                distance_pixel = np.sqrt((wrist_pts[1][0] - wrist_pts[0][0])**2 + (wrist_pts[1][1] - wrist_pts[0][1])**2)
                p2r_scale = 2.0/distance_pixel
                print(f"Current Pixel Distance is: {distance_pixel}")
                print(f"Pixel to Real Scaling is: {p2r_scale}")

        frames = pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()
        # frame to np array as image
        color_img1 = np.asanyarray(color_frame.get_data())
        time0 = time.time() # pre processing time
        color_img = cv2.warpPerspective(color_img1, M, (width, height))
        # apply color filter
        filtered_img_red = mf.colorFilter(color_img, 'red')
        filtered_img_green = mf.colorFilter(color_img, 'green')

        # convert to grayscale pic
        img_gray_red = cv2.cvtColor(filtered_img_red, cv2.COLOR_BGR2GRAY)
        img_gray_green = cv2.cvtColor(filtered_img_green, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.bitwise_or(img_gray_red, img_gray_green)
   
        none_zero_points, xr, yr = mf.dot_locator(img_gray_red)
        _, xg, yg = mf.dot_locator(img_gray_green)
  
        alpha =mf.compute_angle(wrist_pts[1], wrist_pts[2], (xr, yr), (xg, yg))
        # print(alpha)

        if init:
            cv2.imshow('Robot Tip Locator', img_gray)
            init = False
        if none_zero_points is not None:
            bend_angle = -(90 - alpha)
            coordinates_text = f"theta={bend_angle}"
            cv2.circle(img_gray, (int(xr), int(yr)), 10, (255, 255, 255), 1)
            cv2.circle(img_gray, (int(xg), int(yg)), 10, (255, 255, 255), 1)
            cv2.line(img_gray, (int(xr), int(yr)), (int(xg), int(yg)), (255,0,0), 1)
            cv2.putText(img_gray, coordinates_text, (int(xr) - 0, int(yr) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            wrist1, wrist_base = mf.extend_line(wrist_pts[1], wrist_pts[2], 200)
            cv2.line(img_gray, wrist1, wrist_base,(255, 0, 0), 1)

            cv2.imshow('Robot Tip Locator', img_gray)
        
        time1 = time.time()
        print(time1-time0)
            
        if cv2.waitKey(1) & 0xFF == 27:
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()