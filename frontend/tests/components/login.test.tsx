import { describe, it, expect, vi, beforeEach, afterEach, Mock } from 'vitest';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import React from 'react';

import { Login } from '../../src/components/login';
import { useAuth } from '../../src/contexts/authContext';
import { MESSAGETIMER } from '../../src/support';

// Mock useAuth Hook
vi.mock('../../src/contexts/authContext', () => ({
    useAuth: vi.fn(),
}));

describe('Login Component', () => {
    const mockSetUser = vi.fn();
    const mockFetch = vi.fn();

    beforeEach(() => {
        vi.resetAllMocks();
        vi.spyOn(globalThis, 'fetch').mockImplementation(mockFetch);
        (useAuth as Mock).mockReturnValue({
            setUser: mockSetUser,
        });
    });

    afterEach(() => {
        vi.clearAllMocks();
        vi.restoreAllMocks();
    });

    it('should handle successful login', async () => {
        const mockResponse = {
            json: async () => ({ id: 1 }),
            ok: true,
        };

        mockFetch.mockResolvedValue(mockResponse);

        render(<Login />);

        // Input username
        const input = screen.getByLabelText('Username');
        fireEvent.change(input, { target: { value: 'test_user' } });

        // Submit form
        const submitButton = screen.getByRole('button', { name: /Login/i });
        fireEvent.click(submitButton);

        // Check for success message
        await waitFor(() => {
            expect(
                screen.getByText('Logged in as test_user')
            ).toBeInTheDocument();
        });

        // Expect setUser to have been called with the correct user
        expect(mockSetUser).toHaveBeenCalledWith({
            username: 'test_user',
            id: 1,
        });
    });

    it('should handle failed login with error message', async () => {
        const mockErrorResponse = {
            json: async () => ({ error: 'Invalid username' }),
            ok: false,
        };

        mockFetch.mockResolvedValue(mockErrorResponse);

        render(<Login />);

        // Input username
        const input = screen.getByLabelText('Username');
        fireEvent.change(input, { target: { value: 'test_user' } });

        // Submit form
        const submitButton = screen.getByRole('button', { name: /login/i });
        fireEvent.click(submitButton);

        // Check for error message
        await waitFor(() => {
            expect(screen.getByText('Invalid username')).toBeInTheDocument();
        });

        // Expect setUser not to be called
        expect(mockSetUser).not.toHaveBeenCalled();
    });

    it('should handle network error during login', async () => {
        mockFetch.mockRejectedValue(new Error('Network error'));

        render(<Login />);

        // Input username
        const input = screen.getByLabelText('Username');
        fireEvent.change(input, { target: { value: 'test_user' } });

        // Submit form
        const submitButton = screen.getByRole('button', { name: /login/i });
        fireEvent.click(submitButton);

        // Check for network error message
        await waitFor(() => {
            expect(
                screen.getByText(
                    'An error occurred. Please try again later. Error: Network error'
                )
            ).toBeInTheDocument();
        });

        // Expect setUser not to be called
        expect(mockSetUser).not.toHaveBeenCalled();
    });

    it('should clear status message after MESSAGETIMER duration', async () => {
        const mockResponse = {
            json: async () => ({ id: 1 }),
            ok: true,
        };

        mockFetch.mockResolvedValue(mockResponse);

        render(<Login />);

        // Input username
        const input = screen.getByLabelText('Username');
        fireEvent.change(input, { target: { value: 'test_user' } });

        // Submit form
        const submitButton = screen.getByRole('button', { name: /login/i });
        fireEvent.click(submitButton);

        // Check for success message
        await waitFor(() => {
            expect(
                screen.getByText('Logged in as test_user')
            ).toBeInTheDocument();
        });

        // Wait for MESSAGETIMER duration
        await waitFor(
            () => {
                expect(
                    screen.queryByText('Logged in as test_user')
                ).not.toBeInTheDocument();
            },
            { timeout: MESSAGETIMER + 100 } // Add slight buffer to ensure timeout finishes
        );
    });
});
