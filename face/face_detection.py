import pyrealsense2 as rs
import numpy as np
import cv2

if __name__ == "__main__":
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)

    face_path = "/opt/ros/kinetic/share/OpenCV-3.3.1-dev/haarcascades/haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_cascade.load(face_path)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            
            color = np.asanyarray(color_frame.get_data())
            gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

            face = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in face:
                cv2.rectangle(color, (x, y), (x+w, y+h), (0, 255, 0), 3)
            
            cv2.imshow('', color)
            cv2.waitKey(1)
    finally:
        pipeline.stop()
