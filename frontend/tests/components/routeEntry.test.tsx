import { describe, expect, it, vi } from 'vitest';
import { screen, fireEvent, within } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import React, { act, useState } from 'react';

import { RouteEntry } from '../../src/components/routeEntry';
import {
    renderWithContextProviders,
    testUser,
    mockRouteData,
} from '../skip.support.test';

describe('RouteEntry', () => {
    it.skip('should display route data and toggle expanded view on button click', async () => {
        renderWithContextProviders(
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

        renderWithContextProviders(
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
        renderWithContextProviders(
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
        renderWithContextProviders(
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

    it.skip('should also allow expanded view in deletion mode', () => {
        renderWithContextProviders(TestComponent, testUser);

        // Click the button to expand the view
        const button = screen.getByRole('button', {
            name: 'Karthwasten to Rorikstead',
        });

        act(() => {
            fireEvent.click(button);
        });

        // Eindeutig prüfen, ob alternative_distance und distance in einem <strong> existieren
        const altDistanceLabel = screen.getByText('alternative_distance', {
            selector: 'strong',
        });
        expect(altDistanceLabel).toBeInTheDocument();

        const distanceLabel = screen.getByText('distance', { selector: 'strong' });
        expect(distanceLabel).toBeInTheDocument();

        // Die dazugehörigen Werte in <span> suchen (genau zugeordnet)
        const altDistanceValue = screen.getByText('877.25', { selector: 'span' });
        expect(altDistanceValue).toBeInTheDocument();

        const distanceValue = screen.getByText('362.94', { selector: 'span' });
        expect(distanceValue).toBeInTheDocument();

        // alternative_route finden & prüfen
        const altRouteLabel = screen.getByText('alternative_route', {
            selector: 'strong',
        });
        expect(altRouteLabel).toBeInTheDocument();

        // Liste der `alternative_route` Einträge durchsuchen
        const altRouteList = within(altRouteLabel.closest('li')!).getByRole('list');
        expect(
            within(altRouteList).getByText('0', { selector: 'strong' })
        ).toBeInTheDocument();
        expect(within(altRouteList).getByText('Karthwasten')).toBeInTheDocument();
        expect(
            within(altRouteList).getByText('1', { selector: 'strong' })
        ).toBeInTheDocument();
        expect(within(altRouteList).getByText('Markarth')).toBeInTheDocument();
        expect(
            within(altRouteList).getByText('2', { selector: 'strong' })
        ).toBeInTheDocument();
        expect(within(altRouteList).getByText('Rorikstead')).toBeInTheDocument();

        // route finden & prüfen
        const routeLabel = screen.getByText('route', { selector: 'strong' });
        expect(routeLabel).toBeInTheDocument();

        const routeList = within(routeLabel.closest('li')!).getByRole('list');
        expect(
            within(routeList).getByText('0', { selector: 'strong' })
        ).toBeInTheDocument();
        expect(within(routeList).getByText('Karthwasten')).toBeInTheDocument();
        expect(
            within(routeList).getByText('1', { selector: 'strong' })
        ).toBeInTheDocument();
        expect(within(routeList).getByText('Rorikstead')).toBeInTheDocument();

        // Deletion Mode prüfen
        const enterDeletionButton = screen.getByText('Enter deletion mode');
        expect(enterDeletionButton).toBeInTheDocument();

        act(() => {
            fireEvent.click(enterDeletionButton);
        });

        const exitDeletionButton = screen.getByText('Exit deletion mode');
        expect(exitDeletionButton).toBeInTheDocument();
    });
});
