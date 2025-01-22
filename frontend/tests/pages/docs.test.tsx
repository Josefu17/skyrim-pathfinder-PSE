import { describe, expect, it } from 'vitest';
import { screen } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`

import { Docs } from '../../src/pages/docs';
import { renderWithAuthProvider } from '../skip.support.test';

describe('Docs', () => {
    it('should render documentation page', async () => {
        renderWithAuthProvider(Docs);
        const element = await screen.findByText('Home');
        expect(element).toBeInTheDocument();
    });
});
