import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React from 'react';

import { Footer } from '../../src/components/footer';

describe('Footer', () => {
    it('should render correctly', async () => {
        render(<Footer />);

        const footer = screen.getByText('Developers');

        expect(footer).toBeInTheDocument();
    });
});
