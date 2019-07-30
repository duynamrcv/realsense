import pyrealsense2 as rs
import numpy as np
import cv2

if __name__ == "__main__":
    pipeline = rs.pipeline()
    config = rs.config()
    
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    profile = pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics

            cv2.circle(color_image, (200, 300), 5, (0, 255, 0), -1)
            
            depth = depth_frame.get_distance(200, 300)
            depth_point_in_meters = rs.rs2_deproject_pixel_to_point(depth_intrin, [200, 300], depth)

            print depth_point_in_meters
            cv2.imshow('color', color_image)

            cv2.waitKey(1)

    finally:
        pipeline.stop()