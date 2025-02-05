// can be filled with any support functions, variables etc. that could be useful in multiple components
import { useState, useEffect } from 'react';

// Define the keys for global usage in an namespace
// This way we can import all the keys in other files
export const USER = 'user';
export const REGISTER = 'register';
export const LOGIN = 'login';
export const MAP = 'map';

export const MESSAGETIMER = 2000;

export default {
    USER,
    REGISTER,
    LOGIN,
    MAP,
    MESSAGETIMER,
};

// Custom Hook to determine screen orientation based on media query
export const useScreenOrientation = () => {
    const [isPortrait, setIsPortrait] = useState<boolean>(
        window.innerHeight > window.innerWidth
    );

    useEffect(() => {
        const handleResize = () => {
            // If the screen is 1024px or wider, treat it as Landscape
            if (
                window.innerWidth >= 1024 ||
                window.innerWidth / window.innerHeight >= 1
            ) {
                setIsPortrait(false); // Landscape
            } else {
                setIsPortrait(true); // Portrait
            }
        };

        // Set the initial state
        handleResize();

        // Watch for screen resize events
        window.addEventListener('resize', handleResize);

        // Cleanup the event listener
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    return isPortrait;
};
