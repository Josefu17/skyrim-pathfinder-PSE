import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`

import { Docs } from '../../src/pages/docs';
import { renderWithAuthProvider, mockFetch } from '../skip.support.test';

global.fetch = mockFetch;

describe('Docs', () => {
    it('should render documentation page', async () => {
        renderWithAuthProvider(Docs);
        const element = await waitFor(async () => {
            const element = await screen.findByText('Home');
            if (!element) throw new Error('Element not found');
            return element;
        });
        expect(element).toBeInTheDocument();
    });
});
