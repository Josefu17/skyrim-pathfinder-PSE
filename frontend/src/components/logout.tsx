import { useAuth } from '../contexts/authContext';

export const Logout = () => {
    const { user, setUser } = useAuth();

    const handleLogout = () => {
        console.log(`No user logged in`);
        if (user == null) {
            return;
        } else {
            console.log(`Logging out user: ${user.username}`);
            setUser(null);
        }
    };

    return <input type="button" value="Logout" onClick={handleLogout}></input>;
};
