import { describe, it, expect } from 'vitest';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`

import { renderWithContextProviders, mockFetch } from '../skip.support.test';
import { Home } from '../../src/pages/home';
import { waitFor } from '@testing-library/react';

global.fetch = mockFetch;

describe('Home Page', async () => {
    it('should render an interactive map', async () => {
        const { container } = renderWithContextProviders(Home, null, { id: 1, name: 'skyrim' });

        const map = await waitFor(() => {
            const element = container.querySelector("[id='map']");
            if (!element) throw new Error('Map not found');
            return element;
        });
        expect(map).toBeInTheDocument();
    });
});
