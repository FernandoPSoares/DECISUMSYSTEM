// frontend/src/features/auth/ResetPasswordPage.jsx

import React, { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import apiClient from '../../api/apiClient';
import Spinner from '../../components/ui/Spinner';
import { toast } from 'react-hot-toast';
import { ArrowLeftIcon } from '@heroicons/react/24/solid';

export default function ResetPasswordPage() {
    const [searchParams] = useSearchParams();
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
    const token = searchParams.get('token');

    useEffect(() => {
        if (!token) {
            toast.error("Token de recuperação inválido ou em falta.");
            navigate('/login');
        }
    }, [token, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            setError('As senhas não coincidem.');
            return;
        }
        setIsLoading(true);
        setError('');

        try {
            await apiClient.post('/reset-password', {
                token: token,
                nova_senha: password,
            });
            
            toast.success("Senha redefinida com sucesso! Pode agora fazer o login.");
            navigate('/login');

        } catch (err) {
            const detail = err.response?.data?.detail || "Não foi possível redefinir a senha.";
            setError(detail);
            toast.error(detail);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-50 to-indigo-100 p-4">
            <div className="w-full max-w-md p-8 space-y-6 bg-white/70 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-200">
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-gray-900">Redefinir Senha</h2>
                    <p className="mt-2 text-sm text-gray-600">
                        Crie uma nova senha para a sua conta.
                    </p>
                </div>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label htmlFor="password" className="block text-sm font-medium text-gray-700">Nova Senha</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            className="mt-1 w-full px-4 py-3 text-gray-900 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        />
                    </div>
                    <div>
                        <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">Confirmar Nova Senha</label>
                        <input
                            id="confirmPassword"
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                            className="mt-1 w-full px-4 py-3 text-gray-900 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        />
                    </div>
                    {error && <p className="text-sm text-center text-red-600">{error}</p>}
                    <div>
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full flex justify-center px-4 py-3 font-semibold text-white bg-indigo-600 rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                            {isLoading ? <Spinner /> : 'Redefinir Senha'}
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
