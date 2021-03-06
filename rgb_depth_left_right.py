import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()

config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)  # 10、15或者30可选,20或者25会报错，其他帧率未尝试
config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 15)
config.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 15)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)

profile = pipeline.start(config)

# 获取深度传感器的深度刻度 Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: ", depth_scale)

clipping_distance_in_meters = 1  # 1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Create an align object
# Rs.align允许我们对深度帧和其他帧进行对齐 rs.align allows us to perform alignment of depth frames to others frames
# "align_to"是我们计划对齐深度帧的流类型 The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

try:
    while True:
        frames = pipeline.wait_for_frames()

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)
        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
        if not aligned_depth_frame:
            continue
        depth_frame = np.asanyarray(aligned_depth_frame.get_data())
        # 将深度图转化为伪彩色图方便观看
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame, alpha=0.03), cv2.COLORMAP_JET)
        cv2.imshow('1 depth', depth_colormap)

        # color frames
        color_frame = aligned_frames.get_color_frame()
        if not color_frame:
            continue
        color_frame = np.asanyarray(color_frame.get_data())
        cv2.imshow('2 color', color_frame)

        # left　frames
        left_frame = frames.get_infrared_frame(1)
        if not left_frame:
            continue
        left_frame = np.asanyarray(left_frame.get_data())
        cv2.imshow('3 left_frame', left_frame)

        # right frames
        right_frame = frames.get_infrared_frame(2)
        if not right_frame:
            continue
        right_frame = np.asanyarray(right_frame.get_data())
        cv2.imshow('4 right_frame', right_frame)

        c = cv2.waitKey(1)

        # 如果按下ESC则关闭窗口（ESC的ascii码为27），同时跳出循环
        if c == 27:
            cv2.destroyAllWindows()
            break

finally:
    # Stop streaming
    pipeline.stop()

# 深度图上色参考https://github.com/IntelRealSense/librealsense/blob/jupyter/notebooks/distance_to_object.ipynb
# 对齐参考：https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/align-depth2color.py
# 左右图获取参考https://blog.csdn.net/Hanghang_/article/details/102489762
# 其他参考https://blog.csdn.net/Dontla/article/details/102701680
