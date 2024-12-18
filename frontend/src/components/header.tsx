import { Link } from 'react-router-dom';

import mapImage from '../assets/map.svg';
import { UserSection } from './userSection';
import '../styles/header.css';

export const Header = () => {
    return (
        <header role="banner">
            <h1>Path finder</h1>
            <img id="header-logo" src={mapImage} alt="" />
            <ul>
                <li>
                    <Link to="/">Startseite</Link>
                </li>
                <li>
                    <Link to="/docs">Documentation</Link>
                </li>
            </ul>
            <UserSection />
        </header>
    );
};
