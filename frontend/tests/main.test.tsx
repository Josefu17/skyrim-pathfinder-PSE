import { vi, describe, expect, it, Mock } from 'vitest';
import { waitFor } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React, { StrictMode } from 'react';

import { AuthProvider } from '../src/contexts/authContext';
import { App } from '../src/App';

// Mock the `react-dom/client` module
vi.mock('react-dom/client', () => ({
    createRoot: vi.fn(),
}));

describe('Root rendering', () => {
    it('should call createRoot and render the app', async () => {
        // Mock `document.getElementById`
        const rootElement = document.createElement('div');
        rootElement.id = 'root';
        document.body.appendChild(rootElement);

        // Import the mocked `createRoot`
        const { createRoot } = await import('react-dom/client');
        const renderMock = vi.fn();
        (createRoot as Mock).mockReturnValue({ render: renderMock });

        // Import and execute the code
        await import('../src/main'); // Dynamischer Import des Entry Points

        // Assertions
        await waitFor(() => {
            expect(createRoot).toHaveBeenCalledWith(rootElement);
            expect(renderMock).toHaveBeenCalledWith(
                <StrictMode>
                    <AuthProvider>
                        <App />
                    </AuthProvider>
                </StrictMode>
            );
        });

        // Cleanup
        document.body.removeChild(rootElement);
        vi.resetAllMocks();
    });
});
