import { useState } from 'react';
import { Register } from './register';

const RegisterSwitcher = () => {
    const [isRegisterShown, setIsRegisterShown] = useState<boolean>(false);
    return (
        <>
            <input
                type="button"
                value="Register now"
                className="boton-elegante"
                onClick={() => {
                    setIsRegisterShown(!isRegisterShown);
                }}
            ></input>
            {isRegisterShown ? (
                <article>
                    <Register />
                </article>
            ) : null}
        </>
    );
};

export const UserSection = () => {
    return (
        <section id="user-section">
            <h2>User Section</h2>
            <RegisterSwitcher />
        </section>
    );
};
