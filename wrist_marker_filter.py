import numpy as np
import cv2

class markerFilter:

    def colorFilter(img_color, mode="red"):
        # Red color ranges
        if mode == 'red':
            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([10, 255, 255])

            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([180, 255, 255])

            hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)

            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

            img_mask = mask1 + mask2
            result = cv2.bitwise_and(img_color, img_color, mask=img_mask)
        elif mode == 'green':
            lower_green = np.array([25, 120, 70])
            upper_green = np.array([95, 255, 255])

            hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
            img_mask = cv2.inRange(hsv, lower_green, upper_green)
            result = cv2.bitwise_and(img_color, img_color, mask=img_mask)

        return result
    

    def dot_locator(gray_image):
        # Find the non-zero point (tip) in the img
        non_zero_points = cv2.findNonZero(gray_image)

        if non_zero_points is not None:
            # Obtain tip location in the frame
            avg_pos = np.mean(non_zero_points, axis=0)
            x, y = avg_pos[0]
            # print(f"Position of the red point: (x={int(x)}, y={int(y)})")
        else:
            x = None
            y = None
            # print("No red point found in the image")
        return non_zero_points, x, y
    
    def compute_angle(P1, P2, P3, P4):
        # Construct vectors
        v1 = np.subtract(P2, P1)
        v2 = np.subtract(P4, P3)
        
        # Dot product
        dot_product = np.dot(v1, v2)
        
        # Magnitudes of the vectors
        magnitude_v1 = np.linalg.norm(v1)
        magnitude_v2 = np.linalg.norm(v2)
        
        # Angle in radians
        theta = np.arccos(dot_product / (magnitude_v1 * magnitude_v2))
        
        # Convert angle to degrees
        angle_degrees = np.degrees(theta)
        
        return angle_degrees
    
    def extend_line(point1, point2, s):
        direction = np.array(point2) - np.array(point1)
        unit_direction = direction / np.linalg.norm(direction)

        # Calculate new extended endpoints
        new_point1 = point1 - s * unit_direction
        new_point2 = point2 + s * unit_direction
    
        return tuple(map(int, new_point1)), tuple(map(int, new_point2))
    
    
    