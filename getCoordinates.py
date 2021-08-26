import pyrealsense2 as rs
import numpy as np
import cv2


def get_coordinates():
    pc = rs.pointcloud()
    points = rs.points()

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)

    pipe_profile = pipeline.start(config)

    align_to = rs.stream.color
    align = rs.align(align_to)

    n = 0
    while True:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        img_color = np.asanyarray(color_frame.get_data())
        img_depth = np.asanyarray(depth_frame.get_data())

        pc.map_to(color_frame)
        points = pc.calculate(depth_frame)
        vtx = np.asanyarray(points.get_vertices())
        tex = np.asanyarray(points.get_texture_coordinates())
        i = 640 * 340 + 450  # as point（200，200）
        # print('vtx depth: ', [np.float(vtx[i][0]), np.float(vtx[i][1]), np.float(vtx[i][2])])
        cv2.circle(img_color, (340, 450), 8, [255, 0, 255], thickness=-1)
        cv2.putText(img_color, "Dis:" + str(img_depth[340, 450]), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                    [255, 0, 255])
        cv2.putText(img_color, "X:" + str(np.float(vtx[i][0])), (80, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, [255, 0, 255])
        cv2.putText(img_color, "Y:" + str(np.float(vtx[i][1])), (80, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2, [255, 0, 255])
        cv2.putText(img_color, "Z:" + str(np.float(vtx[i][2])), (80, 160), cv2.FONT_HERSHEY_SIMPLEX, 1.2, [255, 0, 255])
        cv2.imshow('depth_frame', img_color)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        # n += 1
        # if n >= 100:
        #     x = np.float(vtx[i][0])
        #     y = np.float(vtx[i][1])
        #     z = np.float(vtx[i][2])
        #     return x, y, z, img_color
get_coordinates()

# x, y, z, img_color = get_coordinates()
# print(x, y, z)
# cv2.imshow('img', img_color)
# cv2.waitKey(1000000)

