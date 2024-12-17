import { FormEvent, useState } from 'react';

import '../styles/register.css';

export const Register = () => {
    const [username, setUsername] = useState<string>(''); // State to store the username input
    const [statusMessage, setStatusMessage] = useState<string>(''); // State to display feedback messages

    // Function to handle form submission
    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault(); // Prevent the default form behavior (page reload)

        try {
            // Send a POST request with the username as JSON
            const response = await fetch(
                `${import.meta.env.VITE_URL}/auth/register`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username }), // Serialize username as JSON
                }
            );

            if (response.ok) {
                setStatusMessage('Registration successful!'); // Show success message
                setUsername(''); // Clear the input field
            } else {
                const errorData = await response.json();
                setStatusMessage(`Error: ${errorData.message}`); // Show server error message
            }
        } catch (error: unknown) {
            setStatusMessage(
                'An error occurred. Please try again later. ' + error
            ); // Show generic error message
        }
    };

    return (
        <section id="register">
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <label htmlFor="username">Username</label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    value={username} // Bind input value to state
                    onChange={(e) => setUsername(e.target.value)} // Update state on input change
                    required
                />
                <input
                    id="submit-username"
                    type="submit"
                    value="Register"
                    className="boton-elegante"
                />
            </form>
            {statusMessage && <p>{statusMessage}</p>}
            {null}
            {/* Conditionally render feedback message */}
        </section>
    );
};
