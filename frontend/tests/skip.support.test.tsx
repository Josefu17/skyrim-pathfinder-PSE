import { AuthProvider, useAuth } from '../src/contexts/authContext';
import { render } from '@testing-library/react';
import React, { useEffect } from 'react';
import { TUser } from '../src/types';

export const renderWithAuthProvider = (
    component: React.ReactNode,
    user: TUser | null = null
) => {
    return render(
        <AuthProvider>
            {user ? (
                <AuthProviderWithUser user={user}>
                    {component}
                </AuthProviderWithUser>
            ) : (
                component
            )}
        </AuthProvider>
    );
};

// AuthProviderWithUser sets the user context for the test
const AuthProviderWithUser = ({
    children,
    user,
}: {
    children: React.ReactNode;
    user: TUser;
}) => {
    const { setUser } = useAuth();

    useEffect(() => {
        setUser(user); // Set the user in the context
    }, []);

    return <>{children}</>;
};
