import { describe, it, expect, vi, beforeEach, Mock } from 'vitest';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom'; // Für bessere Matcher wie `toBeInTheDocument`
import React from 'react';

import { Logout } from '../../src/components/logout';
import { useAuth } from '../../src/contexts/authContext';

// Mock useAuth hook
vi.mock('../../src/contexts/authContext', () => ({
    useAuth: vi.fn(),
}));

describe('Logout Component', () => {
    const mockSetUser = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks(); // Reset all mocks before each test
    });

    it('should do nothing and log message if no user is logged in', () => {
        // Mock useAuth to return no user
        (useAuth as Mock).mockReturnValue({
            user: null,
            setUser: mockSetUser,
        });

        // Spy on console.log
        const consoleLogSpy = vi.spyOn(console, 'log');

        render(<Logout />);

        // Click the logout button
        const logoutButton = screen.getByRole('button', { name: /logout/i });
        fireEvent.click(logoutButton);

        // Expect "No user logged in" to be logged
        expect(consoleLogSpy).toHaveBeenCalledWith('No user logged in');

        // Expect setUser not to be called
        expect(mockSetUser).not.toHaveBeenCalled();
    });

    it('should log out the user and set user to null', () => {
        // Mock useAuth to return a user
        (useAuth as Mock).mockReturnValue({
            user: { id: 1, username: 'test_user' },
            setUser: mockSetUser,
        });

        // Spy on console.log
        const consoleLogSpy = vi.spyOn(console, 'log');

        render(<Logout />);

        // Click the logout button
        const logoutButton = screen.getByRole('button', { name: /logout/i });
        fireEvent.click(logoutButton);

        // Expect "Logging out user: test_user" to be logged
        expect(consoleLogSpy).toHaveBeenCalledWith(
            'Logging out user: test_user'
        );

        // Expect setUser to have been called with null
        expect(mockSetUser).toHaveBeenCalledWith(null);
    });
});
