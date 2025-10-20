// frontend/src/hooks/useDebounce.js

import { useState, useEffect } from 'react';

// Hook personalizado que atrasa a atualização de um valor
export default function useDebounce(value, delay) {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        // Define um temporizador para atualizar o valor apenas após o 'delay'
        const handler = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        // Limpa o temporizador se o valor mudar antes do 'delay' terminar
        return () => {
            clearTimeout(handler);
        };
    }, [value, delay]);

    return debouncedValue;
}
