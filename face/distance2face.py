import pyrealsense2 as rs
import numpy as np
import cv2
import math

def get_angle(face_x, face_y, dist):
    # return angle in x-axis, angle in y-axis, and distance
    ang_x = math.degrees(math.atan2(face_x, dist))
    ang_y = math.degrees(math.atan2(face_y, dist))
    return ang_x, ang_y, dist    

def get_average(range_obj):
    length = len(range_obj)
    obj_x = sum(range_obj[:,0]) / length
    obj_y = sum(range_obj[:,1]) / length
    obj_dist = sum(range_obj[:,2]) / length
    return obj_x, obj_y, obj_dist
    

if __name__ == "__main__":
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    # start config
    pipeline.start(config)

    # using Haar Cascade
    face_path = "/opt/ros/kinetic/share/OpenCV-3.3.1-dev/haarcascades/haarcascade_frontalface_alt.xml"
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    face_cascade.load(face_path)
    
    range_face = []
    count = 0

    try:
        while True:
            # wait for frame
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            # get data 
            color = np.asanyarray(color_frame.get_data())
            gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            depth = np.asanyarray(depth_frame.get_data())

            depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics

            # detect face
            face = face_cascade.detectMultiScale(gray, 1.3, 5)

            for(x, y, w, h) in face:
                cv2.rectangle(color, (x, y), (x+w, y+h), (0, 255, 0), 3)
                face_x = x+w//2
                face_y = y+h//2
                dist = depth_frame.get_distance(face_x, face_y)
                if dist == 0:
                    continue
                
                # convert to depth point in meter
                face_x, face_y, dist = rs.rs2_deproject_pixel_to_point(depth_intrin, [face_x, face_y], dist)
                result = get_angle(face_x, face_y, dist)
                range_face += [result]
                count += 1

            if count >= 20: # get data from 20 face detected
                break

            cv2.imshow('', color)
            cv2.waitKey(1)
    
    finally:
        pipeline.stop()

    range_face = np.array(range_face)
    result = get_average(range_face)
    print result
