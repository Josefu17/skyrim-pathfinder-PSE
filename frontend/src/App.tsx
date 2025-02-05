import { Header } from './components/header';
import { Footer } from './components/footer';
import { BrowserRouter } from 'react-router-dom';
import { AppRoutes } from './routes/appRoutes';
import { ErrorBoundary } from './support/errorBoundary';

import './styles/App.css';

const fallback = <h1>Something went wrong!</h1>;

export const App = () => {
    return (
        <BrowserRouter>
            <section id="top">
                <section id="left">
                    <ErrorBoundary fallback={fallback}>
                        <Header />
                    </ErrorBoundary>
                </section>
                <section id="right">
                    <ErrorBoundary fallback={fallback}>
                        <AppRoutes />
                    </ErrorBoundary>
                </section>
            </section>
            <ErrorBoundary fallback={fallback}>
                <Footer />
            </ErrorBoundary>
        </BrowserRouter>
    );
};
