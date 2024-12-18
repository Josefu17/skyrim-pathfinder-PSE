import { useState, useEffect } from 'react';
import {
    TCities,
    TConnections,
    TRouteData,
    TConnection,
    TCity,
} from '../types';

export const InteractiveMap = () => {
    const [cities, setCities] = useState<TCities | null>(null);
    const [connections, setConnections] = useState<TConnections | null>(null);
    const [startpoint, setStartpoint] = useState('');
    const [endpoint, setEndpoint] = useState('');
    const [routeData, setRouteData] = useState<TRouteData | null>(null);
    const [alternative, setAlternative] = useState(false);
    const routeDistance = alternative
        ? routeData?.alternative_distance
        : routeData?.distance;

    const getCityCoordinates = (id: number | undefined): TCity | null => {
        const city = cities?.find((city) => city.id === id);
        return city
            ? {
                  id: city.id,
                  name: city.name,
                  position_x: city.position_x,
                  position_y: city.position_y,
              }
            : null;
    };

    const getCityNameById = (id: number | undefined): string => {
        const city = cities?.find((city) => city.id === id);
        return city ? city.name : '';
    };

    useEffect(() => {
        const fetchMapData = async () => {
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_URL}/maps`
                );
                const data = await response.json();
                setCities(data.cities);
                setConnections(data.connections);
            } catch (error) {
                console.error('Error fetching map data:', error);
            }
        };
        fetchMapData();
    }, []);

    useEffect(() => {
        const fetchRouteData = async () => {
            if (startpoint && endpoint) {
                try {
                    const response = await fetch(
                        `${import.meta.env.VITE_URL}/routes`,
                        {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                startpoint,
                                endpoint,
                            }),
                        }
                    );
                    const data = await response.json();
                    setRouteData(data);
                    setStartpoint('');
                    setEndpoint('');
                    console.log('Route data:', data);
                } catch (error) {
                    console.error('Error fetching route data:', error);
                }
            }
        };
        fetchRouteData();
    }, [startpoint, endpoint]);

    return (
        <>
            <svg
                id="map"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 3066 2326"
            >
                {/* draw connections */}
                {connections?.map((connection: TConnection) => {
                    const fromCity = getCityCoordinates(
                        connection.parent_city_id
                    );
                    const toCity = getCityCoordinates(connection.child_city_id);

                    if (!fromCity || !toCity) return null;

                    return (
                        <line
                            key={`${connection.parent_city_id}-${connection.child_city_id}`}
                            x1={fromCity.position_x}
                            y1={fromCity.position_y}
                            x2={toCity.position_x}
                            y2={toCity.position_y}
                            data-connection={`${getCityNameById(fromCity.id)}-${getCityNameById(toCity.id)}`}
                            stroke="black"
                            strokeWidth={10}
                        />
                    );
                })}

                {/* draw routes */}
                {routeData &&
                    Object.values(
                        alternative
                            ? routeData.alternative_route
                            : routeData.route
                    ).map((cityName, index, arr) => {
                        if (index === arr.length - 1) return null;
                        const fromCity = getCityCoordinates(
                            cities?.find((city) => city.name === cityName)?.id
                        );
                        const toCity = getCityCoordinates(
                            cities?.find((city) => city.name === arr[index + 1])
                                ?.id
                        );

                        if (!fromCity || !toCity) {
                            return null;
                        }

                        return (
                            <line
                                key={`route-${fromCity.id}-${toCity.id}`}
                                x1={fromCity.position_x}
                                y1={fromCity.position_y}
                                x2={toCity.position_x}
                                y2={toCity.position_y}
                                stroke="green"
                                strokeWidth={20}
                            />
                        );
                    })}

                {/* draw cities */}
                {cities?.map((city) => {
                    // Function to check if the city is part of the current route
                    const isCityOnRoute = () => {
                        const currentRoute = alternative
                            ? routeData?.alternative_route
                            : routeData?.route;
                        return Object.values(currentRoute || {}).includes(
                            city.name
                        );
                    };

                    const getCityColor = () => {
                        if (city.name === startpoint) return 'blue'; // Highlight startpoint
                        if (isCityOnRoute()) return 'green'; // Highlight cities on the route
                        return 'brown'; // Default color
                    };
                    return (
                        <g key={city.id}>
                            <text
                                fontSize={90}
                                x={city.position_x}
                                y={city.position_y + 80}
                                textAnchor="middle"
                            >
                                {city.name}
                            </text>
                            <circle
                                id={`endpoint-${city.id}`}
                                cx={city.position_x}
                                cy={city.position_y}
                                r="1.5rem"
                                fill={getCityColor()}
                                onClick={() => {
                                    if (!startpoint) {
                                        setStartpoint(city.name);
                                        console.log(
                                            `Set startpoint: ${city.name}`
                                        );
                                    } else if (!endpoint) {
                                        if (startpoint != city.name) {
                                            setEndpoint(city.name);
                                            console.log(
                                                `Set endpoint: ${city.name}`
                                            );
                                        }
                                    } else {
                                        setStartpoint('');
                                        setEndpoint('');
                                        console.log('reset data');
                                    }
                                }}
                            />
                        </g>
                    );
                })}
            </svg>
            {routeDistance && (
                <p id="distance">Distance to destination: {routeDistance} m</p>
            )}
            <input
                id="toggle-route"
                type="button"
                className="boton-elegante"
                value={
                    alternative ? 'Show Main Route' : 'Show Alternative Route'
                }
                onClick={() => {
                    setAlternative(!alternative);
                }}
            ></input>
        </>
    );
};
