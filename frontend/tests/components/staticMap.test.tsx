import { describe, it, vi, expect, beforeEach } from 'vitest';
import { fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matchers like `toBeInTheDocument`
import { act } from 'react';

import { renderWithContextProviders, testMap, testUser } from '../skip.support.test';
import { StaticMap } from '../../src/components/staticMap';

describe('StaticMap Component', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    afterEach(() => {
        vi.clearAllMocks();
    });

    it.skip('renders the StaticMap component correctly', () => {
        renderWithContextProviders(StaticMap, testUser, testMap);

        expect(
            screen.getByText('Select your startpoint and endpoint')
        ).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Startpoint')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Endpoint')).toBeInTheDocument();
        expect(screen.getByDisplayValue('Calculate Route')).toBeInTheDocument();
        expect(screen.getByText('No route requested.')).toBeInTheDocument();
    });

    it('updates input fields when typing', () => {
        renderWithContextProviders(StaticMap, testUser, testMap);

        const startpointInput = screen.getByPlaceholderText('Startpoint');
        const endpointInput = screen.getByPlaceholderText('Endpoint');
        act(() => {
            fireEvent.change(startpointInput, {
                target: { value: 'Karthwasten' },
            });
        });
        act(() => {
            fireEvent.change(endpointInput, {
                target: { value: 'Rorikstead' },
            });
        });

        expect((startpointInput as HTMLInputElement).value).toBe('Karthwasten');
        expect((endpointInput as HTMLInputElement).value).toBe('Rorikstead');
    });

    it.skip('fetches and displays route data when the button is clicked', async () => {
        renderWithContextProviders(StaticMap, testUser, testMap);

        const startpointInput = screen.getByPlaceholderText('Startpoint');
        const endpointInput = screen.getByPlaceholderText('Endpoint');
        const calculateButton = screen.getByDisplayValue('Calculate Route');

        act(() => {
            fireEvent.change(startpointInput, {
                target: { value: 'Karthwasten' },
            });
        });
        act(() => {
            fireEvent.change(endpointInput, {
                target: { value: 'Rorikstead' },
            });
        });
        act(() => {
            fireEvent.click(calculateButton);
        });

        // Wait for the mocked route data to appear
        await screen.findByText(/"alternative_distance": 877.25/);

        expect(
            screen.getByText(/"startpoint": "Karthwasten"/)
        ).toBeInTheDocument();
        expect(
            screen.getByText(/"endpoint": "Rorikstead"/)
        ).toBeInTheDocument();
    });

    it.skip('does not fetch route data if input fields are empty', () => {
        renderWithContextProviders(StaticMap, testUser, testMap);

        const calculateButton = screen.getByDisplayValue('Calculate Route');
        act(() => {
            fireEvent.click(calculateButton);
        });

        expect(
            screen.queryByText(/"alternative_distance":/)
        ).not.toBeInTheDocument();
    });

    it.skip('handles the absence of a user in the auth context', () => {
        const spy = vi.spyOn(console, 'log');

        renderWithContextProviders(
            StaticMap,
            null,
            {},
            { useLocal: true, localStorage: null }
        );

        const startpointInput = screen.getByPlaceholderText('Startpoint');
        const endpointInput = screen.getByPlaceholderText('Endpoint');
        const calculateButton = screen.getByText('Calculate Route');

        act(() => {
            fireEvent.change(startpointInput, {
                target: { value: 'Karthwasten' },
            });
        });
        act(() => {
            fireEvent.change(endpointInput, {
                target: { value: 'Rorikstead' },
            });
        });
        act(() => {
            fireEvent.click(calculateButton);
        });

        expect(spy).toHaveBeenNthCalledWith(1, 'user: ', null);
    });
});
