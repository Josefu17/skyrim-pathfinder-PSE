import { screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import '@testing-library/jest-dom'; // For better matchers like `toBeInTheDocument`
import React, { act } from 'react';

import { renderWithAuthProvider } from '../skip.support.test';
import { UserSection } from '../../src/components/userSection';
import { TUser } from '../../src/types';

describe('UserSection', () => {
    it('should render correctly without showing Register or Login forms initially', async () => {
        renderWithAuthProvider(<UserSection />);

        // Check if the Register button is visible
        const switchRegisterSectionButton = screen.getByRole('button', {
            name: /Register now/i,
        });
        expect(switchRegisterSectionButton).toBeInTheDocument();

        // Check if the Login button is visible
        const switchLoginSectionButton = screen.getByRole('button', {
            name: /Login now/i,
        });
        expect(switchLoginSectionButton).toBeInTheDocument();

        // Initially, no form should be visible
        const registerComponent = screen.queryByText(/username/i);
        const loginComponent = screen.queryByText(/username/i);

        // Assert that neither Register nor Login form is displayed
        expect(registerComponent).not.toBeInTheDocument();
        expect(loginComponent).not.toBeInTheDocument();
    });

    it('should show Register component when "Register now" button is clicked', async () => {
        renderWithAuthProvider(<UserSection />);

        // Find the "Register now" button
        const switchRegisterSectionButton = screen.getByRole('button', {
            name: /Register now/i,
        });

        // Simulate clicking the Register button
        await act(async () => {
            fireEvent.click(switchRegisterSectionButton);
        });

        // Check if the Register form is displayed
        const registerComponent = screen.getByText(/Username/i);
        expect(registerComponent).toBeInTheDocument();
    });

    it('should hide Register component when "Register now" button is clicked again', async () => {
        renderWithAuthProvider(<UserSection />);

        // Find the "Register now" button and click it to show the Register form
        const switchRegisterSectionButton = screen.getByRole('button', {
            name: /Register now/i,
        });

        await act(async () => {
            fireEvent.click(switchRegisterSectionButton);
        });

        // Ensure the Register form is displayed
        const registerComponent = screen.getByText(/Username/i);
        expect(registerComponent).toBeInTheDocument();

        // Click the "Register now" button again to hide the form
        await act(async () => {
            fireEvent.click(switchRegisterSectionButton);
        });

        // Assert that the Register form is no longer in the document
        expect(registerComponent).not.toBeInTheDocument();
    });

    it('should show Login component when "Login now" button is clicked', async () => {
        renderWithAuthProvider(<UserSection />);

        // Find the "Login now" button
        const switchLoginSectionButton = screen.getByRole('button', {
            name: /Login now/i,
        });

        // Simulate clicking the Login button
        await act(async () => {
            fireEvent.click(switchLoginSectionButton);
        });

        // Check if the Login form is displayed
        const loginComponent = screen.getByText(/Username/i);
        expect(loginComponent).toBeInTheDocument();
    });

    it('should hide Login component when "Login now" button is clicked again', async () => {
        renderWithAuthProvider(<UserSection />);

        // Find the "Login now" button and click it to show the Login form
        const switchLoginSectionButton = screen.getByRole('button', {
            name: /Login now/i,
        });

        await act(async () => {
            fireEvent.click(switchLoginSectionButton);
        });

        // Ensure the Login form is displayed
        const loginComponent = screen.getByText(/Username/i);
        expect(loginComponent).toBeInTheDocument();

        // Click the "Login now" button again to hide the form
        await act(async () => {
            fireEvent.click(switchLoginSectionButton);
        });

        // Assert that the Login form is no longer in the document
        expect(loginComponent).not.toBeInTheDocument();
    });

    it.skip('should render Logout button if user is logged in', async () => {
        const mockUser: TUser = { id: 1, username: 'test_user' };

        renderWithAuthProvider(<UserSection />, mockUser);

        // Wait for the user to be set in the context
        await waitFor(() => {
            const logoutButton = screen.getByRole('button', {
                name: /Logout/i,
            });
            expect(logoutButton).toBeInTheDocument();
        });
    });
});
