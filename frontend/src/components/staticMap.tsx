import { useCallback, useEffect, useRef, useState } from 'react';

import { useAuth } from '../contexts/authContext';
import { useMap } from '../contexts/mapContext';
import { CityEntry } from './cityEntry';
import { MESSAGETIMER, useScreenOrientation } from '../support/support';
import { JSONObject, TCities } from '../types';
import '../styles/staticMap.css';
import { DisplayJSON } from './displayJSON';
import { apiFetch } from '../api.ts';

export const StaticMap = () => {
    const { user } = useAuth();
    const { currentMap } = useMap();

    // State management
    const isPortrait = useScreenOrientation();
    const [startpoint, setStartpoint] = useState<string>('');
    const [endpoint, setEndpoint] = useState<string>('');
    const [routeData, setRouteData] = useState<object | null>(null);
    const [allCities, setAllCities] = useState<TCities>([]); // All cities, used for infinite scroll
    const [visibleCities, setVisibleCities] = useState<TCities>([]); // Only the cities to display
    const [suggestedCities, setSuggestedCities] = useState<TCities>([]); // Suggested cities, used for infinite scroll
    const [loadingMap, setLoadingMap] = useState<boolean>(true);
    const [loadingRoute, setLoadingRoute] = useState<boolean>(false);
    const [loadingMoreCities, setLoadingMoreCities] = useState<boolean>(false); // to track if we're fetching more cities
    const [loadingSuggestedCities, setLoadingSuggestedCities] =
        useState<boolean>(false); // to track if we're fetching more cities
    const [isActive, setIsActive] = useState<'start' | 'end' | ''>('');
    const [statusMessage, setStatusMessage] = useState<string>(''); // State to display feedback messages

    const sliceSize = 50;
    // Maximum number of visible cities
    const maxVisibleCities = isPortrait ? 20 : 200;
    const scrollThreshold = isPortrait ? 0.7 : 0.85; // Load more cities when reaching 85% of the list

    // Refs for user inputs to avoid unnecessary state updates
    const startpointRef = useRef<HTMLInputElement>(null);
    const endpointRef = useRef<HTMLInputElement>(null);

    // Ref for AbortController to cancel ongoing fetch requests when switching maps
    const abortControllerRef = useRef<AbortController | null>(null);

    // Fetch map data with request cancellation and debouncing
    const fetchMapData = useCallback(async () => {
        // Cancel the previous request if still running
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }

        const controller = new AbortController();
        abortControllerRef.current = controller;

        setLoadingMap(true);

        try {
            if (!currentMap?.name) return;

            const response = await apiFetch(
                `/maps?name=${encodeURIComponent(currentMap.name)}`,
                { signal: controller.signal }
            );

            if (!response.ok) throw new Error('Failed to fetch map data');

            const data = await response.json();

            // Only update state if the request was not aborted
            if (!controller.signal.aborted) {
                setAllCities(data.cities); // Store all cities for the current map
                setVisibleCities(data.cities.slice(0, sliceSize)); // Initially show the first `sliceSize` cities
                setLoadingMap(false);
                setSuggestedCities([]); // Reset suggested cities when switching maps
            }
        } catch (error) {
            if ((error as Error)?.name !== 'AbortError') {
                console.error('Error fetching map data:', error);
            }
        }
    }, [currentMap]);

    useEffect(() => {
        fetchMapData();

        return () => {
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, [fetchMapData]);

    const loadMoreCities = (direction: 'down' | 'up' | 'right' | 'left') => {
        if (loadingMoreCities) return;

        setLoadingMoreCities(true);

        setVisibleCities((prevCities) => {
            let newCities: TCities = [];
            let updatedCities: TCities = [];

            if (direction === 'down' || direction === 'right') {
                const lastVisibleCity = prevCities[prevCities.length - 1];
                const startIndex = allCities.indexOf(lastVisibleCity) + 1;

                if (startIndex < allCities.length) {
                    newCities = allCities.slice(
                        startIndex,
                        startIndex + sliceSize
                    );
                }

                updatedCities = [...prevCities, ...newCities];

                if (updatedCities.length > maxVisibleCities) {
                    updatedCities = updatedCities.slice(
                        updatedCities.length - maxVisibleCities
                    );
                }
            } else if (direction === 'up' || direction === 'left') {
                const firstVisibleCity = prevCities[0];
                const startIndex = allCities.indexOf(firstVisibleCity);

                if (startIndex > 0) {
                    const newStartIndex = Math.max(startIndex - sliceSize, 0);
                    newCities = allCities.slice(newStartIndex, startIndex);
                    updatedCities = [...newCities, ...prevCities];
                } else {
                    updatedCities = [...prevCities]; // If already at the top, don't change anything
                }

                if (updatedCities.length > maxVisibleCities) {
                    updatedCities = updatedCities.slice(0, maxVisibleCities);
                }
            }

            return updatedCities;
        });

        setLoadingMoreCities(false);
    };

    // Fetch suggested cities based on the start and endpoint
    const fetchSuggestedCities = useCallback(async () => {
        if (!startpoint && !endpoint) return;

        setLoadingSuggestedCities(true);
        try {
            if (!currentMap?.id) return;

            const queryFor =
                isActive === 'start'
                    ? startpoint
                    : isActive === 'end'
                      ? endpoint
                      : startpoint || endpoint;

            if (!queryFor) return;

            console.log('Fetching suggested cities for:', queryFor);

            const response = await apiFetch(
                `/suggestions/maps/${currentMap.id}?query=${encodeURIComponent(queryFor)}`
            );

            if (!response.ok)
                throw new Error('Failed to fetch suggested cities');

            const data = await response.json();
            console.log('suggest', data.suggestions);
            setSuggestedCities(data.suggestions);
        } catch (error) {
            console.error('Error fetching suggested cities:', error);
        } finally {
            setLoadingSuggestedCities(false);
        }
    }, [startpoint, endpoint, isActive]);

    // Call fetchSuggestedCities when either startpoint or endpoint changes
    useEffect(() => {
        console.log('Fetching suggested cities...');
        fetchSuggestedCities();
    }, [startpoint, endpoint, fetchSuggestedCities]);

    // Fetch route data with request debouncing
    const fetchRouteData = useCallback(async () => {
        if (!startpoint || !endpoint) return;

        setLoadingRoute(true);
        console.log('Fetching route data for:', startpoint, ', ', endpoint);
        try {
            if (!currentMap?.id) return;

            const url = user
                ? `/users/${user.id}/maps/${currentMap.id}/routes`
                : `/maps/${currentMap.id}/routes`;

            const response = await apiFetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ startpoint, endpoint }),
            });

            console.log('body:', JSON.stringify({ startpoint, endpoint }));

            const data = await response.json();
            if (response.ok) {
                console.log('route data', data);
            } else {
                console.log('error', data.error);
                console.log('response', response);
                setStatusMessage('Unable to calculate route');
                throw new Error(data.error);
            }

            setRouteData(data);
            setStartpoint('');
            setEndpoint('');
            if (startpointRef.current) startpointRef.current.value = '';
            if (endpointRef.current) endpointRef.current.value = '';
            setIsActive('start');
        } catch (error) {
            setStatusMessage('Error fetching route');
            console.error('Error fetching route data:', error);
        } finally {
            setLoadingRoute(false);
            setTimeout(() => {
                setStatusMessage('');
            }, MESSAGETIMER);
        }
    }, [startpoint, endpoint, currentMap, user]);

    // Track scroll position and load more cities when reaching 85% of the list
    const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
        if (isPortrait) {
            const scrollLeft = e.currentTarget.scrollLeft;
            const scrollWidth = e.currentTarget.scrollWidth;
            const clientWidth = e.currentTarget.clientWidth;

            // Trigger loading when the user reaches the scroll threshold of the scrollable content
            if (scrollLeft + clientWidth >= scrollWidth * scrollThreshold) {
                console.log('Load right');
                loadMoreCities('right'); // Load more cities when scrolling to the right
            } else if (scrollLeft <= scrollWidth * (1 - scrollThreshold)) {
                console.log('Load left');
                loadMoreCities('left'); // Load more cities when scrolling to the left
            }
        } else {
            const scrollTop = e.currentTarget.scrollTop;
            const scrollHeight = e.currentTarget.scrollHeight;
            const clientHeight = e.currentTarget.clientHeight;

            // Trigger loading when the user reaches the scroll threshold of the scrollable content
            if (scrollTop + clientHeight >= scrollHeight * scrollThreshold) {
                console.log('Load down');
                loadMoreCities('down'); // Load more cities when scrolling down
            } else if (
                scrollTop <=
                scrollHeight * (1 - scrollThreshold) * 1.25
            ) {
                console.log('Load up');
                loadMoreCities('up'); // Load more cities when scrolling up
            }
        }
    };

    const handleCityClick = (cityName: string) => {
        if (isActive === 'start' || (isActive === '' && !startpoint)) {
            console.log('Setting startpoint:', cityName);
            setStartpoint(cityName);
            setIsActive('end'); // Make endpoint active after setting startpoint
        } else if (isActive === 'end' || (isActive === '' && !endpoint)) {
            console.log('Setting endpoint:', cityName);
            setEndpoint(cityName);
            setIsActive('start'); // Make start active after setting endpoint
        }
    };

    useEffect(() => {
        // Reset related states when logging in or out
        setRouteData(null);
        setStartpoint('');
        setEndpoint('');
        if (startpointRef.current) startpointRef.current.value = '';
        if (endpointRef.current) endpointRef.current.value = '';
        setIsActive('');
        setSuggestedCities([]);
    }, [user]);

    const handleChangeSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
        // TODO: Implement clearing each others field, when same city
        if (isActive === 'start' || (isActive === '' && !startpoint)) {
            if (e.target.value === endpoint) {
                setEndpoint('');
            }
            setStartpoint(e.target.value);
        } else if (isActive === 'end' || (isActive === '' && !endpoint)) {
            if (e.target.value === startpoint) {
                setStartpoint('');
            }
            setEndpoint(e.target.value);
        }
    };

    return (
        <section id="static-map">
            <section
                id="static-cityListArticle"
                onScroll={handleScroll} // Add scroll listener
            >
                <h2 className="listTitle">Cities</h2>
                {loadingMap ? (
                    <p>Loading map data...</p>
                ) : (
                    <>
                        {visibleCities?.map((city) => (
                            <CityEntry
                                key={city.id}
                                city={city}
                                onClick={() => handleCityClick(city.name)}
                                isActive={isActive}
                            />
                        ))}
                        {loadingMoreCities && <p>Loading more cities...</p>}
                    </>
                )}
            </section>
            <section
                id="static-citySuggestionsArticle"
                onScroll={handleScroll} // Add scroll listener
            >
                {!suggestedCities ? (
                    <h2 className="listTitle">Sug-gestions</h2>
                ) : null}
                {loadingMap ? (
                    <p>Loading map data...</p>
                ) : (
                    <>
                        {suggestedCities?.map((city) => (
                            <CityEntry
                                key={city.id}
                                city={city}
                                onClick={() => handleCityClick(city.name)}
                                isActive={isActive}
                            />
                        ))}
                        {loadingSuggestedCities && (
                            <p>Loading more cities...</p>
                        )}
                    </>
                )}
            </section>
            <section id="static-routeSection">
                <article id="static-selectArticle">
                    <h2>Select your startpoint and endpoint</h2>
                    <article id="static-selectPoints">
                        <input
                            id="static-startpoint"
                            name="startpoint"
                            type="text"
                            ref={startpointRef}
                            onFocus={() => {
                                setIsActive('start');
                            }}
                            onChange={(e) => {
                                handleChangeSearch(e);
                            }}
                            value={startpoint}
                            placeholder="Startpoint"
                        />
                        <input
                            id="static-endpoint"
                            name="endpoint"
                            type="text"
                            ref={endpointRef}
                            onFocus={() => setIsActive('end')}
                            onChange={(e) => {
                                if (e.target.value === startpoint) {
                                    setStartpoint('');
                                }
                                setEndpoint(e.target.value);
                            }}
                            value={endpoint}
                            placeholder="Endpoint"
                        />
                        <button
                            id="static-calculateButton"
                            onClick={fetchRouteData}
                        >
                            Calculate Route
                        </button>
                    </article>
                </article>

                <article id="static-routeArticle">
                    <h2>Route</h2>
                    {loadingRoute ? (
                        <p>
                            {user
                                ? 'Calculating route... Please have patience, or view the result in "Routes History" section once ready.'
                                : 'Loading route...'}
                        </p>
                    ) : (
                        <>
                            {routeData ? (
                                <pre id="static-calculated-route">
                                    <DisplayJSON
                                        json={routeData as JSONObject}
                                    />
                                </pre>
                            ) : (
                                <p>
                                    {statusMessage !== ''
                                        ? statusMessage
                                        : 'No route requested.'}
                                </p>
                            )}
                        </>
                    )}
                </article>
            </section>
        </section>
    );
};
