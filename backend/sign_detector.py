import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_styles  = mp.solutions.drawing_styles

def distancia_euclidiana(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

class SignLanguageDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=1
        )

    def detect_letter(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Ahora con estilo multicolor "Google" predeterminado
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    mp_styles.get_default_hand_landmarks_style(),
                    mp_styles.get_default_hand_connections_style()
                )

            hand_landmarks = results.multi_hand_landmarks[0]
            height, width, _ = frame.shape

            # Extracción de puntos de referencia
            index_finger_tip = (int(hand_landmarks.landmark[8].x * width), int(hand_landmarks.landmark[8].y * height))
            index_finger_pip = (int(hand_landmarks.landmark[6].x * width), int(hand_landmarks.landmark[6].y * height))
            index_finger_mcp = (int(hand_landmarks.landmark[5].x * width), int(hand_landmarks.landmark[5].y * height))
            thumb_tip = (int(hand_landmarks.landmark[4].x * width), int(hand_landmarks.landmark[4].y * height))
            thumb_pip = (int(hand_landmarks.landmark[2].x * width), int(hand_landmarks.landmark[2].y * height))
            middle_finger_tip = (int(hand_landmarks.landmark[12].x * width), int(hand_landmarks.landmark[12].y * height))
            middle_finger_pip = (int(hand_landmarks.landmark[10].x * width), int(hand_landmarks.landmark[10].y * height))
            ring_finger_tip = (int(hand_landmarks.landmark[16].x * width), int(hand_landmarks.landmark[16].y * height))
            ring_finger_pip = (int(hand_landmarks.landmark[14].x * width), int(hand_landmarks.landmark[14].y * height))
            pinky_tip = (int(hand_landmarks.landmark[20].x * width), int(hand_landmarks.landmark[20].y * height))
            pinky_pip = (int(hand_landmarks.landmark[18].x * width), int(hand_landmarks.landmark[18].y * height))
            wrist = (int(hand_landmarks.landmark[0].x * width), int(hand_landmarks.landmark[0].y * height))

            # Lógica de detección de letras
            # Letra A
            if abs(thumb_tip[1] - index_finger_pip[1]) < 45 and \
               abs(thumb_tip[1] - middle_finger_pip[1]) < 30 and \
               abs(thumb_tip[1] - ring_finger_pip[1]) < 30 and \
               abs(thumb_tip[1] - pinky_pip[1]) < 30:
                return 'A'


            # Letra B
            elif index_finger_pip[1] > index_finger_tip[1] and \
                 middle_finger_pip[1] > middle_finger_tip[1] and \
                 ring_finger_pip[1] > ring_finger_tip[1] and \
                 pinky_pip[1] > pinky_tip[1] and \
                 abs(thumb_tip[1] - index_finger_mcp[1]) < 40:
                return 'B'

            # Letra C
            elif abs(index_finger_tip[1] - thumb_tip[1]) < 360 and \
                 index_finger_tip[1] < middle_finger_pip[1] and \
                 index_finger_tip[1] < ring_finger_pip[1] and \
                 index_finger_pip[1] > index_finger_tip[1]:
                return 'C'

            # Letra D
            elif distancia_euclidiana(thumb_tip, middle_finger_tip) < 65 and \
                 distancia_euclidiana(thumb_tip, ring_finger_tip) < 65 and \
                 pinky_pip[1] > pinky_tip[1] and \
                 index_finger_pip[1] > index_finger_tip[1]:
                 return 'D'

            # Letra E
            elif index_finger_pip[1] < index_finger_tip[1] and \
                 middle_finger_pip[1] < middle_finger_tip[1] and \
                 ring_finger_pip[1] < ring_finger_tip[1] and \
                 pinky_pip[1] < pinky_tip[1] and \
                 abs(index_finger_tip[1] - thumb_tip[1]) < 100:
                return 'E'
            
            # Letra F
            elif pinky_pip[1] > pinky_tip[1] and \
                 middle_finger_pip[1] > middle_finger_tip[1] and \
                 ring_finger_pip[1] > ring_finger_tip[1] and \
                 distancia_euclidiana(index_finger_tip, thumb_tip) < 65:
                return 'F'

            # Letra I
            elif index_finger_pip[1] < index_finger_tip[1] and \
                 middle_finger_pip[1] < middle_finger_tip[1] and \
                 ring_finger_pip[1] < ring_finger_tip[1] and \
                 pinky_pip[1] > pinky_tip[1]:
                return 'I'

            # Letra L
            elif index_finger_pip[1] > index_finger_tip[1] and \
                 middle_finger_pip[1] < middle_finger_tip[1] and \
                 ring_finger_pip[1] < ring_finger_tip[1] and \
                 pinky_pip[1] < pinky_tip[1] and \
                 thumb_tip[0] > thumb_pip[0]:
                return 'L'
            
            # Letra W
            elif index_finger_pip[1] > index_finger_tip[1] and \
                 middle_finger_pip[1] > middle_finger_tip[1] and \
                 ring_finger_pip[1] > ring_finger_tip[1] and \
                 pinky_pip[1] < pinky_tip[1]:
                return 'W'
            
            # Letra Y
            elif index_finger_pip[1] < index_finger_tip[1] and \
                 middle_finger_pip[1] < middle_finger_tip[1] and \
                 ring_finger_pip[1] < ring_finger_tip[1] and \
                 pinky_pip[1] > pinky_tip[1] and \
                 thumb_tip[0] > thumb_pip[0]:
                return 'Y'

                        # Letra G
            elif abs(index_finger_tip[1] - index_finger_pip[1]) < 20 and \
                 abs(thumb_tip[1] - thumb_pip[1]) < 20 and \
                 index_finger_tip[0] > thumb_tip[0]:
                return 'G'

            # Letra H
            elif abs(index_finger_tip[1] - index_finger_pip[1]) < 20 and \
                 abs(middle_finger_tip[1] - middle_finger_pip[1]) < 20 and \
                 ring_finger_pip[1] < ring_finger_tip[1] and \
                 pinky_pip[1] < pinky_tip[1]:
                return 'H'

            # Letra J (movimiento necesario, aquí solo validación de forma inicial)
            elif index_finger_tip[1] > index_finger_pip[1] and \
                 thumb_tip[0] > index_finger_tip[0] and \
                 pinky_pip[1] < pinky_tip[1]:
                return 'J'

            # Letra K
            elif index_finger_pip[1] > index_finger_tip[1] and \
                 middle_finger_pip[1] > middle_finger_tip[1] and \
                 thumb_tip[1] < thumb_pip[1]:
                return 'K'

            # Letra M
            elif thumb_tip[0] < index_finger_mcp[0] and \
                 index_finger_tip[1] < middle_finger_tip[1] and \
                 middle_finger_tip[1] < ring_finger_tip[1]:
                return 'M'

            # Letra N
            elif thumb_tip[0] < index_finger_mcp[0] and \
                 index_finger_tip[1] < middle_finger_tip[1] and \
                 middle_finger_tip[1] > ring_finger_tip[1]:
                return 'N'

            # Letra O
            elif distancia_euclidiana(index_finger_tip, thumb_tip) < 50 and \
                 distancia_euclidiana(middle_finger_tip, ring_finger_tip) < 50:
                return 'O'

            # Letra P
            elif index_finger_tip[1] > index_finger_pip[1] and \
                 middle_finger_tip[1] > middle_finger_pip[1] and \
                 thumb_tip[1] < index_finger_tip[1]:
                return 'P'

            # Letra Q
            elif thumb_tip[1] > thumb_pip[1] and \
                 index_finger_tip[1] > index_finger_pip[1] and \
                 thumb_tip[0] > index_finger_tip[0]:
                return 'Q'

            # Letra R
            elif index_finger_pip[1] > index_finger_tip[1] and \
                 middle_finger_pip[1] > middle_finger_tip[1] and \
                 abs(index_finger_tip[0] - middle_finger_tip[0]) < 20:
                return 'R'

            # Letra S
            elif thumb_tip[0] < index_finger_mcp[0] and \
                 index_finger_pip[1] < index_finger_tip[1] and \
                 middle_finger_pip[1] < middle_finger_tip[1]:
                return 'S'

            # Letra T
            elif thumb_tip[1] < index_finger_pip[1] and \
                 abs(thumb_tip[0] - index_finger_pip[0]) < 20:
                return 'T'

            # Letra U
            elif index_finger_pip[1] > index_finger_tip[1] and \
                 middle_finger_pip[1] > middle_finger_tip[1] and \
                 abs(index_finger_tip[0] - middle_finger_tip[0]) < 30:
                return 'U'

            # Letra V
            elif index_finger_pip[1] > index_finger_tip[1] and \
                 middle_finger_pip[1] > middle_finger_tip[1] and \
                 abs(index_finger_tip[0] - middle_finger_tip[0]) > 30:
                return 'V'

            # Letra X
            elif index_finger_tip[1] > index_finger_pip[1] and \
                 abs(index_finger_tip[0] - index_finger_pip[0]) < 15:
                return 'X'

            # Letra Z (requiere movimiento, aquí solo forma de inicio)
            elif index_finger_pip[1] > index_finger_tip[1] and \
                 middle_finger_pip[1] < middle_finger_tip[1] and \
                 thumb_tip[0] < index_finger_tip[0]:
                return 'Z'
