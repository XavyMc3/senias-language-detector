import axios from 'axios';

// La URL donde se está ejecutando tu backend de Flask.
// Asegúrate de que el puerto (5000) sea el correcto.
const API_URL = 'http://localhost:5000';

/**
 * Envía un frame de imagen al backend para detectar la seña.
 * @param {string} imageSrc - La imagen en formato base64.
 * @returns {Promise<string|null>} La letra detectada o null si hay un error.
 */
export const detectSign = async (imageSrc) => {
  try {
    // Convierte la imagen base64 a un archivo Blob
    const blob = await fetch(imageSrc).then(res => res.blob());
    const formData = new FormData();
    formData.append('image', blob, 'webcam-frame.jpg');

    // Realiza la petición POST al endpoint /detect
    const response = await axios.post(`${API_URL}/detect`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    // Devuelve la letra detectada por el backend
    if (response.data && response.data.letter) {
      return response.data.letter;
    }
  } catch (error) {
    console.error("Error al detectar la seña:", error);
    return null;
  }
};