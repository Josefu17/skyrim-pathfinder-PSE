import { useState } from 'react';
import { JSONObject, TStrRouteData } from '../types';
import { DisplayJSON } from './displayJSON';

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
                    <DisplayJSON json={routeData.route as JSONObject} />
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
            {isExpanded && <DisplayJSON json={routeData.route as JSONObject} />}
        </li>
    );
};
