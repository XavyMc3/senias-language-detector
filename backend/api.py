from flask import Flask, request, jsonify
from flask_cors import CORS
from sign_detector import SignLanguageDetector
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)  # Permite peticiones desde el frontend
detector = SignLanguageDetector()

@app.route('/detect', methods=['POST'])
def detect_sign():
    # Verificar si se envió una imagen
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    # Leer imagen del request
    file = request.files['image']
    img_bytes = file.read()
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Procesar detección
    try:
        letter = detector.detect_letter(frame)
        return jsonify({'letter': letter})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)