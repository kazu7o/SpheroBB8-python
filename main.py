#!/usr/bin/env python
from bluepy import btle
import BB8_simple
import readchar
import sys
import camera
import cv2
import math

# BB8 Controller
#bb8 = BB8_simple.BB8Controller()

# 
def get_degrees(ball_x, ball_y, bb8_x, bb8_y):
    radian = math.atan2(ball_y - bb8_y, ball_x - bb8_x)
    return math.degrees(radian)


# Main Process
if __name__ == '__main__':
    cap = cv2.VideoCapture("http://127.0.0.1:8081/")
    # ESCキーが押されるまで検出
    while cv2.waitKey(10) != 27:
        frame = cap.read()[1]
        rects = camera.getBall(frame)
        bb8_rects = camera.getBB8(frame)

        # 検出された矩形の中から最大のものだけ描画
        if len(rects) > 0 and len(bb8_rects) > 0:
            # 第2引数で指定した関数は矩形の面積を求めている
            rect = max(rects, key=(lambda x: x[2] * x[3]))
            bb8_rect = max(bb8_rects, key=(lambda x: x[2] * x[3]))
            # 矩形の描画
            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=5)              #ball red
            cv2.rectangle(frame, tuple(bb8_rect[0:2]), tuple(bb8_rect[0:2] + bb8_rect[2:4]), (255, 0, 0), thickness=5)  #bb8  blue
            # 中心点の描画
            # 描画用の座標
            ball_x = rect[0] + (rect[2] // 2)
            ball_y = rect[1] + (rect[3] // 2)
            bb8_x  = bb8_rect[0] + (bb8_rect[2] // 2)
            bb8_y  = bb8_rect[1] + (bb8_rect[3] // 2)
            cv2.circle(frame, tuple([ball_x, ball_y]), 1, (0, 0, 0), 10)
            cv2.circle(frame, tuple([bb8_x, bb8_y]), 1, (0, 0, 0), 10)
            # 角度計算・BB8制御用座標
            ball_ya = abs(ball_y-480)
            bb8_ya  = abs(bb8_y-480)
            degrees = get_degrees(ball_x, ball_ya, bb8_x, bb8_ya)
            print("degrees {}".format(abs(degrees)))
            #print("Ball {}, {}".format(ball_x, ball_ya))
            #print("BB8 {}, {}".format(bb8_x, bb8_ya))

        # 表示
        cv2.namedWindow("BB8 Soccer", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
        cv2.imshow("BB8 Soccer", frame)

    cv2.destroyAllWindows()
