import socket
import numpy as np
import cv2
import time
import picamera
import picamera.array

PICAM = True

def initCamera():
    cap = None
    res = False
    while res is False:
        if PICAM:
            cap = picamera.PiCamera()
            # cap.start_preview()
            cap.resolution = (640, 480)
            cap.framerate = 33
            cv2.waitKey(1000)
            res = True
        else:
            cap = cv2.VideoCapture(DEVICE_ID)
            res, _ = cap.read()
            #pass
            cv2.waitKey(1000)
            print('retry ..')
        return cap

def getImage(cap):
    c_frame = None
    if PICAM:
        with picamera.array.PiRGBArray(cap, size=(640, 480)) as stream:
            c_frame = cap.capture(stream, 'bgr')
            c_frame = stream.array
            if c_frame is None:
                exit

    else:
        end_flag, c_frame = cap.read()
        if end_flag is False or c_frame is None:
            exit
    return c_frame

if __name__ == '__main__':
    #ソケットオブジェクト作成
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # サーバー側PCのipと使用するポート
    s.bind(("192.168.0.30", 50000))
    print("接続待機中")

    # 接続要求を待機
    s.listen(1)

    # 要求が来るまでブロック
    soc, addr = s.accept()
    print(str(addr)+"と接続完了")

    #カメラオブジェクト作成
    cam = initCamera()

    while (True):
        #カメラから画像データを受け取る
        img = getImage(cam)

        #numpy行列からバイトデータに変換
        img = img.tostring()

        # ソケットにデータを送信
        soc.send(img)

        #フリーズするなら#を外す。
        #time.sleep(0.5)

        # ESCで終了
        k = cv2.waitKey(1)
        if k == 27 :
            break

    #カメラオブジェクト破棄
    cam.releace()
