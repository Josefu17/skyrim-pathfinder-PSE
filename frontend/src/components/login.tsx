import { FormEvent, useState } from 'react';

import { TUser } from '../types';
import { useAuth } from '../contexts/authContext';
import { MESSAGETIMER } from '../support/support';
import '../styles/login.css';

export const Login = () => {
    const [username, setUsername] = useState<string>('');
    const [statusMessage, setStatusMessage] = useState<string>(''); // State to display feedback messages
    const { setUser } = useAuth();

    const handleLogin = async (e: FormEvent) => {
        e.preventDefault(); // Prevent the default form behavior (page reload)

        try {
            const response = await fetch(
                `${import.meta.env.VITE_URL}/auth/login`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username }), // Serialize username as JSON
                }
            );

            console.log(response);
            if (response.ok) {
                const data = await response.json();
                console.log(data);
                const user: TUser = { username: username, id: data.user.id };
                setStatusMessage(`Logged in as ${user.username}`); // Show success message
                setUser(user);
                setUsername(''); // Clear the input field
            } else {
                const errorData = await response.json();
                setStatusMessage(`${errorData.error}`);
            }
        } catch (error: unknown) {
            setStatusMessage(
                'An error occurred. Please try again later. ' + error
            ); // Show generic error message
        }
        setTimeout(() => {
            setStatusMessage(''); // Clear the message after 3 seconds
        }, MESSAGETIMER);
    };

    return (
        <section id="login">
            <h2>Login</h2>
            <form id="login-form" onSubmit={handleLogin}>
                <label htmlFor="login-username">Username</label>
                <input
                    id="login-username"
                    name="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <input
                    id="submit-login-username"
                    type="submit"
                    value={'Login'}
                />
            </form>
            {/* Conditionally render feedback message */}
            {statusMessage && <p>{statusMessage}</p>}
            {null}
        </section>
    );
};
