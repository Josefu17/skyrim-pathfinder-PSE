import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React from 'react';

import { useAuth } from '../../src/contexts/authContext';
import { renderWithAuthProvider } from '../skip.support.test';

// Mock localStorage
const mockUser = { id: 1, username: 'test_user' };

describe('AuthContext', () => {
    beforeEach(() => {
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation((key) => {
            if (key === 'user') {
                return JSON.stringify(mockUser); // Return a mock user
            }
            return null;
        });

        vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {});
        vi.spyOn(Storage.prototype, 'removeItem').mockImplementation(() => {});
    });

    afterEach(() => {
        vi.clearAllMocks();
    });

    it('should load user from localStorage on initial render', () => {
        // Custom Test Component to consume the context
        const TestComponent = () => {
            const { user } = useAuth();
            return <div>{user ? `Hello, ${user.username}` : 'No user'}</div>;
        };

        renderWithAuthProvider(TestComponent);

        // Expect the user to be loaded from localStorage
        expect(screen.getByText('Hello, test_user')).toBeInTheDocument();
    });

    it('should set user to null if localStorage contains invalid JSON', () => {
        // Mock localStorage to return invalid JSON
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation(
            () => 'invalid-json'
        );

        const consoleErrorSpy = vi
            .spyOn(console, 'error')
            .mockImplementation(() => {});

        const TestComponent = () => {
            const { user } = useAuth();
            return <div>{user ? `User: ${user.username}` : 'No user'}</div>;
        };

        renderWithAuthProvider(TestComponent);

        // Expect the user to be null due to invalid JSON
        expect(screen.getByText('No user')).toBeInTheDocument();

        // Verify that console.error was called
        expect(consoleErrorSpy).toHaveBeenCalledWith(
            'Failed to parse user from localStorage',
            expect.any(Error)
        );

        consoleErrorSpy.mockRestore();
    });

    it('should set user to null if no user data is in localStorage', () => {
        // Mock localStorage to return null (no saved user)
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => null);

        const TestComponent = () => {
            const { user } = useAuth();
            return <div>{user ? `User: ${user.username}` : 'No user'}</div>;
        };

        renderWithAuthProvider(TestComponent);

        // Expect the user to be null and "No user" to be displayed
        expect(screen.getByText('No user')).toBeInTheDocument();
    });

    it('should throw an error if useAuth is used outside of AuthProvider', () => {
        const TestComponent = () => {
            useAuth();
            return <div>Test</div>;
        };

        // Render die Komponente ohne den AuthProvider
        expect(() => render(<TestComponent />)).toThrowError(
            'useAuth must be used within an AuthProvider'
        );
    });
});
