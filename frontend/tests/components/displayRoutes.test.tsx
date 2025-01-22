import { screen, fireEvent, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, Mock, vi } from 'vitest';
import '@testing-library/jest-dom';
import { act } from 'react';

import {
    renderWithAuthProvider,
    testUser,
    mockRoutesData,
    mockCities,
} from '../skip.support.test'; // importiere die Methode
import { TFilterOptions } from '../../src/types';
import { DisplayRoutes } from '../../src/components/displayRoutes';

global.fetch = vi.fn();

describe('DisplayRoutes', () => {
    beforeEach(() => {
        (global.fetch as Mock).mockImplementation((url) => {
            if (url.includes('/cities')) {
                console.error('Fetching cities');
                return {
                    ok: true,
                    json: async () => mockCities,
                };
            }
            return Promise.resolve({
                ok: true,
                json: async () => mockRoutesData,
            });
        });
    });

    afterEach(() => {
        vi.resetAllMocks();
    });

    it('should show login request when user is loading', () => {
        renderWithAuthProvider(DisplayRoutes); // Kein User, um den Ladezustand zu testen

        expect(
            screen.getByText('Please log in to view routes.')
        ).toBeInTheDocument();
    });

    it('should render routes when user is logged in and routes are fetched', async () => {
        renderWithAuthProvider(DisplayRoutes, testUser);

        // Check if the user-specific message is present
        expect(
            screen.getByText(`Routes History of ${testUser.username}`)
        ).toBeInTheDocument();

        // Wait for the list item to appear, ensuring the fetch response is processed
        const listitem = await waitFor(() => {
            return screen.getByText('Karthwasten to Rorikstead');
        });

        expect(listitem).toBeInTheDocument();
    });

    it('should allow deleting a route when in deletion mode', async () => {
        renderWithAuthProvider(DisplayRoutes, testUser);

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
        renderWithAuthProvider(DisplayRoutes, testUser); // testUser wird gesetzt

        act(() => {
            fireEvent.click(screen.getByText('Show more options'));
        });

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

        renderWithAuthProvider(DisplayRoutes, testUser); // testUser is provided

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

    it('should handle error when fetching routes fails', async () => {
        // Mock `fetch` to simulate failure
        (global.fetch as Mock).mockImplementation(() => {
            return Promise.resolve({
                ok: false,
                json: async () => ({
                    error: 'Error test',
                }),
            });
        });

        // Spy on console.error to verify error logging
        const consoleSpy = vi
            .spyOn(console, 'error')
            .mockImplementation(() => {});

        // Render the component with mocked auth
        renderWithAuthProvider(DisplayRoutes, testUser);

        expect(
            screen.getByText(`Routes History of ${testUser.username}`)
        ).toBeInTheDocument();

        // Verify that the error was logged to the console
        await waitFor(() => {
            expect(consoleSpy).toHaveBeenCalledWith('Error fetching routes');
        });

        // Restore all mocked functions
        vi.restoreAllMocks();
    });

    it('should handle error when deleting selected route fails', async () => {
        // Mock `fetch` to simulate DELETE failure and GET success
        (global.fetch as Mock).mockImplementation((url, options) => {
            if (options?.method === 'DELETE') {
                // Simulate DELETE failure
                return Promise.resolve({
                    ok: false,
                    json: async () => ({
                        error: 'Error test',
                    }),
                });
            }
            // Simulate successful fetch for routes
            return Promise.resolve({
                ok: true,
                json: async () => mockRoutesData,
            });
        });

        // Spy on console.error to verify error logging
        const consoleSpy = vi
            .spyOn(console, 'error')
            .mockImplementation(() => {});

        // Render the component with mocked auth
        renderWithAuthProvider(DisplayRoutes, testUser);

        // Wait for routes to load
        await waitFor(() => screen.getByText('Karthwasten to Rorikstead'));

        // Simulate clicking the "Enter deletion mode" button
        act(() => {
            fireEvent.click(screen.getByText('Enter deletion mode'));
        });

        // Simulate clicking a route for its deletion
        await act(() => {
            fireEvent.click(screen.getByText('Karthwasten to Rorikstead'));
        });

        // Verify `fetch` was called for DELETE
        expect(global.fetch).toHaveBeenCalledWith(
            // @ts-expect-error - TS doesn't know about env variables
            `${import.meta.env.VITE_URL || ''}/users/${testUser.id}/routes/${mockRoutesData.routes[0].id}`,
            {
                method: 'DELETE',
            }
        );

        // Verify that the error was logged to the console
        expect(consoleSpy).toHaveBeenCalledWith(
            'Error deleting route: Error: (user test): Error test'
        );

        // Ensure the UI still shows the routes since the deletion failed
        expect(
            screen.getByText('Karthwasten to Rorikstead')
        ).toBeInTheDocument();

        // Restore all mocked functions
        vi.restoreAllMocks();
    });

    it('should handle error when deleting all routes fails', async () => {
        // Mock `fetch` to simulate DELETE failure and GET success
        (global.fetch as Mock).mockImplementation((url, options) => {
            if (options?.method === 'DELETE') {
                // Simulate DELETE failure
                return Promise.resolve({
                    ok: false,
                    json: async () => ({
                        error: 'Error test',
                    }),
                });
            }
            // Simulate successful fetch for routes
            return Promise.resolve({
                ok: true,
                json: async () => mockRoutesData,
            });
        });

        // Spy on console.error to verify error logging
        const consoleSpy = vi
            .spyOn(console, 'error')
            .mockImplementation(() => {});

        // Render the component with mocked auth
        renderWithAuthProvider(DisplayRoutes, testUser);

        // Wait for routes to load
        await waitFor(() => screen.getByText('Karthwasten to Rorikstead'));

        // Simulate clicking the "Enter deletion mode" button
        act(() => {
            fireEvent.click(screen.getByText('Enter deletion mode'));
        });

        // Simulate clicking the "Delete all" button
        await act(() => {
            fireEvent.click(screen.getByText('Delete all'));
        });

        // Verify `fetch` was called for DELETE
        expect(global.fetch).toHaveBeenCalledWith(
            // @ts-expect-error - TS doesn't know about env variables
            `${import.meta.env.VITE_URL || ''}/users/${testUser.id}/routes`,
            {
                method: 'DELETE',
            }
        );

        // Verify that the error was logged to the console
        expect(consoleSpy).toHaveBeenCalledWith(
            'Error deleting all routes: Error: (user test): Error test'
        );

        // Ensure the UI still shows the routes since the deletion failed
        expect(
            screen.getByText('Karthwasten to Rorikstead')
        ).toBeInTheDocument();

        // Restore all mocked functions
        vi.restoreAllMocks();
    });

    it('renders dropdowns with all options initially', async () => {
        renderWithAuthProvider(DisplayRoutes, testUser, {
            defaultOptionalParametersVisible: true,
        });

        // Wait for the component to load routes
        await waitFor(() => {
            expect(screen.getByLabelText('startpoint:')).toBeInTheDocument();
            expect(screen.getByLabelText('endpoint:')).toBeInTheDocument();
        });

        // Check if dropdowns contain all city options initially
        await waitFor(() => {
            expect(screen.getAllByText('City A')[0]).toBeInTheDocument();
            expect(screen.getAllByText('City B')[0]).toBeInTheDocument();
        });
    });

    it.skip('sorts routes ascending when the checkbox is unchecked', async () => {
        renderWithAuthProvider(DisplayRoutes, testUser, {
            defaultOptionalParametersVisible: false,
            defaultFilterOptions: {
                limit: 1,
            } as TFilterOptions,
        });

        // Check if the routes are sorted in descending order
        const routes_descending = await waitFor(() => {
            const element = screen.getAllByRole('listitem').map((Component) => {
                const inputElement = Component.children[0] as HTMLInputElement;
                return inputElement.value;
            });
            if (!element) throw new Error('Element not found');
            return element;
        });

        expect(routes_descending[0]).toBe('Karthwasten to Rorikstead');
        expect(routes_descending[1]).toBe('Whiterun to Windhelm');

        // Check if the checkbox is present
        const sortCheckbox = screen.getByLabelText('descending');

        // Check if the checkbox is unchecked by default
        expect(sortCheckbox).toHaveAttribute('checked');

        // Check if the checkbox is checked after clicking it
        await act(async () => {
            fireEvent.click(sortCheckbox);
        });

        expect(sortCheckbox).not.toHaveAttribute('checked');
        console.log('checkbox unchecked');

        // Check if the routes are sorted in descending order
        const routes_ascending = await waitFor(async () => {
            const element = screen.getAllByRole('listitem').map((Component) => {
                const inputElement = Component.children[0] as HTMLInputElement;
                return inputElement.value;
            });
            if (!element) throw new Error('Element not found');
            return element;
        });

        screen.debug();
        expect(routes_ascending[0]).toBe('Whiterun to Windhelm');
        expect(routes_ascending[1]).toBe('Karthwasten to Rorikstead');
    });

    it.skip('excludes the startpoint from endpoint options when selected', async () => {
        renderWithAuthProvider(DisplayRoutes, testUser, {
            defaultOptionalParametersVisible: true,
        });

        // Wait for dropdowns to load
        await waitFor(() => {
            expect(screen.getByLabelText('startpoint:')).toBeInTheDocument();
            expect(screen.getByLabelText('endpoint:')).toBeInTheDocument();
        });

        const startpointSelect = screen.getByLabelText('startpoint:');

        // Select "City A" as the startpoint
        await act(async () => {
            fireEvent.change(startpointSelect, { target: { value: 'City A' } });
        });

        // Verify that "City A" is excluded from the endpoint options
        expect(
            screen.queryByText('City A', { selector: 'select#endpoint option' })
        ).not.toBeInTheDocument();

        // Other cities should still be present in the endpoint dropdown
        expect(
            screen.getByText('City B', { selector: 'select#endpoint option' })
        ).toBeInTheDocument();
    });

    it.skip('excludes the endpoint from startpoint options when selected', async () => {
        renderWithAuthProvider(DisplayRoutes, testUser, {
            defaultOptionalParametersVisible: true,
        });

        // Wait for dropdowns to load
        await waitFor(() => {
            expect(screen.getByLabelText('startpoint:')).toBeInTheDocument();
            expect(screen.getByLabelText('endpoint:')).toBeInTheDocument();
        });

        const endpointSelect = screen.getByLabelText('endpoint:');

        // Select "City B" as the endpoint
        await act(async () => {
            fireEvent.change(endpointSelect, { target: { value: 'City B' } });
        });

        console.log('endpointSelected');

        // Other cities should still be present in the startpoint dropdown
        await waitFor(async () => {
            expect(
                screen.getByText('City A', {
                    selector: 'select#startpoint option',
                })
            ).toBeInTheDocument();
        });

        // Verify that "City B" is excluded from the startpoint options
        await waitFor(async () => {
            expect(
                screen.getByText('City B', {
                    selector: 'select#startpoint option',
                })
            ).not.toBeInTheDocument();
        });
    });

    it.skip('restores options correctly when dropdowns are cleared', async () => {
        renderWithAuthProvider(DisplayRoutes, testUser, {
            defaultOptionalParametersVisible: true,
        });

        // Wait for dropdowns to load
        await waitFor(() => {
            expect(screen.getByLabelText('startpoint:')).toBeInTheDocument();
            expect(screen.getByLabelText('endpoint:')).toBeInTheDocument();
        });

        const startpointSelect = screen.getByLabelText('startpoint:');
        const endpointSelect = screen.getByLabelText('endpoint:');

        // Select "City A" as the startpoint and "City B" as the endpoint
        await act(async () => {
            fireEvent.change(startpointSelect, { target: { value: 'City A' } });
        });

        await act(async () => {
            fireEvent.change(endpointSelect, { target: { value: 'City B' } });
        });

        // Verify options are excluded
        await waitFor(async () => {
            expect(
                screen.queryByText('City A', {
                    selector: 'select#endpoint option',
                })
            ).not.toBeInTheDocument();
        });
        await waitFor(async () => {
            expect(
                screen.queryByText('City B', {
                    selector: 'select#startpoint option',
                })
            ).not.toBeInTheDocument();
        });

        // Clear selections
        await act(async () => {
            fireEvent.change(startpointSelect, { target: { value: '' } });
        });

        await act(async () => {
            fireEvent.change(endpointSelect, { target: { value: '' } });
        });

        // Verify all cities are available again
        await waitFor(() => {
            expect(
                screen.getByText('City A', {
                    selector: 'select#endpoint option',
                })
            ).toBeInTheDocument();
        });
        await waitFor(() => {
            expect(
                screen.getByText('City B', {
                    selector: 'select#startpoint option',
                })
            ).toBeInTheDocument();
        });
    });
});
