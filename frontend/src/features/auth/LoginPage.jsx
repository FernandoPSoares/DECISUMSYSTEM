// frontend/src/features/auth/LoginPage.jsx

import React from 'react';
import LoginForm from './components/LoginForm';

export default function LoginPage() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
            <div className="w-full max-w-4xl flex flex-col md:flex-row rounded-2xl shadow-2xl overflow-hidden">
                
                {/* --- Coluna Esquerda: Branding --- */}
                <div className="w-full md:w-1/2 p-8 flex flex-col justify-center items-center bg-gradient-to-br from-indigo-600 to-violet-700 text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" className="w-16 h-16" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
                    </svg>
                    <h1 className="mt-6 text-4xl font-bold tracking-tight">
                        DecisumSystem
                    </h1>
                    <p className="mt-2 text-indigo-200 text-center">
                        A plataforma integrada para otimizar as suas operações.
                    </p>
                </div>

                {/* --- Coluna Direita: Formulário --- */}
                <div className="w-full md:w-1/2 p-8 bg-white flex flex-col justify-center">
                    <div className="w-full max-w-sm mx-auto">
                        <h2 className="text-2xl font-bold text-gray-800 mb-2">
                            Iniciar Sessão
                        </h2>
                        <p className="text-gray-600 mb-6">
                            Use o seu utilizador ou e-mail para aceder.
                        </p>
                        <LoginForm />
                    </div>
                </div>
            </div>
        </div>
    );
}

