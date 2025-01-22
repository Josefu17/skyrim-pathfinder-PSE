import { afterAll, afterEach, describe, expect, it, vi } from 'vitest';
import { fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { act } from 'react';

import { renderWithAuthProvider, testUser } from '../skip.support.test';
import { Register } from '../../src/components/register';
import { MESSAGETIMER } from '../../src/support/support';

globalThis.fetch = vi.fn();

const renderAndSubmitTestUser = async (): Promise<{
    container: HTMLElement;
    usernameInput: HTMLElement;
    submitUsernameButton: HTMLElement;
}> => {
    let container: HTMLElement = document.createElement('div');

    // Use act to wrap rendering
    await act(async () => {
        ({ container } = renderWithAuthProvider(Register));
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

    afterAll(() => {
        vi.restoreAllMocks();
    });

    it('should render correctly', async () => {
        await act(async () => {
            renderWithAuthProvider(Register);
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

    it('should show success message and then clear it after timeout', async () => {
        // Enable fake timers
        vi.useFakeTimers();

        // Mock the fetch call
        globalThis.fetch = vi
            .fn()
            .mockReturnValueOnce({
                ok: true,
                json: async () => ({
                    message: 'Registration successful!',
                    user: testUser,
                }),
            })
            .mockReturnValueOnce({
                ok: true,
                json: async () => ({
                    routes: [
                        {
                            endpoint: 'Rorikstead',
                            id: 139,
                            route: {
                                alternative_distance: 877.25,
                                alternative_route: {
                                    0: 'Karthwasten',
                                    1: 'Markarth',
                                    2: 'Rorikstead',
                                },
                                distance: 362.94,
                                route: {
                                    0: 'Karthwasten',
                                    1: 'Rorikstead',
                                },
                            },
                            startpoint: 'Karthwasten',
                        },
                    ],
                }),
            });

        renderWithAuthProvider(Register);

        // Simulate filling the form
        const input = screen.getByLabelText(/Username/i);
        const button = screen.getByRole('button', { name: /Register/i });

        await act(async () => {
            fireEvent.change(input, { target: { value: testUser.username } });
        });
        await act(async () => {
            fireEvent.click(button);
        });

        // Simulate the passing of time to wait for the success message to appear
        act(() => {
            vi.advanceTimersByTime(100);
        });

        expect(
            screen.getByText(/Registration successful!/i)
        ).toBeInTheDocument();

        // Simulate the passing of time
        console.log('Advancing timers by 2000ms...');
        act(() => {
            vi.advanceTimersByTime(MESSAGETIMER);
        });

        // Wait for the success message to disappear
        expect(
            screen.queryByText(/Registration successful!/i)
        ).not.toBeInTheDocument();

        // Disable fake timers
        vi.useRealTimers();
    });
});
