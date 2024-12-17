import { afterEach, describe, expect, it, vi } from 'vitest';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import React, { act } from 'react';

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
        ({ container } = render(<Register />));
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
            render(<Register />);
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
            json: async () => ({ message: 'Username already taken' }),
        });

        await renderAndSubmitTestUser();

        const errorMessage = await screen.findByText(/username already taken/i);
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
});
