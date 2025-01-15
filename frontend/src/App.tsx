import { Header } from './components/header';
import { Footer } from './components/footer';
import { BrowserRouter } from 'react-router-dom';
import { AppRoutes } from './routes/appRoutes';
import { ErrorBoundary } from './support/errorBoundary';

import './styles/App.css';

export const App = () => {
    return (
        <BrowserRouter>
            <section id="left">
                <ErrorBoundary fallback={<h1>Something went wrong!</h1>}>
                    <Header />
                </ErrorBoundary>
            </section>
            <section id="right">
                <ErrorBoundary fallback={<h1>Something went wrong!</h1>}>
                    <AppRoutes />
                </ErrorBoundary>
                <ErrorBoundary fallback={<h1>Something went wrong!</h1>}>
                    <Footer />
                </ErrorBoundary>
            </section>
        </BrowserRouter>
    );
};
