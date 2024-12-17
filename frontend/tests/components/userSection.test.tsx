import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import '@testing-library/jest-dom';
import React, { act } from 'react';

import { UserSection } from '../../src/components/userSection';

describe('UserSection', () => {
    it('should render correctly', async () => {
        render(<UserSection />);

        // Use screen to find the submit button
        const switchRegisterSectionButton = await screen.findByRole('button', {
            name: /Register now/i,
        });

        // Check if the button is in the document
        expect(switchRegisterSectionButton).toBeInTheDocument();

        // Check if the Register component is not in the document
        const registerComponent = screen.queryByText(/username/i);

        // Assert that the Register component is not in the document
        expect(registerComponent).not.toBeInTheDocument();
    });

    it('should show Register component when button is clicked', async () => {
        render(<UserSection />);

        // Use screen to find the submit button
        const switchRegisterSectionButton = await screen.findByRole('button', {
            name: /Register now/i,
        });

        // Click the button
        await act(() => {
            switchRegisterSectionButton.click();
        });

        // Check if the Register component is in the document
        const registerComponent = await screen.findByText(/username/i);
        expect(registerComponent).toBeInTheDocument();
    });
});
