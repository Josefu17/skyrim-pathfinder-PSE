import { describe, it, expect } from 'vitest';
import { findByText, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`

import {
    renderWithContextProviders,
    testUser,
    mockFetch,
} from '../skip.support.test';
import { RoutesHistory } from '../../src/pages/routesHistory';

global.fetch = mockFetch;

describe('Routes History Page', () => {
    it('should render a page with routes history', async () => {
        // Arrange
        const { container } = renderWithContextProviders(
            RoutesHistory,
            testUser
        );

        // Act
        const element = await waitFor(() => {
            const element = findByText(container, 'Routes History of test');
            if (!element) throw new Error('Element not found');
            return element;
        });

        // Assert
        expect(element).toBeInTheDocument();
    });
});
