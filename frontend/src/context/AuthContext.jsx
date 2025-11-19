// frontend/src/context/AuthContext.jsx

import React, { createContext, useState, useContext, useEffect } from 'react';
import apiClient from '../api/apiClient';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    // --- 1. LEITURA INTELIGENTE DO TOKEN ---
    // Ao iniciar, verifica primeiro o localStorage (persistente) e depois o sessionStorage (temporário).
    const [token, setToken] = useState(
        localStorage.getItem('authToken') || sessionStorage.getItem('authToken')
    );

    useEffect(() => {
        if (token) {
            apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        } else {
            delete apiClient.defaults.headers.common['Authorization'];
        }
    }, [token]);

    // --- 2. FUNÇÃO DE LOGIN ATUALIZADA ---
    // Agora aceita um parâmetro 'rememberMe' para decidir onde guardar o token.
    const login = async (username, password, rememberMe = false) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await apiClient.post('/login/token', formData);
        const newToken = response.data.access_token;
        
        if (rememberMe) {
            localStorage.setItem('authToken', newToken); // Guarda de forma persistente
        } else {
            sessionStorage.setItem('authToken', newToken); // Guarda apenas para a sessão atual
        }
        setToken(newToken);
    };

    // --- 3. FUNÇÃO DE LOGOUT ATUALIZADA ---
    // Garante que o token é removido de AMBOS os locais de armazenamento.
    const logout = () => {
        sessionStorage.removeItem('authToken');
        localStorage.removeItem('authToken');
        setToken(null);
    };

    const authValue = {
        token,
        login,
        logout,
    };

    return <AuthContext.Provider value={authValue}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
    return useContext(AuthContext);
};

