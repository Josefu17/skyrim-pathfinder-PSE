import { AuthProvider, useAuth } from '../src/contexts/authContext';
import { MapProvider, useMap } from '../src/contexts/mapContext';
import { fireEvent, render, waitFor } from '@testing-library/react';
import React, { act, useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import { TMap, TUser } from '../src/types';
import { vi } from 'vitest';

// Rendering function that wraps the component in the AuthProvider
export const renderWithContextProviders = (
    Component: React.ElementType,
    user: TUser | null = null,
    map: TMap | null = null,
    props: Record<string, string | number | boolean | object> = {},
    mockLocal: TUseLocal = { useLocal: false, localStorage: null },
) => {
    const queryClient = createMockQueryClient();

    return render(
        <QueryClientProvider client={queryClient}>
            <AuthProvider>
                {user || mockLocal.useLocal ? (
                    <AuthProviderWithUser user={user} mockLocal={mockLocal}>
                        <MapProvider>
                            {map || mockLocal.useLocal ? (
                                <MapProviderWithMap
                                    map={map}
                                    mockLocal={mockLocal}
                                >
                                    <Component {...props} />
                                </MapProviderWithMap>
                            ) : (
                                <Component {...props} />
                            )}
                        </MapProvider>
                    </AuthProviderWithUser>
                ) : (
                    <MapProvider>
                        {map || mockLocal.useLocal ? (
                            <MapProviderWithMap map={map} mockLocal={mockLocal}>
                                <Component {...props} />
                            </MapProviderWithMap>
                        ) : (
                            <Component {...props} />
                        )}
                    </MapProvider>
                )}
            </AuthProvider>
        </QueryClientProvider>,
        {}
    );
};

// AuthProviderWithUser sets the user context for the test
const AuthProviderWithUser = ({
    children,
    user,
    mockLocal,
}: {
    children: React.ReactNode;
    user: TUser | null;
    mockLocal: TUseLocal;
}) => {
    const { setUser, loading } = useAuth();

    if (mockLocal.useLocal) {
        vi.spyOn(
            Object.getPrototypeOf(window.localStorage),
            'getItem'
        ).mockImplementation(() => mockLocal.localStorage);
    }

    useEffect(() => {
        setUser(user); // Set the user in the context
    }, [loading]);

    if (loading) {
        return <div>Loading...</div>;
    }

    return <>{children}</>;
};

// MapProviderWithMap sets the map context for the test
const MapProviderWithMap = ({
    children,
    map,
    mockLocal,
}: {
    children: React.ReactNode;
    map: TMap | null;
    mockLocal: TUseLocal;
}) => {
    const { setCurrentMap, loading } = useMap();

    if (mockLocal.useLocal) {
        vi.spyOn(
            Object.getPrototypeOf(window.localStorage),
            'getItem'
        ).mockImplementation(() => mockLocal.localStorage);
    }

    useEffect(() => {
        setCurrentMap(map); // Set the map in the context
    }, [loading]);

    if (loading) {
        return <div>Loading...</div>;
    }

    return <>{children}</>;
};

type TUseLocal = {
    useLocal: boolean;
    localStorage: TUser | TMap | string | null | undefined;
};

// Mocks for the tests

export const testUser: TUser = {
    id: 1,
    username: 'test',
};

export const testMap: TMap = {
    id: 1,
    name: 'skyrim',
};

// Mock data for the map and routes
export const mockFetch = vi.fn().mockImplementation(async (url) => {
    if (url.includes('/users/1/maps/1/routes')) {
        return {
            ok: true,
            json: async () => mockRoutesData,
        };
    } else if (url.includes('/cities?map_id=')) {
        return {
            ok: true,
            json: async () => ({
                cities: mockCitiesWithoutConnections,
            }),
        };
    } else if (url.includes('/maps?name')) {
        return {
            ok: true,
            json: async () => mockMapData,
        };
    } else if (url.includes('README.md')) {
        return Promise.resolve({
            ok: true,
            text: () => Promise.resolve('[Main Documentation](../other.md)'),
        });
    } else if (url.includes('/maps')) {
        return {
            ok: true,
            json: async () => mockMapList,
        };
    }
    return Promise.reject(new Error('Not Found'));
});

export const mockConnection = {
    cities: [
        { id: 1, name: 'City A', position_x: 100, position_y: 200 },
        { id: 2, name: 'City B', position_x: 300, position_y: 400 },
    ],
    connections: [{ parent_city_id: 1, child_city_id: 2 }],
};

export const mockCitiesWithoutConnections = {
    cities: [
        { id: 1, name: 'City A', position_x: 100, position_y: 200 },
        { id: 2, name: 'City B', position_x: 300, position_y: 400 },
    ],
    connections: [],
};

export const mockCities = {
    cities: [
        { name: 'City A', position_x: 100, position_y: 200 },
        { name: 'City B', position_x: 300, position_y: 400 },
    ],
};

export const mockRoute = {
    route: {
        '0': 'City A',
        '1': 'City B',
    },
    distance: 5000,
};

export const mockMapData = {
    cities: [
        {
            id: 1,
            name: 'Markarth',
            position_x: 380,
            position_y: 1196,
        },
        {
            id: 2,
            name: 'Karthwasten',
            position_x: 628,
            position_y: 992,
        },
    ],
    connections: [
        {
            child_city_id: 1,
            parent_city_id: 2,
        },
        {
            child_city_id: 2,
            parent_city_id: 1,
        },
    ],
    map: {
        id: 1,
        name: 'Skyrim',
        size_x: 3066,
        size_y: 2326,
    },
};

export const mockMapList = {
    maps: [
        {
            id: 1,
            name: 'skyrim',
        },
        {
            id: 2,
            name: '10',
        },
    ],
};

export const mockRouteData = {
    id: 1,
    startpoint: 'Karthwasten',
    endpoint: 'Rorikstead',
    route: {
        alternative_distance: 877.25,
        alternative_route: {
            '0': 'Karthwasten',
            '1': 'Markarth',
            '2': 'Rorikstead',
        },
        distance: 362.94,
        route: {
            '0': 'Karthwasten',
            '1': 'Rorikstead',
        },
    },
};

export const mockRoutesData = {
    routes: [
        {
            id: 1,
            startpoint: 'Karthwasten',
            endpoint: 'Rorikstead',
            route: {
                alternative_distance: 877.25,
                alternative_route: {
                    '0': 'Karthwasten',
                    '1': 'Markarth',
                    '2': 'Rorikstead',
                },
                distance: 362.94,
                route: {
                    '0': 'Karthwasten',
                    '1': 'Rorikstead',
                },
            },
        },
        {
            id: 2,
            startpoint: 'Whiterun',
            endpoint: 'Windhelm',
            route: {
                alternative_distance: 877.25,
                alternative_route: {
                    '0': 'Whiterun',
                    '1': 'Windhelm',
                },
                distance: 362.94,
                route: {
                    '0': 'Whiterun',
                    '1': 'Windhelm',
                },
            },
        },
    ],
};

// Helper function to change the page by clicking a link
export const changePage = async (container: HTMLElement, href: string) => {
    const routePageButton = await waitFor(() => {
        const element = container.querySelector(`a[href="${href}"]`);
        if (!element) throw new Error('Element not found');
        return element;
    });
    act(() => {
        fireEvent.click(routePageButton);
    });
    console.log('Page changed to:', href);
};

// Error throwing component
export const ErrorComponent = () => {
    throw new Error('Test Error');
};

// Function to create a mock QueryClient
export const createMockQueryClient = () => {
    return new QueryClient({
        defaultOptions: {
            queries: {
                retry: false, // Disable retries for deterministic tests
                // cacheTime: 0, // Reset cache immediately after tests
                staleTime: 0, // Always mark queries as "stale" to force fetching
            },
        },
    });
};

// Helper function to clean up the QueryClient after each test
export const cleanupQueryClient = (queryClient: QueryClient) => {
    queryClient.clear();
};
