import { screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import '@testing-library/jest-dom';
import React, { act } from 'react';

import {
    renderWithAuthProvider,
    testUser,
    mockRoutesData,
} from '../skip.support.test'; // importiere die Methode
import { DisplayRoutes } from '../../src/components/displayRoutes';

global.fetch = vi.fn();

describe('DisplayRoutes', () => {
    beforeEach(() => {
        vi.mock('fetch', () => {
            return {
                ok: true,
                json: async () => mockRoutesData,
            };
        });
    });

    afterEach(() => {
        vi.resetAllMocks();
    });

    it('should show login request when user is loading', () => {
        renderWithAuthProvider(<DisplayRoutes />); // Kein User, um den Ladezustand zu testen

        expect(
            screen.getByText('Please log in to view routes.')
        ).toBeInTheDocument();
    });

    it.skip('should render routes when user is logged in and routes are fetched', async () => {
        renderWithAuthProvider(<DisplayRoutes />, testUser);

        // Check if the user-specific message is present
        expect(
            screen.getByText(`Routes History of ${testUser.username}`)
        ).toBeInTheDocument();

        // Wait for the list item to appear, ensuring the fetch response is processed
        const listitem = await waitFor(() => {
            return screen.findByRole('listitem', {
                name: /Karthwasten to Rorikstead/i,
            });
        });

        expect(listitem).toBeInTheDocument();
    });

    it('should allow deleting a route when in deletion mode', async () => {
        renderWithAuthProvider(<DisplayRoutes />, testUser);

        // Enter deletion mode
        act(() => {
            fireEvent.click(screen.getByText('Enter deletion mode'));
        });

        const deleteAllButton = await waitFor(() =>
            screen.getByText('Delete all')
        );

        // Spy auf console.log (falls Logging geprüft wird)
        const consoleSpy = vi
            .spyOn(console, 'log')
            .mockImplementation(() => {});

        // Simuliere Klick auf Delete-All-Button
        await act(() => {
            fireEvent.click(deleteAllButton);
        });

        // Prüfung
        expect(consoleSpy).toHaveBeenCalledWith('Deleting all routes');

        consoleSpy.mockRestore();
    });

    it('should render optional parameters when the button is clicked', async () => {
        renderWithAuthProvider(<DisplayRoutes />, testUser); // testUser wird gesetzt

        fireEvent.click(screen.getByText('Show more options'));

        expect(screen.getByLabelText('from:')).toBeInTheDocument();
        expect(screen.getByLabelText('to:')).toBeInTheDocument();
        expect(screen.getByLabelText('startpoint:')).toBeInTheDocument();
        expect(screen.getByLabelText('endpoint:')).toBeInTheDocument();
    });

    it('should delete selected routes when delete button is clicked', async () => {
        // Spy on console.log and add a custom implementation for the test
        const consoleSpy = vi
            .spyOn(console, 'log')
            .mockImplementationOnce(() => {});

        renderWithAuthProvider(<DisplayRoutes />, testUser); // testUser is provided

        // Enter deletion mode
        act(() => {
            fireEvent.click(screen.getByText('Enter deletion mode'));
        });

        const deleteButton = await waitFor(() =>
            screen.getByText('Delete all')
        );

        act(() => {
            fireEvent.click(deleteButton);
        });

        await waitFor(() => {
            expect(consoleSpy).toHaveBeenCalledWith('Deleting all routes');
        });

        // Restore the original behavior of console.log after the test
        consoleSpy.mockRestore();
    });

    it.skip('should handle error when deleting selected route fails', async () => {
        // Override the mock to simulate an error
        const mockFetch = vi.fn().mockImplementation(async (url) => {
            if (url.includes('DELETE')) {
                return Promise.resolve({
                    ok: false,
                    json: async () => ({ error: 'Error deleting route' }),
                });
            }
            // For routes fetch
            return Promise.resolve({
                ok: true,
                json: async () => mockRoutesData,
            });
        });

        globalThis.fetch = mockFetch;

        const mockDeleteRoute = vi.fn();

        renderWithAuthProvider(<DisplayRoutes />, testUser);

        // Wait for the route data to be rendered
        await waitFor(() => screen.getByText('Karthwasten to Rorikstead'));

        // Simulate clicking the delete button for a route
        fireEvent.click(screen.getByText('Delete'));

        // Expect the deletion function to be called
        expect(mockDeleteRoute).toHaveBeenCalledTimes(1);

        // Verify that an error message is logged
        expect(console.error).toHaveBeenCalledWith(
            'Error deleting routes: Error deleting route'
        );
    });

    it.skip('should handle error when deleting all routes fails', async () => {
        // Mock fetch to simulate failure for deleting all routes
        vi.mock('fetch', (url) => {
            if (url.includes('DELETE')) {
                return Promise.resolve({
                    ok: false,
                    json: async () => ({ error: 'Error deleting all routes' }),
                });
            }
            // For routes fetch
            return Promise.resolve({
                ok: true,
                json: async () => mockRoutesData,
            });
        });

        renderWithAuthProvider(<DisplayRoutes />, testUser);

        // Wait for routes to load
        await waitFor(() => screen.getByText('Karthwasten to Rorikstead'));

        // Simulate clicking the "Delete all" button
        fireEvent.click(screen.getByText('Delete all'));

        // Verify that fetch was called for deleting all routes
        expect(globalThis.fetch).toHaveBeenCalledWith(
            `${import.meta.env.VITE_URL}/users/${testUser.id}/routes`,
            {
                method: 'DELETE',
            }
        );

        // Verify error logging behavior
        expect(console.error).toHaveBeenCalledWith(
            'Error deleting all routes: Error deleting all routes'
        );
    });
});
