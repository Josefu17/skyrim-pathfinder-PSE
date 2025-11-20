import { FormEvent, useState } from 'react';

import { TUser } from '../types';
import { useAuth } from '../contexts/authContext';
import { MESSAGETIMER } from '../support/support';
import '../styles/register.css';
import { apiFetch } from '../api.ts';

export const Register = () => {
    const [username, setUsername] = useState<string>(''); // State to store the username input
    const [statusMessage, setStatusMessage] = useState<string>(''); // State to display feedback messages
    const { setUser } = useAuth(); // Get the setUser function from the AuthContext

    // Function to handle form submission
    const handleRegister = async (e: FormEvent) => {
        e.preventDefault(); // Prevent the default form behavior (page reload)

        try {
            // Send a POST request with the username as JSON
            const response = await apiFetch('/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username }),
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
                setStatusMessage('Registration successful!'); // Show success message
                const user: TUser = data.user;
                setUser(user); // Set the user in the context
                setUsername(''); // Clear the input field
            } else {
                const errorData = await response.json();
                setStatusMessage(`${errorData.error}`); // Show server error message
            }
        } catch (error: unknown) {
            setStatusMessage(
                'An error occurred. Please try again later. ' + error
            ); // Show generic error message
        }
        console.log('Waiting to clear message ...');
        setTimeout(() => {
            setStatusMessage(''); // Clear the message after predefined timeout
            console.log('Message cleared!');
        }, MESSAGETIMER);
    };

    return (
        <section id="register">
            <h2>Register</h2>
            <form id="register-form" onSubmit={handleRegister}>
                <label htmlFor="register-username">Username</label>
                <input
                    id="register-username"
                    name="username"
                    type="text"
                    value={username} // Bind input value to state
                    onChange={(e) => setUsername(e.target.value)} // Update state on input change
                    required
                />
                <input
                    id="submit-register-username"
                    type="submit"
                    value="Register"
                />
            </form>
            {/* Conditionally render feedback message */}
            {statusMessage && <p>{statusMessage}</p>}
            {null}
        </section>
    );
};
