import { afterEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import React, { act } from 'react';

import { renderWithAuthProvider } from '../skip.support.test';
import { Register } from '../../src/components/register';

globalThis.fetch = vi.fn();

const renderAndSubmitTestUser = async (): Promise<{
    container: HTMLElement;
    usernameInput: HTMLElement;
    submitUsernameButton: HTMLElement;
}> => {
    let container: HTMLElement = document.createElement('div');

    // Use act to wrap rendering
    await act(async () => {
        ({ container } = renderWithAuthProvider(<Register />));
    });

    // Find the username input field
    const usernameInput = await screen.findByLabelText(/username/i);
    expect(usernameInput).toBeInTheDocument();

    // Type "test_user" into the username input field
    await act(async () => {
        fireEvent.change(usernameInput, { target: { value: 'test_user' } });
    });

    // Assert that the input value was updated
    expect(usernameInput).toHaveValue('test_user');

    // Find the submit button
    const submitUsernameButton = await screen.findByRole('button', {
        name: /register/i,
    });

    // Click the submit button
    await act(async () => {
        fireEvent.click(submitUsernameButton);
    });

    return { container, usernameInput, submitUsernameButton };
};

describe('Register', () => {
    afterEach(() => {
        vi.clearAllMocks();
    });

    it('should render correctly', async () => {
        await act(async () => {
            renderWithAuthProvider(<Register />);
        });

        const submitUsernameButton = await screen.findByRole('button', {
            name: /register/i,
        });

        expect(submitUsernameButton).toBeInTheDocument();
    });

    it('should show success message after entering username and submitting', async () => {
        // Mock fetch response
        globalThis.fetch = vi.fn().mockResolvedValueOnce({
            ok: true,
            json: async () => ({ message: 'Registration successful!' }),
        });

        await renderAndSubmitTestUser();

        const successMessage = await screen.findByText(
            /registration successful!/i
        );
        expect(successMessage).toBeInTheDocument();
    });

    it('should show error message after entering username and submitting', async () => {
        // Mock fetch response
        globalThis.fetch = vi.fn().mockResolvedValueOnce({
            ok: false,
            json: async () => ({ error: 'Username already taken' }),
        });

        await renderAndSubmitTestUser();

        const errorMessage = await screen.findByText(/Username already taken/i);
        expect(errorMessage).toBeInTheDocument();
    });

    it('should show generic error message after entering username and submitting', async () => {
        // Mock fetch response
        globalThis.fetch = vi
            .fn()
            .mockRejectedValueOnce(new Error('Network error'));

        await renderAndSubmitTestUser();

        const errorMessage = await screen.findByText(/an error occurred/i);
        expect(errorMessage).toBeInTheDocument();
    });

    it.skip('should show success message and then clear it after timeout', async () => {
        // Enable fake timers
        vi.useFakeTimers();
        globalThis.fetch = vi.fn().mockReturnValueOnce({
            ok: true,
            json: async () => ({
                message: 'Registration successful!',
                user: { username: 'test_user', id: 1 },
            }),
        });

        renderWithAuthProvider(<Register />);

        // Fill the form and simulate the submit
        const input = await screen.getByLabelText(/username/i);
        const button = await screen.getByRole('button', { name: /Register/i });

        act(() => {
            fireEvent.change(input, { target: { value: 'test_user' } });
            fireEvent.click(button);
        });

        // Check if the success message is displayed
        const successMessage = await screen.getByText(
            /Registration successful!/i
        );
        expect(successMessage).toBeInTheDocument();

        // Simulate the passing of time (3 seconds)
        act(() => {
            vi.advanceTimersByTime(3000); // Advance the timer by 3 seconds
        });

        // Check if the success message is removed after timeout
        expect(successMessage).not.toBeInTheDocument();

        // Disable fake timers
        vi.useRealTimers();
    });
});
