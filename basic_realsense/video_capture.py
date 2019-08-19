import pyrealsense2 as rs
import cv2
import numpy as np

if __name__ == "__main__":
    # config depth and color
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # stream
    pipeline.start(config)

    try:
        while True:
            # wait for frames
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            
            # convert to numpy
            depth_img = np.asanyarray(depth_frame.get_data())
            color_img = np.asanyarray(color_frame.get_data())

            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_img,
                                                alpha=0.03), cv2.COLORMAP_JET)

            img = np.hstack((color_img, depth_colormap))
            
            cv2.imshow('realsense', img)
            cv2.waitKey(1)

    finally:
        pipeline.stop()

