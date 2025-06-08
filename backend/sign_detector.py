import cv2
import mediapipe as mp
import numpy as np
import base64
from io import BytesIO
from PIL import Image

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

        annotated_image = frame.copy()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    mp_styles.get_default_hand_landmarks_style(),
                    mp_styles.get_default_hand_connections_style()
                )

            hand_landmarks = results.multi_hand_landmarks[0]
            height, width, _ = frame.shape

            # Coordenadas normalizadas a pixeles
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

            # Codificar imagen anotada en base64
            _, buffer = cv2.imencode('.jpg', annotated_image)
            image_base64 = base64.b64encode(buffer).decode('utf-8')

            # 🟢 Desde aquí continúa tu lógica de detección de letras
            # Retorna letra detectada y base64
            if abs(thumb_tip[1] - index_finger_pip[1]) < 45 and \
               abs(thumb_tip[1] - middle_finger_pip[1]) < 30 and \
               abs(thumb_tip[1] - ring_finger_pip[1]) < 30 and \
               abs(thumb_tip[1] - pinky_pip[1]) < 30:
                return 'A', image_base64
            
            # Letra B
            elif index_finger_pip[1] > index_finger_tip[1] and \
                 middle_finger_pip[1] > middle_finger_tip[1] and \
                 ring_finger_pip[1] > ring_finger_tip[1] and \
                 pinky_pip[1] > pinky_tip[1] and \
                 abs(thumb_tip[1] - index_finger_mcp[1]) < 40:
                return 'B', image_base64

            # Letra C
            elif abs(index_finger_tip[1] - thumb_tip[1]) < 360 and \
                 index_finger_tip[1] < middle_finger_pip[1] and \
                 index_finger_tip[1] < ring_finger_pip[1] and \
                 index_finger_pip[1] > index_finger_tip[1]:
                return 'C', image_base64

            # Letra D
            elif distancia_euclidiana(thumb_tip, middle_finger_tip) < 65 and \
                 distancia_euclidiana(thumb_tip, ring_finger_tip) < 65 and \
                 pinky_pip[1] > pinky_tip[1] and \
                 index_finger_pip[1] > index_finger_tip[1]:
                return 'D', image_base64

            # Letra E
            elif index_finger_pip[1] < index_finger_tip[1] and \
                 middle_finger_pip[1] < middle_finger_tip[1] and \
                 ring_finger_pip[1] < ring_finger_tip[1] and \
                 pinky_pip[1] < pinky_tip[1] and \
                 abs(index_finger_tip[1] - thumb_tip[1]) < 100:
                return 'E', image_base64

            # Letra F
            elif pinky_pip[1] > pinky_tip[1] and \
                 middle_finger_pip[1] > middle_finger_tip[1] and \
                 ring_finger_pip[1] > ring_finger_tip[1] and \
                 distancia_euclidiana(index_finger_tip, thumb_tip) < 65:
                return 'F', image_base64

            # Letra G (gesto apuntando lateralmente con índice extendido y pulgar)
            elif index_finger_tip[0] > index_finger_pip[0] and \
                 thumb_tip[1] < index_finger_tip[1] and \
                 middle_finger_tip[1] > index_finger_tip[1]:
                return 'G', image_base64

            # Letra H (índice y medio extendidos, demás dedos doblados)
            elif index_finger_tip[0] > index_finger_pip[0] and \
                 middle_finger_tip[0] > middle_finger_pip[0] and \
                 ring_finger_tip[1] > ring_finger_pip[1] and \
                 pinky_tip[1] > pinky_pip[1]:
                return 'H', image_base64

            # Letra I (meñique extendido, resto doblado)
            elif pinky_tip[1] < pinky_pip[1] and \
                 index_finger_tip[1] > index_finger_pip[1] and \
                 middle_finger_tip[1] > middle_finger_pip[1] and \
                 ring_finger_tip[1] > ring_finger_pip[1]:
                return 'I', image_base64

            # Letra J (parecida a I pero con movimiento, difícil sin video, se puede simular igual que I)
            elif pinky_tip[1] < pinky_pip[1] and \
                 index_finger_tip[1] > index_finger_pip[1] and \
                 middle_finger_tip[1] > middle_finger_pip[1]:
                return 'J', image_base64

            # Letra K (índice y medio en forma de “V”, pulgar entre ellos)
            elif abs(index_finger_tip[0] - middle_finger_tip[0]) > 20 and \
                 thumb_tip[1] < index_finger_tip[1]:
                return 'K', image_base64

            # Letra L (índice hacia arriba y pulgar hacia el costado)
            elif index_finger_tip[1] < index_finger_pip[1] and \
                 abs(thumb_tip[0] - index_finger_tip[0]) > 50:
                return 'L', image_base64

            # Letra M (tres dedos sobre el pulgar)
            elif index_finger_tip[1] > thumb_tip[1] and \
                 middle_finger_tip[1] > thumb_tip[1] and \
                 ring_finger_tip[1] > thumb_tip[1]:
                return 'M', image_base64

            # Letra N (dos dedos sobre el pulgar)
            elif index_finger_tip[1] > thumb_tip[1] and \
                 middle_finger_tip[1] > thumb_tip[1] and \
                 ring_finger_tip[1] < thumb_tip[1]:
                return 'N', image_base64

            # Letra O (forma circular con todos los dedos)
            elif distancia_euclidiana(index_finger_tip, thumb_tip) < 50 and \
                 distancia_euclidiana(middle_finger_tip, thumb_tip) < 50:
                return 'O', image_base64

            # Letra P (similar a K pero con palma hacia abajo)
            elif abs(index_finger_tip[0] - middle_finger_tip[0]) > 20 and \
                 index_finger_tip[1] > index_finger_pip[1] and \
                 thumb_tip[0] < index_finger_tip[0]:
                return 'P', image_base64

            # Letra Q (similar a G pero hacia abajo)
            elif index_finger_tip[0] < index_finger_pip[0] and \
                 thumb_tip[1] > index_finger_tip[1]:
                return 'Q', image_base64

            # Letra R (índice y medio cruzados)
            elif abs(index_finger_tip[0] - middle_finger_tip[0]) < 10 and \
                 index_finger_tip[1] < middle_finger_tip[1]:
                return 'R', image_base64

            # Letra S (puño cerrado)
            elif distancia_euclidiana(index_finger_tip, thumb_tip) < 30 and \
                 pinky_tip[1] > pinky_pip[1]:
                return 'S', image_base64

            # Letra T (pulgar entre índice y medio)
            elif abs(thumb_tip[0] - index_finger_tip[0]) < 20 and \
                 thumb_tip[1] > index_finger_tip[1]:
                return 'T', image_base64

            # Letra U (índice y medio juntos hacia arriba)
            elif abs(index_finger_tip[0] - middle_finger_tip[0]) < 10 and \
                 index_finger_tip[1] < index_finger_pip[1]:
                return 'U', image_base64

            # Letra V (índice y medio formando “V”)
            elif abs(index_finger_tip[0] - middle_finger_tip[0]) > 20 and \
                 index_finger_tip[1] < index_finger_pip[1]:
                return 'V', image_base64

            # Letra W (índice, medio y anular en forma de “W”)
            elif index_finger_tip[1] < index_finger_pip[1] and \
                 middle_finger_tip[1] < middle_finger_pip[1] and \
                 ring_finger_tip[1] < ring_finger_pip[1]:
                return 'W', image_base64

            # Letra X (dedo índice curvado como garra)
            elif index_finger_tip[1] > index_finger_pip[1] and \
                 index_finger_tip[0] > index_finger_pip[0] and \
                 thumb_tip[1] < index_finger_tip[1]:
                return 'X', image_base64

            # Letra Y (meñique y pulgar extendidos)
            elif pinky_tip[1] < pinky_pip[1] and \
                 thumb_tip[1] < thumb_pip[1] and \
                 index_finger_tip[1] > index_finger_pip[1]:
                return 'Y', image_base64

            # Letra Z (requiere movimiento, difícil con imagen estática. Aquí una simulación)
            elif index_finger_tip[0] > index_finger_pip[0] and \
                 index_finger_tip[1] > index_finger_pip[1] and \
                 thumb_tip[1] > index_finger_tip[1]:
                return 'Z', image_base64

            # Si no se reconoce ninguna letra
            return None, image_base64
