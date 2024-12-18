import { describe, expect, it } from 'vitest';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React from 'react';

import { renderWithAuthProvider } from './skip.support.test';
import { App } from '../src/App';

describe('App', () => {
    it('should render correctly', () => {
        const { container } = renderWithAuthProvider(<App />);

        const leftSection = container.querySelector("[id='left']");
        const rightSection = container.querySelector("[id='right']");

        expect(leftSection).toBeInTheDocument();
        expect(rightSection).toBeInTheDocument();
    });
});
