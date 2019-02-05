import sys
import cv2
import numpy as np

def getBall(frame):
    # HSV色範囲指定
    # yellow
    #lower = np.array([30,100,250])
    #upper = np.array([40,255,255])
    # pink
    #lower = np.array([160,50,50])
    #upper = np.array([180,255,255])
    # yellowgreen
    lower = np.array([30,100,100])
    upper = np.array([60,255,250])

    # 指定した色範囲のみを抽出
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = cv2.inRange(frame, lower, upper)

    # 輪郭抽出
    image, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for contour in contours:
        # 輪郭の凹凸のあるドットの情報を内包する多角形を生成
        approx = cv2.convexHull(contour)
        # 生成した多角形を内包する矩形を計算
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))
    
    return rects


def getBB8(frame):
    # HSV色範囲指定
    # orange
    lower = np.array([15,150,150])
    upper = np.array([35,255,255])

    # 指定した色範囲のみを抽出
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = cv2.inRange(frame, lower, upper)

    # 輪郭抽出
    image, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for contour in contours:
        # 輪郭の凹凸のあるドットの情報を内包する多角形を生成
        approx = cv2.convexHull(contour)
        # 生成した多角形を内包する矩形を計算
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))
    
    return rects

if __name__ == '__main__':
    cap = cv2.VideoCapture("http://127.0.0.1:8081/")
    # ESCキーが押されるまで検出
    while cv2.waitKey(10) != 27:
        frame = cap.read()[1]
        rects = getBall(frame)
        bb8_rects = getBB8(frame)

        # 検出された矩形の中から最大のものだけ描画
        if len(rects) > 0 and len(bb8_rects) > 0:
            # 第2引数で指定した関数は矩形の面積を求めている
            rect = max(rects, key=(lambda x: x[2] * x[3]))
            bb8_rect = max(bb8_rects, key=(lambda x: x[2] * x[3]))
            # 矩形の描画
            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=5)
            cv2.rectangle(frame, tuple(bb8_rect[0:2]), tuple(bb8_rect[0:2] + bb8_rect[2:4]), (255, 0, 0), thickness=5)
            # 中心点の描画
            cv2.circle(frame, tuple([rect[0] + (rect[2] // 2), rect[1] + (rect[3] // 2)]), 1, (0, 0, 0), 10)
            cv2.circle(frame, tuple([bb8_rect[0] + (bb8_rect[2] // 2), bb8_rect[1] + (bb8_rect[3] // 2)]), 1, (0, 0, 0), 10)
            #print('Ball: {}'.format(tuple([rect[0] + (rect[2] // 2), rect[1] + (rect[3] // 2)])))
            #print('BB8 : {}'.format(tuple([bb8_rect[0] + (bb8_rect[2] // 2), bb8_rect[1] + (bb8_rect[3] // 2)])))

        # 表示
        cv2.namedWindow("TennisBall Detector", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
        cv2.imshow("TennisBall Detector", frame)

    cv2.destroyAllWindows()
