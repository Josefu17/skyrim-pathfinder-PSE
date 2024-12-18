import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React from 'react';

import { InteractiveMap } from '../../src/components/interactiveMap';

globalThis.fetch = vi.fn();

describe('InteractiveMap Component', () => {
    // Mock data for the map
    const mockConnection = {
        cities: [
            { id: 1, name: 'City A', position_x: 100, position_y: 200 },
            { id: 2, name: 'City B', position_x: 300, position_y: 400 },
        ],
        connections: [{ parent_city_id: 1, child_city_id: 2 }],
    };

    const mockCities = {
        cities: [
            { id: 1, name: 'City A', position_x: 100, position_y: 200 },
            { id: 2, name: 'City B', position_x: 300, position_y: 400 },
        ],
        connections: [],
    };

    const mockRoute = {
        route: {
            '0': 'City A',
            '1': 'City B',
        },
        distance: 5000,
    };

    // Helper function to render the map and return the container and cities
    async function RenderInteractiveMapCities(): Promise<{
        container: HTMLElement;
        cityA: Element;
        cityB: Element;
    }> {
        const { container } = render(<InteractiveMap />);

        // Wait for the map to render
        const cityA = await screen.findByText('City A');
        const cityB = await screen.findByText('City B');

        // Check if the cities are displayed
        expect(cityA).toBeInTheDocument();
        expect(cityB).toBeInTheDocument();

        return { container, cityA, cityB };
    }

    async function RenderInteractiveMapAndTriggerFetchRoute(): Promise<{
        container: HTMLElement;
        cityA: Element;
        cityB: Element;
    }> {
        // Render the component
        const { container } = render(<InteractiveMap />);

        // Wait for the cities to render
        const cityA = await waitFor(() => {
            const element = container.querySelector('[id="endpoint-1"]');
            if (!element) throw new Error('Element not found');
            return element;
        });
        const cityB = await waitFor(() => {
            const element = container.querySelector('[id="endpoint-2"]');
            if (!element) throw new Error('Element not found');
            return element;
        });

        // trigger route fetch
        fireEvent.click(cityA);
        fireEvent.click(cityB);

        return { container, cityA, cityB };
    }

    // Setup and cleanup
    beforeEach(() => {
        vi.spyOn(console, 'log').mockImplementation(() => {});
        vi.spyOn(console, 'error').mockImplementation(() => {});
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    // Tests
    describe('fetch map data and display map', () => {
        it('renders the map and displays cities', async () => {
            // Mock Connection and fetch response
            globalThis.fetch = vi.fn().mockResolvedValueOnce({
                json: async () => mockConnection,
            } as Response);

            // Render the component
            await RenderInteractiveMapCities();

            // Check if the connection line is displayed
            const connectionLine = document.querySelector(
                'line[data-connection="City A-City B"]'
            );
            expect(connectionLine).toBeInTheDocument();
        });

        it('handles fetch errors for map data', async () => {
            // Mock fetch response
            globalThis.fetch = vi
                .fn()
                .mockRejectedValueOnce(new Error('Fetch error'));

            // Render the component
            render(<InteractiveMap />);

            // Wait for the map data fetch error to be logged
            await waitFor(() => {
                expect(console.error).toHaveBeenCalledWith(
                    'Error fetching map data:',
                    new Error('Fetch error')
                );
            });
        });

        it('handles missing city for connection', async () => {
            // Mock Connection and fetch response
            globalThis.fetch = vi.fn().mockResolvedValueOnce({
                json: async () => ({
                    cities: [
                        {
                            id: 1,
                            name: 'City A',
                            position_x: 100,
                            position_y: 200,
                        },
                        {
                            id: 2,
                            name: 'City B',
                            position_x: 300,
                            position_y: 400,
                        },
                    ],
                    connections: [{ parent_city_id: 1, child_city_id: 3 }],
                }),
            } as Response);

            // Render the component
            const { container } = await RenderInteractiveMapCities();

            // Check if the connection line is not displayed
            const lineElement = container.querySelector('line');
            expect(lineElement).not.toBeInTheDocument();
        });

        it('handles missing city in getCityNameById', async () => {
            // Mock map data and fetch response
            globalThis.fetch = vi.fn().mockResolvedValueOnce({
                json: async () => mockConnection,
            } as Response);

            // Prepare mocks of the `find` method which is also used in `getCityNameById`
            const mockFind = vi
                .fn()
                // first 8 calls are irrelevant
                .mockImplementationOnce(Array.prototype.find)
                .mockImplementationOnce(Array.prototype.find)
                .mockImplementationOnce(Array.prototype.find)
                .mockImplementationOnce(Array.prototype.find)
                .mockImplementationOnce(Array.prototype.find)
                .mockImplementationOnce(Array.prototype.find)
                .mockImplementationOnce(Array.prototype.find)
                .mockImplementationOnce(Array.prototype.find)
                .mockImplementationOnce(Array.prototype.find)
                // next 2 calls are to validate the existence of cities given in connection
                .mockImplementationOnce(Array.prototype.find)
                .mockImplementationOnce(Array.prototype.find)
                // last 2 calls are to validate the non-existence of cities given in connection
                // to validate, that getCityNameById returns empty string
                .mockReturnValueOnce(undefined)
                .mockReturnValueOnce(undefined);

            // Spy on the `find` method and mock it
            vi.spyOn(Array.prototype, 'find').mockImplementation(mockFind);

            // Render the component
            const { container } = render(<InteractiveMap />);

            // Check if `getCityNameById` returns an empty string for a non-existent city
            const element = await waitFor(() => {
                const element = container.querySelector(
                    'line[data-connection="-"]'
                );
                if (!element) throw new Error('Element not found');
                return element;
            });
            expect(element).toBeInTheDocument();

            // Cleanup: restore the mock
            mockFind.mockRestore();
        });
    });

    describe('fetch route data and display route', () => {
        it('fetches and displays route data', async () => {
            // Mock cities and route and fetch responses
            globalThis.fetch = vi
                .fn()
                .mockResolvedValueOnce({
                    json: async () => mockCities,
                } as Response)
                .mockResolvedValueOnce({
                    json: async () => mockRoute,
                } as Response);

            // Render the component and trigger route fetch
            await RenderInteractiveMapAndTriggerFetchRoute();

            // Check if the route line is displayed
            const routeLine = await screen.findByText(
                'Distance to destination: 5000 m'
            );
            expect(routeLine).toBeInTheDocument();
        });

        it('handles fetch errors for route data', async () => {
            // Mock Cities and fetch response
            globalThis.fetch = vi
                .fn()
                .mockResolvedValueOnce({
                    json: async () => mockCities,
                } as Response)
                .mockRejectedValueOnce(new Error('Fetch error'));

            // Render the component and trigger route fetch
            await RenderInteractiveMapAndTriggerFetchRoute();

            // Wait for the route data fetch error to be logged
            await waitFor(() => {
                expect(console.error).toHaveBeenCalledWith(
                    'Error fetching route data:',
                    new Error('Fetch error')
                );
            });
        });

        it('handles missing city for route', async () => {
            // Mock Cities und Route-Daten
            globalThis.fetch = vi
                .fn()
                .mockResolvedValueOnce({
                    json: async () => mockCities,
                } as Response)
                .mockResolvedValueOnce({
                    json: async () => ({
                        route: {
                            '0': 'City A',
                            '1': 'City C',
                        },
                        distance: 5000,
                    }),
                } as Response);

            // Render the component and trigger route fetch
            const { container } =
                await RenderInteractiveMapAndTriggerFetchRoute();

            // Stelle sicher, dass keine Linie gerendert wird, wenn Städte fehlen
            const notExistingLine = container.querySelector(
                'line[stroke="blue"]'
            );

            // Testen, dass die Linie nicht existiert
            expect(notExistingLine).not.toBeInTheDocument();
        });
    });

    describe('check functionalities', () => {
        it('sets startpoint, endpoint and resets on city click', async () => {
            // Mock City and fetch response
            globalThis.fetch = vi.fn().mockResolvedValueOnce({
                json: async () => mockCities,
            } as Response);

            // Render the component and trigger route fetch
            const { cityA } = await RenderInteractiveMapAndTriggerFetchRoute();

            // Check if the startpoint and endpoint are set
            expect(console.log).toHaveBeenCalledWith('Set startpoint: City A');
            expect(console.log).toHaveBeenCalledWith('Set endpoint: City B');

            // trigger reset
            fireEvent.click(cityA);

            // Check if the startpoint and endpoint are reset
            expect(console.log).toHaveBeenCalledWith('reset data');
        });

        it('toggles alternative route', async () => {
            // Mock cities, alternative route and fetch responses
            const mockRoute = {
                route: {
                    '0': 'City A',
                    '1': 'City B',
                },
                alternative_route: {
                    '0': 'City A',
                    '1': 'City B',
                },
                distance: 5000,
                alternative_distance: 7000,
            };

            globalThis.fetch = vi
                .fn()
                .mockResolvedValueOnce({ json: async () => mockCities })
                .mockResolvedValueOnce({ json: async () => mockRoute });

            // Render the component and trigger route fetch
            await RenderInteractiveMapAndTriggerFetchRoute();

            // get the toggle button and click it
            const toggleButton = screen.getByRole('button', {
                name: /show alternative route/i,
            });

            fireEvent.click(toggleButton);

            // Check if the alternative route line is displayed
            const alternativeDistance = await screen.findByText(
                'Distance to destination: 7000 m'
            );
            expect(alternativeDistance).toBeInTheDocument();
        });
    });
});
