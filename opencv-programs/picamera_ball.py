# coding: utf-8
import picamera
import picamera.array
import cv2
import numpy as np

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (640, 480)
        while True:
            # stream.arrayにRGBの順で映像データを格納
            camera.capture(stream, 'bgr', use_video_port=True)

            # グレースケールに変換
            #gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)
            # ↓
            # HSVに変換
            hsv = cv2.cvtColor(stream.array, cv2.COLOR_BGR2HSV)

            # 白のHSV範囲
            lower =np.array([0,0,100])
            upper =np.array([180,45,255])

            # yellow
            #lower = np.array([60, 62, 100])
            #upper = np.array([60, 100, 100])

            # マスク
            mask_white = cv2.inRange(hsv, lower, upper)
            res_white = cv2.bitwise_and(stream.array, stream.array, mask=mask_white)

            # 輪郭抽出
            gray = cv2.cvtColor(res_white, cv2.COLOR_RGB2GRAY)
            ret, thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)
            imgEdge, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # 一番大きい輪郭を抽出
            contours.sort(key=cv2.contourArea, reverse=True)
            for i in contours:
                print(i)

            if len(contours)==0:
                cv2.imshow('frame', stream.array)
                 # "q"でウィンドウを閉じる
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

                stream.seek(0)
                stream.truncate()
                continue
            cnt = contours[0]

            # 円を描画！
            (x,y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            img = cv2.circle(stream.array,center,radius,(0,255,0),2)

            # 再生
            cv2.imshow('frame', stream.array)

            # "q"でウィンドウを閉じる
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            # streamをリセット
            stream.seek(0)
            stream.truncate()
        cv2.destroyAllWindows()
