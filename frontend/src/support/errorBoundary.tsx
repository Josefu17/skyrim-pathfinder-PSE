import React, { Component } from 'react';
import { useNavigate } from 'react-router-dom';
import { ErrorBoundaryProps, ErrorBoundaryState } from '../types';

export class ErrorBoundaryClass extends Component<
    ErrorBoundaryProps,
    ErrorBoundaryState
> {
    constructor(props: ErrorBoundaryProps) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(): ErrorBoundaryState {
        // Setzt den Fehlerzustand auf true, wenn ein Fehler auftritt
        return { hasError: true };
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        // Logging oder Fehlerverfolgung hier durchführen
        console.error('ErrorBoundary caught an error:', error, errorInfo);
    }

    handleGoHome = () => {
        // Navigiere zur Startseite (/)
        this.setState({ hasError: false });
        this.props.navigate('/');
    };

    render() {
        if (this.state.hasError) {
            // Wenn ein Fehler aufgetreten ist, zeige die Fallback-UI mit Reset- und Home-Button
            return (
                <>
                    {this.props.fallback}
                    <button onClick={this.handleGoHome}>Startpage</button>
                </>
            );
        }

        // Render die Kinder, wenn kein Fehler aufgetreten ist
        return this.props.children;
    }
}

// Higher-Order Component, um den React Router Navigator hinzuzufügen
export const ErrorBoundary = (props: Omit<ErrorBoundaryProps, 'navigate'>) => {
    const navigate = useNavigate();
    return <ErrorBoundaryClass {...props} navigate={navigate} />;
};
