import React, {
    createContext,
    useContext,
    useState,
    useEffect,
    useMemo,
} from 'react';

import { TMap, TMapContext } from '../types'; // Types for the currentMap and the MapContext
import { MAP } from '../support/support'; // Constants for the storage keys

// Create the context with default values
export const MapContext = createContext<TMapContext | undefined>(undefined);

// MapProvider component that wraps the application and provides the context
export const MapProvider: React.FC<{ children: React.ReactNode }> = ({
    children,
}) => {
    const [currentMap, setCurrentMap] = useState<TMap | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    // Load currentMap data from localStorage on initial render
    useEffect(() => {
        const savedCurrentMap = localStorage.getItem(MAP);
        if (savedCurrentMap) {
            try {
                setCurrentMap(JSON.parse(savedCurrentMap)); // Parse and set the currentMap
            } catch (error) {
                console.error(
                    'Failed to parse currentMap from localStorage',
                    error
                );
                setCurrentMap(null);
            }
        } else {
            setCurrentMap({ id: 1, name: 'skyrim' }); // Explicitly set currentMap to skyrim if no data exists
        }
        setLoading(false); // Set loading to false after loading currentMap data
    }, []);

    // Save currentMap data to localStorage whenever it changes
    useEffect(() => {
        if (currentMap) {
            localStorage.setItem(MAP, JSON.stringify(currentMap)); // Save currentMap as JSON
        } else {
            localStorage.removeItem(MAP); // Remove currentMap if null
        }
    }, [currentMap]);

    // Memoize the value object so it doesn't change on every render
    const value = useMemo(
        () => ({ currentMap, setCurrentMap, loading }),
        [currentMap, loading]
    );

    return <MapContext.Provider value={value}>{children}</MapContext.Provider>;
};

// Custom hook to use the MapContext
export const useMap = (): TMapContext => {
    const context = useContext(MapContext);
    if (!context) {
        throw new Error('useMap must be used within an MapProvider');
    }
    return context;
};
