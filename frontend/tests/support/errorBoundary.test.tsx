import { describe, expect, it, vi, Mock } from 'vitest';
import { fireEvent, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import { useNavigate } from 'react-router-dom';
import React, { act } from 'react';

import {
    ErrorBoundary,
    ErrorBoundaryClass,
} from '../../src/support/errorBoundary';
import { ErrorBoundaryProps } from '../../src/types';
import { ErrorComponent, renderWithAuthProvider } from '../skip.support.test';

describe('ErrorBoundary', () => {
    it('should set hasError state to true when getDerivedStateFromError is called', () => {
        const state = ErrorBoundaryClass.getDerivedStateFromError();

        expect(state.hasError).toBe(true);
    });

    it('should call componentDidCatch and log the error', () => {
        const spy = vi.spyOn(console, 'error'); // Spy on console.error
        const instance = new ErrorBoundaryClass({} as ErrorBoundaryProps);

        instance.componentDidCatch(new Error('Test error'), {
            componentStack: 'test stack',
        });

        expect(spy).toHaveBeenCalledWith(
            'ErrorBoundary caught an error:',
            expect.any(Error),
            expect.any(Object)
        );

        spy.mockRestore(); // Reset spy
    });

    it('should navigate to home when handleGoHome is called', () => {
        const mockNavigate = vi.fn(); // Mock navigation function
        const instance = new ErrorBoundaryClass({
            navigate: mockNavigate,
            fallback: <div>Error</div>,
            children: <div />,
        } as ErrorBoundaryProps);

        // Set the error state to true
        instance.setState({ hasError: true });

        // Simulate button click (handleGoHome is called)
        instance.handleGoHome();

        // Check if navigate led to the homepage
        expect(mockNavigate).toHaveBeenCalledWith('/');
    });

    it('should render fallback UI and a home button when there is an error', async () => {
        const mockNavigate = vi.fn();

        renderWithAuthProvider(() => (
            <ErrorBoundaryClass
                navigate={mockNavigate}
                fallback={<p>Error Occurred</p>}
            >
                <ErrorComponent />
            </ErrorBoundaryClass>
        ));

        // Check if the fallback UI was rendered
        const element = await waitFor(() => screen.getByText('Error Occurred'));
        expect(element).toBeInTheDocument();

        // Check if the button is present
        const button = screen.getByText(/Startpage/i);
        expect(button).toBeInTheDocument();

        // Simulate a click on the button
        act(() => {
            fireEvent.click(button);
        });

        // Check if the navigation occurred
        expect(mockNavigate).toHaveBeenCalledWith('/');
    });
});

describe('ErrorBoundary (HOC(Higher-Order Component))', () => {
    it('should pass the navigate function to ErrorBoundaryClass', () => {
        vi.mock('react-router-dom', async () => {
            const actual = await vi.importActual('react-router-dom');
            return {
                ...actual,
                useNavigate: vi.fn(), // Mock the useNavigate function
            };
        });
        (useNavigate as Mock).mockReturnValue(vi.fn());

        const { container } = renderWithAuthProvider(() => (
            <ErrorBoundary fallback={<p>Error Occurred</p>}>
                <ErrorComponent />
            </ErrorBoundary>
        ));

        // Ensure that the ErrorBoundaryClass was rendered
        expect(container).toBeInTheDocument();

        // Check if the navigate function was correctly passed
        expect(ErrorBoundaryClass).toBeTruthy(); // Check that the class exists
        expect(useNavigate).toHaveBeenCalled();
    });
});
