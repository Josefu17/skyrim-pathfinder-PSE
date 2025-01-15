import { useState } from 'react';
import { TStrRouteData } from '../types';

export const RouteEntry = ({
    routeId,
    routeData,
    isDeleting: isSelecting,
    onSelection,
}: {
    routeId: number;
    routeData: TStrRouteData;
    isDeleting: boolean;
    onSelection: (routeId: number) => void;
}) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const toggleExpand = () => {
        setIsExpanded((prev) => !prev);
    };

    const handleSelection = () => {
        onSelection(routeId);
    };

    if (isSelecting) {
        return (
            <li key={routeId}>
                <input
                    id={routeData.id.toString()}
                    type="button"
                    className="selectable"
                    onClick={handleSelection}
                    value={`${routeData.startpoint} to ${routeData.endpoint}`}
                />
                {isExpanded && (
                    <pre>{JSON.stringify(routeData.route, null, 2)}</pre>
                )}
            </li>
        );
    }

    return (
        <li key={routeId}>
            <input
                id={routeData.id.toString()}
                type="button"
                onClick={toggleExpand}
                value={`${routeData.startpoint} to ${routeData.endpoint}`}
            />
            {isExpanded && (
                <pre>{JSON.stringify(routeData.route, null, 2)}</pre>
            )}
        </li>
    );
};
