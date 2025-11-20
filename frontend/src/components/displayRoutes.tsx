import { useEffect, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import {
    TCities,
    TCity,
    TFilterOptions,
    TStrRouteData,
    TStrRoutes,
} from '../types';
import { useAuth } from '../contexts/authContext';
import { RouteEntry } from './routeEntry';

import '../styles/routesHistory.css';
import { useMap } from '../contexts/mapContext';
import { apiFetch } from '../api.ts';

export const DisplayRoutes = ({
    defaultOptionalParametersVisible = false,
    defaultFilterOptions,
}: {
    defaultOptionalParametersVisible?: boolean;
    defaultFilterOptions?: TFilterOptions;
}) => {
    const { user, loading } = useAuth();
    const { currentMap } = useMap();
    const queryClient = useQueryClient();
    const [startpoint, setStartpoint] = useState<string>('');
    const [endpoint, setEndpoint] = useState<string>('');
    const [options, setOptions] = useState<TFilterOptions>({
        limit: 10,
        descending: true,
        from_date: '',
        map_id: currentMap?.id ?? 1,
        to_date: '',
        startpoint: '',
        endpoint: '',
        ...defaultFilterOptions,
    });
    const [isOptionalParametersVisible, setIsOptionalParametersVisible] =
        useState<boolean>(defaultOptionalParametersVisible);
    const [isDeleting, setIsDeleting] = useState<boolean>(false);

    const { data: cities } = useQuery<TCities>({
        queryKey: [
            'cities',
            { startpoint: options.startpoint, endpoint: options.endpoint },
        ],
        queryFn: async () => {
            const response = await apiFetch(`/cities?map_id=${currentMap?.id}`);

            const data = await response.json();
            return data.cities;
        },
        enabled: isOptionalParametersVisible,
    });

    const { data: routes, isLoading: routesLoading } = useQuery<TStrRoutes>({
        queryKey: ['routes', user?.id, { options }],
        queryFn: async () => {
            try {
                let parameters = '?';
                for (const [key, value] of Object.entries(options)) {
                    parameters += `${key}=${value}&`;
                }

                const response = await apiFetch(
                    `/users/${user?.id}/routes${parameters}`
                );

                const data = await response.json();
                if (!response.ok) {
                    console.error('Error fetching routes');
                    throw new Error(`(user ${user?.username}): ` + data.error);
                }
                return data.routes;
            } catch (error) {
                console.error('Error fetching routes' + error);
                return null;
            }
        },
        enabled: !!user, // Start query only when user is defined
    });

    useEffect(() => {
        console.log('Changing map to ', currentMap);
        setOptions((prevOptions) => ({
            ...prevOptions,
            map_id: currentMap?.id ?? 1,
        }));
    }, [currentMap]);

    const handleChange = (
        e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
    ) => {
        const { name, value, type, checked } = e.target as HTMLInputElement;

        setOptions((prevOptions) => ({
            ...prevOptions,
            [name]: type === 'checkbox' ? checked : value,
        }));
    };

    const handleDeleteSelectedRoute = async (key: number) => {
        const route = routes?.find((route) => route.id === key);
        console.log('Deleting route:', route);
        try {
            const response = await apiFetch(
                `/users/${user?.id}/routes/${key}`,
                { method: 'DELETE' }
            );

            const data = await response.json();
            if (response.ok) {
                console.log(data);
            } else {
                console.error('Error deleting route');
                throw new Error(`(user ${user?.username}): ` + data.error);
            }
        } catch (error) {
            console.error(`Error deleting route: ` + error);
        }
    };

    const { mutateAsync: deleteSelectedRoute } = useMutation({
        mutationFn: handleDeleteSelectedRoute,
        onSuccess: () => {
            void queryClient.invalidateQueries({ queryKey: ['routes'] });
        },
    });

    const { mutateAsync: deleteAllRoutes } = useMutation({
        mutationFn: async () => {
            console.log('Deleting all routes');
            try {
                const response = await apiFetch(`/users/${user?.id}/routes`, {
                    method: 'DELETE',
                });

                const data = await response.json();
                if (response.ok) {
                    console.log(data);
                } else {
                    console.error('Error deleting all routes');
                    throw new Error(`(user ${user?.username}): ` + data.error);
                }
            } catch (error) {
                console.error(`Error deleting all routes: ` + error);
            }
        },
        onSuccess: () => {
            void queryClient.invalidateQueries({ queryKey: ['routes'] });
        },
    });

    const handleDeleteAll = async () => {
        try {
            await deleteAllRoutes();
        } catch (error) {
            console.error(`Error deleting all routes: `, error);
        }
    };

    if (loading) {
        console.log('loading...');
        return <p>Loading...</p>;
    }

    if (!user) {
        return <p>Please log in to view routes.</p>;
    }

    return (
        <>
            <h1>{`Routes History of ${user.username}`}</h1>
            <section id="manage-routes-section">
                <h2>Manage Routes</h2>
                <article id="sort-descending-option">
                    <label htmlFor="sort-descending"> descending </label>
                    <input
                        id="sort-descending"
                        name="descending"
                        type="checkbox"
                        checked={options.descending}
                        onChange={handleChange}
                    />
                </article>
                <article id="limit-option">
                    <label htmlFor="limit">limit</label>
                    <input
                        id="limit"
                        name="limit"
                        type="text"
                        placeholder="10"
                        value={options.limit}
                        maxLength={3}
                        onChange={handleChange}
                    />
                </article>
                {isOptionalParametersVisible && (
                    <>
                        <article id="from-date-option">
                            <label htmlFor="from-date">from:</label>
                            <input
                                id="from-date"
                                name="from_date"
                                type="datetime-local"
                                value={options.from_date}
                                onChange={handleChange}
                            />
                        </article>
                        <article id="to-date-option">
                            <label htmlFor="to-date">to:</label>
                            <input
                                id="to-date"
                                name="to_date"
                                type="datetime-local"
                                value={options.to_date}
                                onChange={handleChange}
                            />
                        </article>
                        <article id="startpoint-option">
                            <label htmlFor="startpoint">startpoint:</label>
                            <select
                                id="startpoint"
                                name="startpoint"
                                value={startpoint}
                                onChange={(e) => {
                                    setStartpoint(e.target.value);
                                    handleChange(e);
                                }}
                            >
                                <option value="">not selected</option>
                                {cities?.map(({ name }: TCity) => {
                                    if (name === endpoint) return null;
                                    return (
                                        <option key={name} value={name}>
                                            {name}
                                        </option>
                                    );
                                })}
                            </select>
                        </article>
                        <article id="endpoint-option">
                            <label htmlFor="endpoint">endpoint:</label>
                            <select
                                id="endpoint"
                                name="endpoint"
                                value={endpoint}
                                onChange={(e) => {
                                    setEndpoint(e.target.value);
                                    handleChange(e);
                                }}
                            >
                                <option value="">not selected</option>
                                {cities?.map(({ name }: TCity) => {
                                    if (name === startpoint) return null;
                                    return (
                                        <option key={name} value={name}>
                                            {name}
                                        </option>
                                    );
                                })}
                            </select>
                        </article>
                    </>
                )}
                <input
                    id="optionial-parameters-button"
                    type="button"
                    value={
                        isOptionalParametersVisible
                            ? 'Hide options'
                            : 'Show more options'
                    }
                    onClick={() =>
                        setIsOptionalParametersVisible(
                            !isOptionalParametersVisible
                        )
                    }
                />
                {isDeleting ? (
                    <>
                        <input
                            id="cancel-deletion"
                            type="button"
                            value="Quit deletion mode"
                            onClick={() => {
                                setIsDeleting(false);
                            }}
                        />
                        <input
                            id="delete-all-button"
                            type="button"
                            value="Delete all"
                            onClick={handleDeleteAll}
                        />
                    </>
                ) : (
                    <input
                        id="delete-button"
                        type="button"
                        value="Enter deletion mode"
                        onClick={() => {
                            setIsDeleting(!isDeleting);
                        }}
                    />
                )}
            </section>
            <section id="routes-section">
                <h2>Routes</h2>
                {routesLoading && <p>Loading routes...</p>}
                {!routesLoading && routes === null ? (
                    <p id="routes-list">No routes found.</p>
                ) : (
                    <ul id="routes-list">
                        {routes?.map((route: TStrRouteData) => (
                            <RouteEntry
                                key={route.id}
                                routeId={route.id}
                                routeData={route}
                                isDeleting={isDeleting}
                                onSelection={deleteSelectedRoute}
                            />
                        ))}
                    </ul>
                )}
            </section>
        </>
    );
};
