import { describe, expect, it } from 'vitest';
import { findByText, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React from 'react';

import {
    changePage,
    mockFetch,
    renderWithContextProviders,
    testMap,
    testUser,
} from '../skip.support.test';
import { AppRoutes } from '../../src/routes/appRoutes';
import { App } from '../../src/App';

global.fetch = mockFetch;

describe('App Routes', () => {
    it('should render the Home page', async () => {
        const { container } = renderWithContextProviders(() => (
            <MemoryRouter initialEntries={['/']}>
                <AppRoutes />
            </MemoryRouter>
        ));

        const element = container.querySelector('[id="map"]');
        expect(element).toBeInTheDocument();
    });

    it('should render the Docs page', async () => {
        renderWithContextProviders(() => (
            <MemoryRouter initialEntries={['/Docs']}>
                <AppRoutes />
            </MemoryRouter>
        ));

        const element = await screen.findByText('Home');
        expect(element).toBeInTheDocument();
    });

    it('should render the Routes History page', async () => {
        const { container } = renderWithContextProviders(App, testUser, testMap);

        await changePage(container, '/routes-history');

        const element = await waitFor(() => {
            const element = findByText(container, 'Routes History of test');

            if (!element) throw new Error('Element not found');
            return element;
        });

        // Assert
        expect(element).toBeInTheDocument();
    });
});
