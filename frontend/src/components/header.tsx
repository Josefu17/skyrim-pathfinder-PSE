import { Link } from 'react-router-dom';

import { useAuth } from '../contexts/authContext';
import mapImage from '../assets/map.svg';
import { UserSection } from './userSection';
import '../styles/header.css';
import { MapSelector } from './mapSelector';

export const Header = () => {
    const { user } = useAuth();
    return (
        <header role="banner">
            <h1>Path finder</h1>
            <img id="header-logo" src={mapImage} alt="" />
            <MapSelector />
            <ul>
                <li>
                    <Link to="/">Path Finder</Link>
                </li>
                <li>
                    <Link to="/docs">Documentation</Link>
                </li>
                {user ? (
                    <li>
                        <Link to="/routes-history">Routes History</Link>
                    </li>
                ) : null}
            </ul>
            <UserSection />
        </header>
    );
};
