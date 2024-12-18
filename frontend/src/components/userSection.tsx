import { useState } from 'react';

import { useAuth } from '../contexts/authContext';
import { Register } from './register';
import { Login } from './login';
import { Logout } from './logout';
import { REGISTER, LOGIN } from '../support';
import '../styles/userSection.css';

const RegisterSwitcher = ({
    activeForm,
    setActiveForm,
}: {
    activeForm: string;
    setActiveForm: React.Dispatch<React.SetStateAction<string>>;
}) => (
    <input
        type="button"
        value="Register now"
        onClick={() => setActiveForm(activeForm === REGISTER ? '' : REGISTER)}
    />
);

const LoginSwitcher = ({
    activeForm,
    setActiveForm,
}: {
    activeForm: string;
    setActiveForm: React.Dispatch<React.SetStateAction<string>>;
}) => (
    <input
        type="button"
        value="Login now"
        onClick={() => setActiveForm(activeForm === LOGIN ? '' : LOGIN)}
    />
);

const LogoutSwitcher = () => {
    const { user } = useAuth(); // Take the user from the context
    return user ? (
        <article>
            <Logout />
        </article>
    ) : null;
};

export const UserSection = () => {
    const [activeForm, setActiveForm] = useState<string>(''); // Track the active form (empty, 'register', 'login')
    const { user } = useAuth(); // Take the user from the context

    const renderForm = () => {
        if (activeForm === REGISTER)
            return (
                <article id="userSection-activeForm">
                    <Register />
                </article>
            );
        if (activeForm === LOGIN)
            return (
                <article id="userSection-activeForm">
                    <Login />
                </article>
            );
        return null; // Nothing is shown if no form is active
    };

    return (
        <section id="user-section">
            <h2>User Section</h2>
            {user ? (
                <p>Logged in as {user.username}</p>
            ) : (
                <p>Welcome, Guest!</p>
            )}
            <RegisterSwitcher
                activeForm={activeForm}
                setActiveForm={setActiveForm}
            />
            <LoginSwitcher
                activeForm={activeForm}
                setActiveForm={setActiveForm}
            />
            <LogoutSwitcher />
            {renderForm()}
        </section>
    );
};
