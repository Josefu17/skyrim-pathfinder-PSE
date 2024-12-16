import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React from 'react';

import { Docs } from '../../src/pages/docs';

describe('Docs', () => {
    it('should render documentation page', async () => {
        render(<Docs />);
        const element = await screen.findByText(
            'This is the documentation page'
        );
        expect(element).toBeInTheDocument();
    });
});
