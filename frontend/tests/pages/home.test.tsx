import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React from 'react';

import { Home } from '../../src/pages/home';

describe('Home Page', () => {
    it('should render an interactive map', () => {
        const { container } = render(<Home />);

        const map = container.querySelector("[id='map']");
        expect(map).toBeInTheDocument();
    });
});
