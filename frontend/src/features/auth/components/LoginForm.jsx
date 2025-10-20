// frontend/src/features/auth/components/LoginForm.jsx

import React, { useState } from 'react';
import { useAuth } from '../../../context/AuthContext';
import Spinner from '../../../components/ui/Spinner';
import { UserIcon, LockClosedIcon, EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import { Link } from 'react-router-dom';

export default function LoginForm() {
    const [username, setUsername] = useState('admin.sistema');
    const [password, setPassword] = useState('senha123');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    
    // --- NOVO ESTADO PARA A CHECKBOX ---
    const [rememberMe, setRememberMe] = useState(false);
    
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        try {
            // Passamos o estado da checkbox para a função de login
            await login(username, password, rememberMe);
        } catch (err) {
            setError('Utilizador ou senha incorretos. Verifique as suas credenciais.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div>
                <label htmlFor="username" className="sr-only">Utilizador ou Email</label>
                <div className="relative">
                    <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                        <UserIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                        id="username"
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        className="w-full pl-10 pr-4 py-3 text-gray-900 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                        placeholder="Utilizador ou Email"
                    />
                </div>
            </div>
            <div>
                <label htmlFor="password" className="sr-only">Senha</label>
                <div className="relative">
                    <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                        <LockClosedIcon className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                        id="password"
                        type={showPassword ? 'text' : 'password'}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="w-full pl-10 pr-10 py-3 text-gray-900 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                        placeholder="Senha"
                    />
                    <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                        <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="text-gray-400 hover:text-gray-600"
                        >
                            {showPassword ? (
                                <EyeSlashIcon className="h-5 w-5" />
                            ) : (
                                <EyeIcon className="h-5 w-5" />
                            )}
                        </button>
                    </div>
                </div>
            </div>
            
            {error && <p className="text-sm text-center text-red-600">{error}</p>}

            <div className="flex items-center justify-between text-sm">
                <div className="flex items-center">
                    {/* --- CHECKBOX FUNCIONAL --- */}
                    <input 
                        id="remember-me" 
                        name="remember-me" 
                        type="checkbox" 
                        checked={rememberMe}
                        onChange={(e) => setRememberMe(e.target.checked)}
                        className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500" 
                    />
                    <label htmlFor="remember-me" className="ml-2 block text-gray-900">Lembrar de mim</label>
                </div>
                <Link to="/forgot-password" className="font-medium text-indigo-600 hover:text-indigo-500">
                    Esqueceu-se da sua senha?
                </Link>
            </div>

            <div>
                <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full flex justify-center px-4 py-3 font-semibold text-white bg-indigo-600 rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-400 disabled:cursor-not-allowed transition-all"
                >
                    {isLoading ? <Spinner /> : 'Entrar'}
                </button>
            </div>
        </form>
    );
}

