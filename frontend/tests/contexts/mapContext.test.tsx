import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import React from 'react';

import { useMap } from '../../src/contexts/mapContext';
import { renderWithContextProviders, testMap } from '../skip.support.test';
import { MAP } from '../../src/support/support';

describe('MapContext', () => {
    beforeEach(() => {
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation((key) => {
            if (key === MAP) {
                return JSON.stringify(testMap);
            }
            return null;
        });

        vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {});
        vi.spyOn(Storage.prototype, 'removeItem').mockImplementation(() => {});
    });

    afterEach(() => {
        vi.clearAllMocks();
    });

    const TestComponent = () => {
        const { currentMap } = useMap();
        return <p>{currentMap ? `Map: ${currentMap.name}` : 'No map'}</p>;
    };

    it('should load currentMap from localStorage on initial render', () => {

        renderWithContextProviders(TestComponent, null, testMap);

        expect(screen.getByText(`Map: ${testMap.name}`)).toBeInTheDocument();
    });

    it('should set currentMap to default if no data exists in localStorage', () => {
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => null);

        renderWithContextProviders(TestComponent);

        expect(screen.getByText('Map: skyrim')).toBeInTheDocument();
    });

    it('should set currentMap to null if localStorage contains invalid JSON', () => {
        const consoleErrorSpy = vi
            .spyOn(console, 'error')
            .mockImplementation(() => {});

        renderWithContextProviders(
            TestComponent,
            null,
            null,
            {},
            { useLocal: true, localStorage: 'invalid JSON' }
        );

        expect(screen.getByText('No map')).toBeInTheDocument();
        expect(consoleErrorSpy).toHaveBeenCalledWith(
            'Failed to parse currentMap from localStorage',
            expect.any(Error)
        );

        consoleErrorSpy.mockRestore();
    });

    it('should throw an error if useMap is used outside of MapProvider', () => {
        const TestComponent = () => {
            useMap();
            return <p>Test</p>;
        };

        expect(() => render(<TestComponent />)).toThrowError(
            'useMap must be used within an MapProvider'
        );
    });
});
