import { Header } from './components/header';
import { Footer } from './components/footer';
import { BrowserRouter } from 'react-router-dom';
import { AppRoutes } from './routes/app_routes';

import './style/App.css';

function App() {
    return (
        <BrowserRouter>
            <section id="left">
                <Header />
            </section>
            <section id="right">
                <AppRoutes />
                <Footer />
            </section>
        </BrowserRouter>
    );
}

export default App;
