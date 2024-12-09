import { Routes, Route } from 'react-router-dom';

import { Docs } from '../pages/docs';
import { Home } from '../pages/home';

export const AppRoutes = () => {
    return (
        <Routes>
            <Route path="/docs" element={<Docs />} />
            <Route path="/" element={<Home />} />
        </Routes>
    );
};
