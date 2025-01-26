import { screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { App } from '../../src/App';
import { renderWithAuthProvider, mockFetch } from '../skip.support.test';
import { describe, expect, it } from 'vitest';

global.fetch = mockFetch;

describe('renders the App component without crashing', async () => {
    it('should render the App component', async () => {
        renderWithAuthProvider(App);

        await waitFor(() => {
            expect(screen.getByRole('banner')).toBeInTheDocument();
        });
        await waitFor(() => {
            expect(screen.getByRole('contentinfo')).toBeInTheDocument();
        });
        await waitFor(() => {
            expect(screen.getByText('Path finder')).toBeInTheDocument();
        });
        await waitFor(() => {
            expect(screen.getByText('Developers')).toBeInTheDocument();
        });
        await waitFor(() => {
            expect(screen.getByText('Arian Farzad')).toBeInTheDocument();
        });
        await waitFor(() => {
            expect(screen.getByText('Târik-Cemal Atis')).toBeInTheDocument();
        });
        await waitFor(() => {
            expect(screen.getByText('Yusuf Birdane')).toBeInTheDocument();
        });
    });
});
