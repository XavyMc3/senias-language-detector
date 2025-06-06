import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Silencia warnings de TensorFlow/MediaPipe

import cv2
from sign_detector import SignLanguageDetector

detector = SignLanguageDetector()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignorando fotograma vacío de la cámara.")
        continue

    frame = cv2.flip(frame, 1)
    letter = detector.detect_letter(frame)

    if letter:
        cv2.putText(frame, letter, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)

    cv2.imshow('Test de Deteccion de Señas', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
