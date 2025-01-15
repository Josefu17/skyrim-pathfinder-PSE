import { Routes, Route, Navigate } from 'react-router-dom';

import { useAuth } from '../contexts/authContext';
import { Docs } from '../pages/docs';
import { Home } from '../pages/home';
import { RoutesHistory } from '../pages/routesHistory';

export const AppRoutes = () => {
    const { user, loading } = useAuth();

    if (loading) {
        return <p>Loading...</p>;
    }

    return (
        <Routes>
            <Route
                path="/routes-history"
                element={user ? <RoutesHistory /> : <Navigate to="/" />}
            />
            <Route path="/docs" element={<Docs />} />
            <Route path="/" element={<Home />} />
        </Routes>
    );
};
