import { screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { App } from '../../src/App';
import { renderWithAuthProvider } from '../skip.support.test';
import { describe, expect, it } from 'vitest';

describe('renders the App component without crashing', async () => {
    it('should render the App component', async () => {
        renderWithAuthProvider(App);

        await waitFor(() => {
            expect(screen.getByRole('banner')).toBeInTheDocument();
            expect(screen.getByRole('contentinfo')).toBeInTheDocument();
            expect(screen.getByText('Path finder')).toBeInTheDocument();
            expect(screen.getByText('Developers')).toBeInTheDocument();
            expect(screen.getByText('Arian Farzad')).toBeInTheDocument();
            expect(screen.getByText('Târik-Cemal Atis')).toBeInTheDocument();
            expect(screen.getByText('Yusuf Birdane')).toBeInTheDocument();
        });
    });
});
