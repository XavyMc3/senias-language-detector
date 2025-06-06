import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { detectSign } from '../services/api';

const SignPlayer = () => {
  const webcamRef = useRef(null);
  const [detectedLetter, setDetectedLetter] = useState('...');

  // Función que se ejecuta a intervalos para detectar la seña
  const captureAndDetect = useCallback(async () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        const letter = await detectSign(imageSrc);
        if (letter) {
          setDetectedLetter(letter);
        }
      }
    }
  }, [webcamRef]);

  // Ejecuta la detección cada segundo
  React.useEffect(() => {
    const interval = setInterval(() => {
      captureAndDetect();
    }, 1000); // Detecta cada 1 segundo

    return () => clearInterval(interval); // Limpia el intervalo al desmontar el componente
  }, [captureAndDetect]);

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', fontFamily: 'sans-serif' }}>
      <h1>Intérprete de Lenguaje de Señas</h1>
      <p>Muestra una letra del abecedario a la cámara.</p>
      <div style={{ position: 'relative', width: '720px' }}>
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
          style={{ width: '100%', borderRadius: '10px' }}
        />
        <div style={{
          position: 'absolute',
          top: '20px',
          right: '20px',
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          color: 'white',
          padding: '10px 20px',
          borderRadius: '10px',
          fontSize: '48px',
          fontWeight: 'bold',
        }}>
          {detectedLetter}
        </div>
      </div>
    </div>
  );
};

export default SignPlayer;