import face_recognition

from os import listdir
import sys
import cv2
import numpy as np
import math
print('顔認証バージョン0.01')
cap = cv2.VideoCapture(1)
print('カメラが起動したよ')
camera_check=input('カメラが起動してない場合はendと入力してね>>')

if camera_check == 'end':
    exit('終了するよ')
else:
    print('OK!')

Registered_Names = []
Registered_Faces = []
Registered_Faces_Encoding = []

image_file = [filename for filename in listdir(
    '/Users/tomoya/Desktop/テックソン/1/顔認証/Faces') if not filename.startswith('.')]

for image in image_file:

    face_image = face_recognition.load_image_file(
        f'/Users/tomoya/Desktop/テックソン/1/顔認証/Faces/{image}')
    face_encoding = face_recognition.face_encodings(face_image)[0]
    print(face_encoding)
    Registered_Names.append(image.replace('.jpg', ''))
    Registered_Faces_Encoding.append(face_encoding)

print(Registered_Names)
print(Registered_Faces_Encoding)

while True:
    ret, frame = cap.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_name = []

    for face_encoding in face_encodings:
        name = '????'
        matchs = face_recognition.compare_faces(
            Registered_Faces_Encoding, face_encoding)
        face_distances = face_recognition.face_distance(
            Registered_Faces_Encoding, face_encoding)
        best_matchs = np.argmin(face_distances)
        if matchs[best_matchs]:
            name = Registered_Names[best_matchs]
        else:
            name = 'Unknown'
        # print(face_distances) #顔の一致率?　0に近いほど似ている。
        # print(best_matchs) #リストの中で最も数値が低い（登録されている顔と一致している）数値が何番目にあるのかが入る。
        # print(matchs) #登録されている顔がカメラの顔と一致する場合Trueを返す。
        print(name) #登録済みの顔と一致する場合、名前を表示する。未登録の場合'Unknown'と表示する