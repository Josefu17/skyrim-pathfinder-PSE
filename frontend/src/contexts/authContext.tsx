import React, {
    createContext,
    useContext,
    useState,
    useEffect,
    useMemo,
} from 'react';

import { TUser, TAuthContext } from '../types'; // Types for the user and the AuthContext
import { USER } from '../support'; // Constants for the storage keys

// Create the context with default values
const AuthContext = createContext<TAuthContext | undefined>(undefined);

// AuthProvider component that wraps the application and provides the context
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
    children,
}) => {
    const [user, setUser] = useState<TUser | null>(null);

    // Load user data from localStorage on initial render
    useEffect(() => {
        const savedUser = localStorage.getItem(USER);
        if (savedUser) {
            try {
                setUser(JSON.parse(savedUser)); // Parse and set the user
            } catch (error) {
                console.error('Failed to parse user from localStorage', error);
                setUser(null);
            }
        } else {
            setUser(null); // Explicitly set user to null if no data exists
        }
    }, []);

    // Save user data to localStorage whenever it changes
    useEffect(() => {
        if (user) {
            localStorage.setItem(USER, JSON.stringify(user)); // Save user as JSON
        } else {
            localStorage.removeItem(USER); // Remove user if null
        }
    }, [user]);

    // Memoize the value object so it doesn't change on every render
    const value = useMemo(() => ({ user, setUser }), [user]);

    return (
        <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
    );
};

// Custom hook to use the AuthContext
export const useAuth = (): TAuthContext => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
