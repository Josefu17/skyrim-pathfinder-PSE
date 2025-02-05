import { TCity } from '../types';
import '../styles/cityEntry.css';

export const CityEntry = ({
    city,
    onClick,
    isActive,
}: {
    city: TCity;
    onClick: () => void;
    isActive: 'start' | 'end' | '';
    }) => {
let coordinates = `(${city.position_x}, ${city.position_y})`;
    if (!city.position_x || !city.position_y) {
        coordinates = '';
    }
    
    return (
        <input
            type="button"
            className={`static-city${isActive ? ' ' + isActive : ''}`}
            onClick={onClick}
            value={`${city.name}\n${coordinates}`}
        />
    );
};
