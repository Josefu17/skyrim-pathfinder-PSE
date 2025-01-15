import { describe, it, expect } from 'vitest';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React from 'react';

import { renderWithAuthProvider } from '../skip.support.test';
import { Home } from '../../src/pages/home';

describe('Home Page', () => {
    it('should render an interactive map', () => {
        const { container } = renderWithAuthProvider(<Home />);

        const map = container.querySelector("[id='map']");
        expect(map).toBeInTheDocument();
    });
});
