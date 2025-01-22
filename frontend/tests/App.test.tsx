import { describe, expect, it, vi } from 'vitest';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`

import { renderWithAuthProvider } from './skip.support.test';
import { App } from '../src/App';

describe('App', () => {
    it('should render correctly', () => {
        globalThis.fetch = vi.fn().mockImplementation(() => {
            return {
                ok: true,
                json: async () => [],
            };
        });

        const { container } = renderWithAuthProvider(App);

        const leftSection = container.querySelector("[id='left']");
        const rightSection = container.querySelector("[id='right']");

        expect(leftSection).toBeInTheDocument();
        expect(rightSection).toBeInTheDocument();
    });
});
