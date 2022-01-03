# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 16:11:36 2021

@author: Oğuz yıldırım - B181210085
"""

import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

from firebase import firebase
firebase = firebase.FirebaseApplication("https://iotproje-d97e6-default-rtdb.europe-west1.firebasedatabase.app/", None)

# Kamera girişi
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        #Kamerayi doğru açıya döndürürüz ve renkli yaparız
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks: #handlandmarkları saydırıyor

                ## el açık ve kapalı iken ekrana yazdırma
                x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y  # 9.nokta x,y
                x1, y1 = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y #12.nokta x,y

                font = cv2.FONT_HERSHEY_PLAIN

                if y1 > y: # el kapalı
                    cv2.putText(image, "KAPALI", (10, 50), font, 4, (0, 0, 0), 3)
                    firebase.put('/test/' , 'LED_STATUS', 0) # firebase led durumunu 0 yapar
                else:
                    cv2.putText(image, "ACIK", (10, 50), font, 4, (0, 0, 0), 3)
                    firebase.put('/test/' , 'LED_STATUS', 1) # firebase led durumunu 1 yapar

                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        cv2.imshow('IOT PROJECT', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
       