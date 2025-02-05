import { describe, it, expect } from 'vitest';
import { fireEvent, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import { act } from 'react';

import { MapSelector } from '../../src/components/mapSelector';
import { renderWithContextProviders, mockFetch } from '../skip.support.test';

// Mock global fetch API
global.fetch = mockFetch;

describe('MapSelector Component', () => {
    it.skip('renders correctly and fetches map list', async () => {
        renderWithContextProviders(MapSelector);

        // Check if label and select elements are present
        expect(
            screen.getByLabelText(/choose a map to view/i)
        ).toBeInTheDocument();
        expect(
            screen.getByRole('combobox', { name: /choose a map to view/i })
        ).toBeInTheDocument();

        // Wait for map list to load
        await waitFor(() => {
            expect(
                screen.getByRole('option', { name: 'skyrim' })
            ).toBeInTheDocument();
        });

        // Check if the fetched map list is rendered in the dropdown
        const options = screen.getAllByRole('option');
        expect(options).toHaveLength(11); // Total number of maps in mock data
        expect(options.map((option) => option.textContent)).toContain('skyrim');
    });

    it.skip('updates the selected map when a new option is chosen', async () => {
        renderWithContextProviders(MapSelector);

        // Wait for map list to load
        await waitFor(() => {
            expect(
                screen.getByRole('option', { name: 'skyrim' })
            ).toBeInTheDocument();
        });

        // Check initial selected map
        expect(screen.getByText(/selected map: skyrim/i)).toBeInTheDocument();

        // Select a new map
        act(() => {
            fireEvent.change(
                screen.getByRole('combobox', { name: /choose a map to view/i }),
                {
                    target: { value: 'germany' },
                }
            );
        });

        // Verify selected map is updated
        expect(screen.getByText(/selected map: germany/i)).toBeInTheDocument();
    });

    it.skip("renders the InteractiveMap when 'skyrim' is selected", async () => {
        renderWithContextProviders(MapSelector);

        // Wait for map list to load
        await waitFor(() => {
            expect(
                screen.getByRole('option', { name: 'skyrim' })
            ).toBeInTheDocument();
        });

        // Verify InteractiveMap is rendered
        expect(screen.getByText(/selected map: skyrim/i)).toBeInTheDocument();
        expect(
            screen.queryByText(/Select your startpoint and endpoint/i)
        ).not.toBeInTheDocument();
    });

    it.skip('renders the StaticMap when a non-skyrim map is selected', async () => {
        renderWithContextProviders(MapSelector, null, {id: 10, name: 'germany'});	

        // Wait for map list to load
        await waitFor(() => {
            expect(
                screen.getByRole('option', { name: 'germany' })
            ).toBeInTheDocument();
        });

        // Select a non-skyrim map
        act(() => {
            fireEvent.change(
                screen.getByRole('combobox', { name: /choose a map to view/i }),
                {
                    target: { value: 'germany' },
                }
            );
        });

        // Verify StaticMap is rendered
        expect(screen.getByText(/selected map: germany/i)).toBeInTheDocument();
        expect(
            screen.getByText(/Select your startpoint and endpoint/i)
        ).toBeInTheDocument(); // Assuming StaticMap renders this text
    });

    // TODO: adjust and activate after fetching data from the API instead of using mock data is implemented
    it.skip('handles fetch error gracefully', async () => {
        // Mock fetch to simulate an error
        mockFetch.mockImplementationOnce(() =>
            Promise.reject(new Error('Network Error'))
        );

        renderWithContextProviders(MapSelector);

        await waitFor(() => {
            expect(screen.queryAllByRole('option')).not.toBeInTheDocument();
        });

        // Check if error message is logged
        expect(console.log).toHaveBeenCalledWith(
            'error fetching map list',
            expect.any(Error)
        );
    });
});
