import React, { useState, useRef, useCallback, useEffect } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import { Camera, RotateCcw, Play, Pause, CheckCircle, XCircle, Award } from 'lucide-react';

const SignLanguageApp = () => {
  const webcamRef = useRef(null);
  const [currentChallenge, setCurrentChallenge] = useState('');
  const [userInput, setUserInput] = useState('');
  const [isCapturing, setIsCapturing] = useState(false);
  const [detectedLetter, setDetectedLetter] = useState('');
  const [score, setScore] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const [feedback, setFeedback] = useState('');
  const [level, setLevel] = useState(1);
  const [consecutiveCorrect, setConsecutiveCorrect] = useState(0);
  
  // Lista de palabras y letras para practicar por nivel
  const challengesByLevel = {
    1: ['A', 'B', 'C', 'D', 'E'],
    2: ['F', 'G', 'H', 'I', 'J'],
    3: ['K', 'L', 'M', 'N', 'O'],
    4: ['P', 'Q', 'R', 'S', 'T'],
    5: ['U', 'V', 'W', 'X', 'Y', 'Z'],
    6: ['HOLA', 'SOL', 'PAZ'],
    7: ['AMOR', 'CASA', 'AGUA'],
    8: ['FELIZ', 'MUNDO', 'VIDA']
  };

  // Inicializar con un desafío aleatorio
  useEffect(() => {
    newChallenge();
  }, [level]);

  const newChallenge = () => {
    const currentChallenges = challengesByLevel[level] || challengesByLevel[1];
    const randomChallenge = currentChallenges[Math.floor(Math.random() * currentChallenges.length)];
    setCurrentChallenge(randomChallenge);
    setUserInput('');
    setIsCompleted(false);
    setFeedback('');
    setDetectedLetter('');
  };

  const captureAndDetect = useCallback(async () => {
    if (!webcamRef.current) return;

    try {
      const imageSrc = webcamRef.current.getScreenshot();
      if (!imageSrc) return;

      // Convertir base64 a blob
      const response = await fetch(imageSrc);
      const blob = await response.blob();
      
      // Crear FormData para enviar al backend
      const formData = new FormData();
      formData.append('image', blob, 'capture.jpg');

      // Enviar al backend
      const result = await axios.post('http://localhost:5000/detect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      const letter = result.data.letter;
      if (letter) {
        setDetectedLetter(letter);
        handleLetterDetected(letter);
      }
    } catch (error) {
      console.error('Error detecting sign:', error);
      setFeedback('Error al detectar la seña. Verifica que el backend esté funcionando.');
    }
  }, [currentChallenge, userInput]);

  const handleLetterDetected = (letter) => {
    const nextExpectedLetter = currentChallenge[userInput.length];
    
    if (letter === nextExpectedLetter) {
      const newInput = userInput + letter;
      setUserInput(newInput);
      setFeedback(`¡Correcto! Detectaste: ${letter}`);
      setConsecutiveCorrect(prev => prev + 1);
      
      if (newInput === currentChallenge) {
        setIsCompleted(true);
        const points = currentChallenge.length * 10 + (level * 5);
        setScore(score + points);
        setFeedback(`¡Excelente! Completaste: ${currentChallenge} (+${points} puntos)`);
        
        // Subir de nivel cada 5 palabras completadas
        if (consecutiveCorrect > 0 && consecutiveCorrect % 5 === 0 && level < 8) {
          setLevel(prev => prev + 1);
          setFeedback(prev => prev + ` ¡Subiste al nivel ${level + 1}!`);
        }
        
        setTimeout(() => {
          newChallenge();
        }, 2500);
      }
    } else {
      setFeedback(`Detectado: ${letter}. Necesitas: ${nextExpectedLetter}`);
      setConsecutiveCorrect(0);
    }
  };

  const toggleCapture = () => {
    setIsCapturing(!isCapturing);
  };

  const resetCurrentWord = () => {
    setUserInput('');
    setDetectedLetter('');
    setFeedback('');
  };

  const resetProgress = () => {
    setScore(0);
    setLevel(1);
    setConsecutiveCorrect(0);
    newChallenge();
  };

  // Auto-captura cuando está activada
  useEffect(() => {
    let interval;
    if (isCapturing && !isCompleted) {
      interval = setInterval(() => {
        captureAndDetect();
      }, 1500); // Captura cada 1.5 segundos
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isCapturing, isCompleted, captureAndDetect]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900 text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent">
            Aprende Lenguaje de Señas
          </h1>
          <p className="text-xl text-blue-200">Practica detectando letras y palabras con tu cámara</p>
        </div>

        {/* Stats Bar */}
        <div className="flex justify-center space-x-6 mb-6 flex-wrap gap-4">
          <div className="bg-white/10 backdrop-blur-md rounded-full px-6 py-2 border border-white/20">
            <span className="text-xl font-bold text-yellow-400">Puntuación: {score}</span>
          </div>
          <div className="bg-white/10 backdrop-blur-md rounded-full px-6 py-2 border border-white/20">
            <span className="text-xl font-bold text-green-400">Nivel: {level}</span>
          </div>
          <div className="bg-white/10 backdrop-blur-md rounded-full px-6 py-2 border border-white/20">
            <span className="text-xl font-bold text-blue-400">Racha: {consecutiveCorrect}</span>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {/* Challenge Panel */}
          <div className="space-y-6">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-2xl">
              <h2 className="text-2xl font-bold mb-4 text-center text-blue-200">
                Desafío Nivel {level}
              </h2>
              
              <div className="text-center mb-6">
                <div className="text-6xl font-mono font-bold mb-4 text-yellow-400">
                  {currentChallenge}
                </div>
                <p className="text-lg text-blue-200">
                  {currentChallenge.length === 1 ? 'Forma esta letra' : 'Forma esta palabra letra por letra'}
                </p>
              </div>

              {/* Progress */}
              <div className="mb-4">
                <div className="flex justify-center space-x-2 mb-2 flex-wrap gap-2">
                  {currentChallenge.split('').map((letter, index) => (
                    <div
                      key={index}
                      className={`w-12 h-12 border-2 rounded-lg flex items-center justify-center text-xl font-bold transition-all duration-300
                        ${index < userInput.length 
                          ? 'bg-green-500 border-green-400 text-white transform scale-110' 
                          : index === userInput.length 
                          ? 'bg-yellow-500 border-yellow-400 text-black animate-pulse' 
                          : 'bg-white/10 border-white/30 text-white/50'
                        }`}
                    >
                      {index < userInput.length ? userInput[index] : letter}
                    </div>
                  ))}
                </div>
                <div className="text-center text-sm text-blue-200">
                  Progreso: {userInput.length}/{currentChallenge.length}
                </div>
              </div>

              {/* Controls */}
              <div className="flex justify-center space-x-4 flex-wrap gap-2">
                <button
                  onClick={newChallenge}
                  className="flex items-center space-x-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 px-4 py-2 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105"
                >
                  <RotateCcw size={20} />
                  <span>Nueva Palabra</span>
                </button>
                <button
                  onClick={resetCurrentWord}
                  className="flex items-center space-x-2 bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700 px-4 py-2 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105"
                >
                  <XCircle size={20} />
                  <span>Reiniciar</span>
                </button>
                <button
                  onClick={resetProgress}
                  className="flex items-center space-x-2 bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 px-4 py-2 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105"
                >
                  <Award size={20} />
                  <span>Reset</span>
                </button>
              </div>
            </div>

            {/* Feedback */}
            {feedback && (
              <div className={`bg-white/10 backdrop-blur-md rounded-2xl p-4 border text-center font-semibold transition-all duration-500 fade-in
                ${feedback.includes('Correcto') || feedback.includes('Excelente') 
                  ? 'border-green-400 text-green-300' 
                  : 'border-yellow-400 text-yellow-300'
                }`}>
                <div className="flex items-center justify-center space-x-2">
                  {feedback.includes('Correcto') || feedback.includes('Excelente') ? (
                    <CheckCircle className="text-green-400" size={24} />
                  ) : (
                    <XCircle className="text-yellow-400" size={24} />
                  )}
                  <span>{feedback}</span>
                </div>
              </div>
            )}

            {/* Level Progress */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/20">
              <h3 className="text-lg font-bold mb-2 text-blue-200">Progreso del Nivel {level}</h3>
              <div className="w-full bg-white/20 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-green-400 to-blue-500 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${(consecutiveCorrect % 5) * 20}%` }}
                ></div>
              </div>
              <p className="text-sm text-blue-200 mt-2">
                {5 - (consecutiveCorrect % 5)} palabras para el siguiente nivel
              </p>
            </div>
          </div>

          {/* Camera Panel */}
          <div className="space-y-6">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-2xl">
              <h2 className="text-2xl font-bold mb-4 text-center text-blue-200">Cámara</h2>
              
              <div className="relative">
                <Webcam
                  ref={webcamRef}
                  screenshotFormat="image/jpeg"
                  className="w-full rounded-xl shadow-lg"
                  mirrored={true}
                />
                
                {/* Overlay con letra detectada */}
                {detectedLetter && (
                  <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm rounded-lg px-3 py-2 animate-pulse">
                    <span className="text-2xl font-bold text-yellow-400">
                      {detectedLetter}
                    </span>
                  </div>
                )}

                {/* Indicador de captura */}
                {isCapturing && (
                  <div className="absolute top-4 left-4 flex items-center space-x-2">
                    <div className="bg-red-500 rounded-full w-4 h-4 animate-pulse"></div>
                    <span className="text-sm bg-black/70 backdrop-blur-sm rounded px-2 py-1">
                      Detectando...
                    </span>
                  </div>
                )}

                {/* Frame guidance */}
                <div className="absolute inset-4 border-2 border-dashed border-white/30 rounded-lg pointer-events-none"></div>
              </div>

              <div className="mt-4 text-center">
                <button
                  onClick={toggleCapture}
                  className={`flex items-center space-x-2 mx-auto px-6 py-3 rounded-lg font-semibold text-lg transition-all duration-200 transform hover:scale-105 ${
                    isCapturing
                      ? 'bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800'
                      : 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800'
                  }`}
                >
                  {isCapturing ? <Pause size={24} /> : <Play size={24} />}
                  <span>{isCapturing ? 'Pausar Detección' : 'Iniciar Detección'}</span>
                </button>
                <p className="text-sm text-blue-200 mt-2">
                  {isCapturing ? 'Detectando señas automáticamente cada 1.5s...' : 'Haz clic para comenzar la detección'}
                </p>
              </div>
            </div>

            {/* Instructions */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
              <h3 className="text-xl font-bold mb-3 text-blue-200">Instrucciones</h3>
              <ul className="space-y-2 text-sm text-blue-100">
                <li>• Coloca tu mano dentro del marco punteado</li>
                <li>• Forma la letra que aparece en el desafío</li>
                <li>• Mantén la posición hasta que sea detectada</li>
                <li>• Completa palabras letra por letra</li>
                <li>• Avanza de nivel completando 5 palabras seguidas</li>
                <li>• ¡Gana más puntos en niveles superiores!</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignLanguageApp;