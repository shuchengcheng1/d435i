import cv2
from realsense_depth import *

font = cv2.FONT_HERSHEY_SIMPLEX
# lower_green = np.array([35, 110, 106])  # 绿色范围低阈值
lower_green = np.array([35, 110, 106])  # 绿色范围低阈值
upper_green = np.array([78, 255, 255])  # 绿色范围高阈值

# lower_red = np.array([0, 127, 128])  # 红色范围低阈值
lower_red = np.array([150, 127, 128])  # 红色范围低阈值
upper_red = np.array([180, 255, 255])  # 红色范围高阈值

lower_yellow = np.array([22, 43, 46])  # 黄色范围低阈值
upper_yellow = np.array([34, 255, 255])  # 黄色范围高阈值

lower_blue = np.array([95, 43, 46])  # 蓝色范围低阈值
upper_blue = np.array([125, 255, 255])  # 蓝色范围高阈值

# 需要更多颜色，可以去百度一下HSV阈值！


def getColorAll(color_frame):
    colorList = []
    hsv_img = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)
    mask_green = cv2.inRange(hsv_img, lower_green, upper_green)  # 根据颜色范围删选
    mask_red = cv2.inRange(hsv_img, lower_red, upper_red)
    mask_yellow = cv2.inRange(hsv_img, lower_yellow, upper_yellow)  # 根据颜色范围删选
    mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)
    # 根据颜色范围删选
    mask_green = cv2.medianBlur(mask_green, 7)  # 中值滤波
    mask_red = cv2.medianBlur(mask_red, 7)  # 中值滤波
    mask_yellow = cv2.medianBlur(mask_yellow, 7)  # 中值滤波
    mask_blue = cv2.medianBlur(mask_blue, 7)  # 中值滤波
    mask = cv2.bitwise_or(mask_green, mask_red)
    contours_green, hierarchy_green = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_red, hierarchy_red = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_yellow, hierarchy_yellow = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours_blue, hierarchy_blue = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if contours_green:
        (x1, y1, w1, h1) = cv2.boundingRect(contours_green[0])
        cv2.rectangle(color_frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 255), 1)
        cv2.putText(color_frame, "Green", (x1, y1 - 5), font, 0.7, (0, 255, 0), 1)
        colorList.append('Green')

    if contours_red:
        (x2, y2, w2, h2) = cv2.boundingRect(contours_red[0])
        cv2.rectangle(color_frame, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 255), 1)
        cv2.putText(color_frame, "Red", (x2, y2 - 5), font, 0.7, (0, 0, 255), 1)
        colorList.append('Red')

    if contours_yellow:
        (x3, y3, w3, h3) = cv2.boundingRect(contours_yellow[0])
        cv2.rectangle(color_frame, (x3, y3), (x3 + w3, y3 + h3), (0, 255, 255), 1)
        cv2.putText(color_frame, "Yellow", (x3, y3 - 5), font, 0.7, (0, 255, 255), 1)
        colorList.append('Yellow')

    if contours_blue:
        (x4, y4, w4, h4) = cv2.boundingRect(contours_blue[0])
        cv2.rectangle(color_frame, (x4, y4), (x4 + w4, y4 + h4), (0, 255, 255), 1)
        cv2.putText(color_frame, "Blue", (x4, y4 - 5), font, 0.7, (255, 0, 0), 1)
        colorList.append('Blue')

    return colorList, color_frame





def d435i_camera():
    dc = DepthCamera()
    num = 0
    while True:
        ret, depth_frame, color_frame = dc.get_frame()  # 读取深度相机彩色图和深度图
        color, img = getColorAll(color_frame)
        num += 1
        if color and num > 50:
            return color, img



if __name__ == '__main__':
    print("123")
    # color, img = d435i_camera()
    # print('color', color)
    # # 显示图片
    # cv2.imshow('img', img)
    # cv2.waitKey(200)





