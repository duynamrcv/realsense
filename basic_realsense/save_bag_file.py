import pyrealsense2 as rs
import numpy as np
import cv2

if __name__ == "__main__":
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_record_to_file("record.bag")

    pipeline.start(config)
    try:
        while True:
            # wait for frames
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            # convert to numpy array
            depth_img = np.asanyarray(depth_frame.get_data())
            color_img = np.asanyarray(color_frame.get_data())

            # apply colormap
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
                        depth_img, alpha=0.05), cv2.COLORMAP_JET)
            
            # stack
            img_show = np.hstack((color_img, depth_colormap))

            # visualize
            cv2.imshow("", img_show)
            cv2.waitKey(1)
    finally:
        # stop stream
        pipeline.stop()