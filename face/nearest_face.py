import pyrealsense2 as rs
import numpy as np
import cv2

def nearestFace(list_dist_obj):
    min_obj =  list_dist_obj[0]
    for i in range(len(list_dist_obj)):
        if list_dist_obj[i][4] < min_obj[4]:
            min_obj = list_dist_obj[i]
    return min_obj


if __name__ == "__main__":
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    pipeline.start(config)

    face_path = "/opt/ros/kinetic/share/OpenCV-3.3.1-dev/haarcascades/haarcascade_frontalface_alt2.xml"
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    face_cascade.load(face_path)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not color_frame or not depth_frame:
                continue
            
            color = np.asanyarray(color_frame.get_data())
            gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            face = face_cascade.detectMultiScale(gray, 1.3, 5)

            list_distance_face = []
            for (x, y, w, h) in face:
                dist = depth_frame.get_distance(x+w//2, y+h//2)
                distance_face = x, y, w, h, dist
                # print distance_face
                list_distance_face += [distance_face]
                cv2.rectangle(color, (x, y), (x+w, y+h), (255, 0, 0), 3)

            list_distance_face = np.array(list_distance_face)
            nearest = nearestFace(list_distance_face)
            cv2.rectangle(color, (nearest[0], nearest[1]), (nearest[0]+nearest[2], nearest[1]+nearest[3]), (0, 255, 0), 3)

            cv2.imshow('', color)
            cv2.waitKey(1)
    finally:
        pipeline.stop()
