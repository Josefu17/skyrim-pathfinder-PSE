import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React from 'react';

import { AppRoutes } from '../../src/routes/app_routes';

describe('App Routes', () => {
    it('should render the Home page', async () => {
        const { container } = render(
            <MemoryRouter initialEntries={['/']}>
                <AppRoutes />
            </MemoryRouter>
        );

        const element = container.querySelector('[id="map"]');
        expect(element).toBeInTheDocument();
    });

    it('should render the Docs page', async () => {
        render(
            <MemoryRouter initialEntries={['/Docs']}>
                <AppRoutes />
            </MemoryRouter>
        );

        const element = await screen.findByText(
            'This is the documentation page'
        );
        expect(element).toBeInTheDocument();
    });
});
