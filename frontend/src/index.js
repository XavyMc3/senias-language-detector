import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css'; // Si no tienes este archivo, puedes crear uno vacío o quitar esta línea.

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
