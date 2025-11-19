// frontend/src/features/auth/ForgotPasswordPage.jsx

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import apiClient from '../../api/apiClient';
import Spinner from '../../components/ui/Spinner';
import { toast } from 'react-hot-toast';
import { ArrowLeftIcon } from '@heroicons/react/24/solid';

export default function ForgotPasswordPage() {
    const [email, setEmail] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        const promise = apiClient.post('/password-recovery', { email });

        toast.promise(promise, {
            loading: 'A enviar link de recuperação...',
            success: 'Se o e-mail estiver registado, receberá um link de recuperação.',
            error: 'Ocorreu um erro ao processar o seu pedido.',
        });

        // Espera 2 segundos para o utilizador ler o "toast" e depois redireciona
        promise.finally(() => {
            setTimeout(() => {
                navigate('/login');
            }, 2000);
        });
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-50 to-indigo-100 p-4">
            <div className="w-full max-w-md p-8 space-y-6 bg-white/70 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-200">
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-gray-900">Recuperar Senha</h2>
                    <p className="mt-2 text-sm text-gray-600">
                        Insira o seu e-mail para receber um link de redefinição de senha.
                    </p>
                </div>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-700">Endereço de e-mail</label>
                        <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            className="mt-1 w-full px-4 py-3 text-gray-900 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            placeholder="o.seu.email@exemplo.com"
                        />
                    </div>
                    <div>
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full flex justify-center px-4 py-3 font-semibold text-white bg-indigo-600 rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400"
                        >
                            {isLoading ? <Spinner /> : 'Enviar Link de Recuperação'}
                        </button>
                    </div>
                </form>
                <div className="text-center mt-6">
                    <Link to="/login" className="text-sm font-medium text-indigo-600 hover:text-indigo-500 inline-flex items-center">
                        <ArrowLeftIcon className="w-4 h-4 mr-1" />
                        Voltar para o Login
                    </Link>
                </div>
            </div>
        </div>
    );
}
