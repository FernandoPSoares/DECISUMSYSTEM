// frontend/src/App.jsx

import React from 'react';
import { AuthProvider } from './context/AuthContext';
import AppRouter from './router/AppRouter';
import { Toaster } from 'react-hot-toast';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';

export default function App() {
  return (
    <AuthProvider>
      <AppRouter />

      {/* --- CONFIGURAÇÃO DO TOASTER REFINADA --- */}
      <Toaster
        position="top-right"
        reverseOrder={false}
        toastOptions={{
          // --- 1. DURAÇÃO REDUZIDA ---
          // A notificação de sucesso agora desaparece após 3 segundos (3000ms).
          duration: 1750,
          
          // --- 2. ESTILO MAIS COMPACTO ---
          // Ajustámos o padding, o tamanho da fonte e a sombra para um visual mais subtil.
          style: {
            background: '#ffffff',
            color: '#1f2937',
            border: '1px solid #e5e7eb',
            padding: '12px 14px', // Menor que antes
            fontSize: '15px',     // Fonte mais pequena
            maxWidth: '350px',
            boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)', // Sombra mais suave
          },

          // Estilos específicos para cada tipo de notificação
          success: {
            // Ícones mais pequenos para combinar com o novo tamanho
            icon: <CheckCircleIcon className="w-5 h-5 text-green-500" />,
            style: {
              background: '#f0fdf4',
              borderColor: '#dcfce7',
            },
          },
          error: {
            duration: 2500, // Damos um pouco mais de tempo para os erros serem lidos
            icon: <XCircleIcon className="w-5 h-5 text-red-500" />,
            style: {
              background: '#fef2f2',
              borderColor: '#fee2e2',
            },
          },
        }}
      />
    </AuthProvider>
  );
}

