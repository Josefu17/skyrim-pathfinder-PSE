import { describe, expect, it } from 'vitest';
import { screen } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like toBeInTheDocument
import React from 'react';
import { MemoryRouter } from 'react-router-dom'; // Import MemoryRouter for test context

import { renderWithAuthProvider } from '../skip.support.test';
import { Header } from '../../src/components/header';

describe('Header', () => {
    it('should render correctly', async () => {
        // Wrap the Header with MemoryRouter to provide router context
        renderWithAuthProvider(
            <MemoryRouter>
                <Header />
            </MemoryRouter>
        );

        const header = screen.getByText('Path finder');

        expect(header).toBeInTheDocument();
    });
});
