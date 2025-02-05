import { useEffect, useState, useRef, useCallback } from 'react';
import { useMap } from '../contexts/mapContext';
import { TMap } from '../types';

export const MapSelector = () => {
    const { currentMap, setCurrentMap } = useMap();
    const [value, setValue] = useState<number>(currentMap?.id ?? 0);
    const [mapList, setMapList] = useState<TMap[]>([]);
    const abortControllerRef = useRef<AbortController | null>(null);
    const timeoutRef = useRef<NodeJS.Timeout | null>(null);

    useEffect(() => {
        const fetchMapList = async () => {
            // Cancel previous request if still running
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }

            const controller = new AbortController();
            abortControllerRef.current = controller;

            try {
                console.log('Fetching map list...');
                const response = await fetch(
                    `${import.meta.env.VITE_URL}/maps`,
                    {
                        signal: controller.signal,
                    }
                );

                if (!response.ok) {
                    throw new Error(
                        'Failed to fetch data: ' + response.statusText
                    );
                }

                const data = await response.json();
                console.log(data);
                setMapList(data.maps);
            } catch (error) {
                if ((error as Error)?.name !== 'AbortError') {
                    console.error('Error fetching map list:', error);
                }
            }
        };

        fetchMapList();

        return () => {
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, []);

    useEffect(() => {
        if (currentMap) {
            setValue(currentMap.id);
        }
    }, [currentMap]);

    useEffect(() => {
        console.log('Current Map has changed:', currentMap);
    }, [currentMap]);

    const handleChange = useCallback(
        (e: React.ChangeEvent<HTMLSelectElement>) => {
            const selectedId = Number(e.target.value);

            // Clear previous debounce timeout
            if (timeoutRef.current) {
                clearTimeout(timeoutRef.current);
            }

            // Debounce state update to prevent UI lag
            timeoutRef.current = setTimeout(() => {
                setValue(selectedId);
                const selectedMap = mapList.find(
                    (map) => map.id === selectedId
                );
                if (selectedMap && selectedId !== currentMap?.id) {
                    setCurrentMap(selectedMap);
                }
            }, 200); // 200ms debounce
        },
        [mapList, currentMap, setCurrentMap]
    );

    return (
        <section id="map-selector">
            <label htmlFor="select-map">Choose a map to view: </label>
            <select
                id="select-map"
                name="select-map"
                value={value}
                onChange={handleChange}
            >
                {mapList.map((map) => (
                    <option key={map.id} value={map.id}>
                        {map.name}
                    </option>
                ))}
            </select>
            <h2>Selected Map: {currentMap?.name}</h2>
        </section>
    );
};
