import pyrealsense2 as rs
import numpy as np
import cv2

if __name__ == "__main__":
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16,  30)

    pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()

            if not depth:
                continue

            depth_img = np.asanyarray(depth.get_data())
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_img, alpha=0.03), cv2.COLORMAP_JET)

            img = np.array(depth_colormap)

            cv2.circle(img, (320, 240), 5, (0, 0, 255), -1)
            dist = depth.get_distance(320, 240)
            print(dist)


            cv2.imshow("", img)
            cv2.waitKey(1)
    
    finally:
        pipeline.stop()