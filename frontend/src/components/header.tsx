import { Link } from 'react-router-dom';

import '../style/header.css';
import mapImage from '../assets/map.svg';

export const Header = () => {
    return (
        <header>
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
        </header>
    );
};
