import { describe, expect, it, vi } from 'vitest';
import { screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React, { act, useState } from 'react';

import { RouteEntry } from '../../src/components/routeEntry';
import {
    renderWithAuthProvider,
    testUser,
    mockRouteData,
} from '../skip.support.test';

describe('RouteEntry', () => {
    it('should display route data and toggle expanded view on button click', async () => {
        renderWithAuthProvider(
            () => (
                <RouteEntry
                    routeId={mockRouteData.id}
                    routeData={mockRouteData}
                    isDeleting={false}
                    onSelection={() => {}}
                />
            ),
            testUser
        );

        // Check if the button is displayed with the correct values
        expect(screen.getByRole('button')).toHaveValue(
            'Karthwasten to Rorikstead'
        );

        // Click the button to expand the view
        const button = screen.getByRole('button');
        act(() => {
            fireEvent.click(button);
        });

        // Check if the `pre` tag with the correct JSON content is displayed
        expect(
            screen.getByText(/"alternative_distance": 877.25/)
        ).toBeInTheDocument();
        expect(screen.getByText(/"distance": 362.94/)).toBeInTheDocument();

        // Click again to collapse the view
        act(() => {
            fireEvent.click(button);
        });

        // Check if the `pre` tag is no longer displayed
        expect(screen.queryByText(/"distance": 362.94/)).toBeNull();
    });

    it('should call onSelection when isDeleting is true', () => {
        const mockOnSelection = vi.fn();

        renderWithAuthProvider(
            () => (
                <RouteEntry
                    routeId={mockRouteData.id}
                    routeData={mockRouteData}
                    isDeleting={true}
                    onSelection={mockOnSelection}
                />
            ),
            testUser
        );

        // Click the button when `isDeleting` is true
        act(() => {
            fireEvent.click(screen.getByRole('button'));
        });

        // Check if the `onSelection` function was called with the correct `routeId`
        expect(mockOnSelection).toHaveBeenCalledWith(mockRouteData.id);
    });

    it('should render correctly with isDeleting as false', () => {
        renderWithAuthProvider(
            () => (
                <RouteEntry
                    routeId={mockRouteData.id}
                    routeData={mockRouteData}
                    isDeleting={false}
                    onSelection={() => {}}
                />
            ),
            testUser
        );

        // Check if the button is displayed
        const button = screen.getByRole('button');
        expect(button).toHaveValue('Karthwasten to Rorikstead');

        // Check that `pre` is not displayed on initial render
        expect(screen.queryByText(/"distance":/)).toBeNull();
    });

    it('should render correctly with isDeleting as true', () => {
        renderWithAuthProvider(
            () => (
                <RouteEntry
                    routeId={mockRouteData.id}
                    routeData={mockRouteData}
                    isDeleting={true}
                    onSelection={() => {}}
                />
            ),
            testUser
        );

        // Check if the button is displayed
        const button = screen.getByRole('button');
        expect(button).toHaveValue('Karthwasten to Rorikstead');
    });

    const TestComponent = () => {
        const [isDeleting, setIsDeleting] = useState(false);

        // Function to set isDeleting to true
        const toggleDeleting = () => {
            setIsDeleting((prev) => !prev);
        };

        return (
            <div>
                {isDeleting ? (
                    <button onClick={toggleDeleting}>Exit deletion mode</button>
                ) : (
                    <button onClick={toggleDeleting}>
                        Enter deletion mode
                    </button>
                )}
                <RouteEntry
                    routeId={mockRouteData.id}
                    routeData={mockRouteData}
                    isDeleting={isDeleting}
                    onSelection={() => {}}
                />
            </div>
        );
    };

    it('should also allow expanded view in deletion mode', () => {
        renderWithAuthProvider(TestComponent, testUser);

        // Click the button to expand the view
        const button = screen.getByRole('button', {
            name: 'Karthwasten to Rorikstead',
        });

        act(() => {
            fireEvent.click(button);
        });

        // Check if the `pre` tag with the correct JSON content is displayed
        expect(
            screen.getByText(/"alternative_distance": 877.25/)
        ).toBeInTheDocument();
        expect(screen.getByText(/"distance": 362.94/)).toBeInTheDocument();

        // Initially check if isDeleting is false
        const enterDeletionButton = screen.getByText('Enter deletion mode');
        expect(enterDeletionButton).toBeInTheDocument();

        // Click the button to set isDeleting
        act(() => {
            fireEvent.click(enterDeletionButton);
        });

        // Check if isDeleting is now true
        const exitDeletionButton = screen.getByText('Exit deletion mode');
        expect(exitDeletionButton).toBeInTheDocument();

        expect(exitDeletionButton).toBeInTheDocument();

        // Check if the `pre` tag with the correct JSON content is still displayed
        expect(
            screen.getByText(/"alternative_distance": 877.25/)
        ).toBeInTheDocument();
        expect(screen.getByText(/"distance": 362.94/)).toBeInTheDocument();
    });
});
