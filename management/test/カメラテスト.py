import cv2

#カメラの設定　デバイスIDは0
cap = cv2.VideoCapture(0)

img = cv2.imread("faces/福沢諭吉_srcnn_anime_noise3_32x.jpg")

while True:
    a=input('A/B')
#繰り返しのためのwhile文
    while True:
        ret, frame = cap.read()
        if a=='A':
            cv2.imshow('camera' , frame)
        elif a=='B':
            cv2.imshow("Image", img)

        key =cv2.waitKey(10)
        if key == 27:
            break
    key =cv2.waitKey(10)
    if key == 27:
        break
#メモリを解放して終了するためのコマンド
cap.release