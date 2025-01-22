import { screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom'; // For better matcher like `toBeInTheDocument`
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach, Mock } from 'vitest';
import { act } from 'react';

import { DisplayDocumentation } from '../../src/components/displayDocumentation';
import { renderWithAuthProvider } from '../skip.support.test';

describe('DisplayDocumentation', () => {
    beforeEach(() => {
        global.fetch = vi.fn();
    });

    it('loads and displays the initial file (README.md)', async () => {
        (global.fetch as Mock).mockResolvedValueOnce({
            ok: true,
            text: () => Promise.resolve('# Test Documentation'),
        });

        renderWithAuthProvider(DisplayDocumentation, null, {
            initialFile: 'README.md',
        });

        await waitFor(() => {
            expect(screen.getByText('Test Documentation')).toBeInTheDocument();
        });

        expect(global.fetch).toHaveBeenCalledWith('README.md');
    });

    it('navigates to a relative file and loads its content', async () => {
        (global.fetch as Mock).mockImplementation((url) => {
            if (url === 'test/README.md') {
                return Promise.resolve({
                    ok: true,
                    text: () =>
                        Promise.resolve('[Main Documentation](../other.md)'),
                });
            }
            if (url === 'other.md') {
                return Promise.resolve({
                    ok: true,
                    text: () => Promise.resolve('Other Documentation'),
                });
            }
            return Promise.reject(new Error('Not Found'));
        });

        renderWithAuthProvider(DisplayDocumentation, null, {
            initialFile: 'test/README.md',
        });

        await waitFor(() => {
            expect(screen.getByText('Main Documentation')).toBeInTheDocument();
        });

        const link = screen.getByText('Main Documentation');

        act(() => {
            userEvent.click(link);
        });

        await waitFor(() => {
            expect(screen.getByText('Other Documentation')).toBeInTheDocument();
        });

        expect(global.fetch).toHaveBeenCalledWith('other.md');
    });

    it('sets the initialFile and filePath to README.md if none is provided', async () => {
        (global.fetch as Mock).mockResolvedValueOnce({
            ok: true,
            text: () => Promise.resolve('# Home Documentation'),
        });

        renderWithAuthProvider(DisplayDocumentation, null, { initialFile: '' });

        await waitFor(() => {
            expect(screen.getByText('Home Documentation')).toBeInTheDocument();
        });

        expect(global.fetch).toHaveBeenCalledWith('README.md');
    });

    it('sets the filePath to initialFile if none is provided and initial filePath exists', async () => {
        (global.fetch as Mock).mockResolvedValueOnce({
            ok: true,
            text: () => Promise.resolve('[Test Documentation]()'),
        });

        renderWithAuthProvider(DisplayDocumentation, null, {
            initialFile: 'README.md',
        });

        await waitFor(() => {
            expect(screen.getByText('Test Documentation')).toBeInTheDocument();
        });

        expect(global.fetch).toHaveBeenCalledWith('README.md');
    });

    it('ignores the "./" in the href and stays in the current folder', async () => {
        (global.fetch as Mock).mockImplementation((url) => {
            if (url === 'README.md') {
                return Promise.resolve({
                    ok: true,
                    text: () =>
                        Promise.resolve('[Test Documentation](./test.md)'),
                });
            }
            if (url === 'test.md') {
                return Promise.resolve({
                    ok: true,
                    text: () => Promise.resolve('Other Documentation'),
                });
            }
            return Promise.reject(new Error('Not Found'));
        });

        renderWithAuthProvider(DisplayDocumentation, null, {
            initialFile: 'README.md',
        });

        await waitFor(() => {
            expect(screen.getByText('Test Documentation')).toBeInTheDocument();
        });

        const link = screen.getByText('Test Documentation');

        act(() => {
            userEvent.click(link);
        });

        await waitFor(() => {
            expect(global.fetch).toHaveBeenLastCalledWith('test.md');
        });
    });

    it('displays an error message if a file cannot be loaded', async () => {
        (global.fetch as Mock).mockResolvedValueOnce({
            ok: false,
        });

        renderWithAuthProvider(DisplayDocumentation, null, {
            initialFile: 'nonexistent.md',
        });

        await waitFor(() => {
            expect(screen.getByText('Error')).toBeInTheDocument();
            expect(
                screen.getByText('Could not load the file.')
            ).toBeInTheDocument();
        });
    });

    it('handles internal links correctly', async () => {
        (global.fetch as Mock).mockResolvedValueOnce({
            ok: true,
            text: () => Promise.resolve('[Internal](#anchor)\n\n# anchor'),
        });

        renderWithAuthProvider(DisplayDocumentation, null, {
            initialFile: 'README.md',
        });

        await waitFor(() => {
            const link = screen.getByText('Internal');
            expect(link).toHaveAttribute('href', '#anchor');
        });
    });

    it('handles external and relative links correctly', async () => {
        (global.fetch as Mock).mockResolvedValueOnce({
            ok: true,
            text: () =>
                Promise.resolve(
                    '[External](http://example.com) [Internal](../internal.md)'
                ),
        });

        renderWithAuthProvider(DisplayDocumentation, null, {
            initialFile: 'README.md',
        });

        await waitFor(() => {
            const externalLink = screen.getByText('External');
            const internalLink = screen.getByText('Internal');

            expect(externalLink).toHaveAttribute('href', 'http://example.com');
            expect(externalLink).toHaveAttribute('target', '_blank');
            expect(externalLink).toHaveAttribute('rel', 'noopener noreferrer');

            expect(internalLink).toHaveAttribute('href', '#');
        });
    });

    it('does not convert <p> elements to <pre> if the file ends with .md', async () => {
        (global.fetch as Mock).mockResolvedValueOnce({
            ok: true,
            text: () => Promise.resolve('A short text'),
        });

        renderWithAuthProvider(DisplayDocumentation, null, {
            initialFile: 'README.md',
        });

        await waitFor(() => {
            const pElement = screen.getByText('A short text');
            expect(pElement.tagName).toBe('P');
        });
    });

    it('loads the home file when the Home button is clicked', async () => {
        (global.fetch as Mock).mockImplementation((url) => {
            if (url === 'README.md') {
                return Promise.resolve({
                    ok: true,
                    text: () => Promise.resolve('# Home Documentation'),
                });
            }
            return Promise.reject(new Error('Not Found'));
        });

        renderWithAuthProvider(DisplayDocumentation, null, {
            initialFile: 'other.md',
        });

        const homeButton = screen.getByRole('button', { name: 'Home' });

        userEvent.click(homeButton);

        await waitFor(() => {
            expect(screen.getByText('Home Documentation')).toBeInTheDocument();
        });

        expect(global.fetch).toHaveBeenCalledWith('README.md');
    });

    describe('non-.md files', () => {
        it('for non-.md files: converts <p> elements to <pre> if the condition is met', async () => {
            (global.fetch as Mock).mockResolvedValueOnce({
                ok: true,
                text: () => Promise.resolve('A long\ntext block'),
            });

            renderWithAuthProvider(DisplayDocumentation, null, {
                initialFile: 'README.txt',
            });

            await waitFor(() => {
                const preElement = screen.getByText('A long text block');
                expect(preElement.tagName).toBe('PRE');
            });
        });

        it('for non-.md files: does not convert <p> elements to <pre> if the condition is not met', async () => {
            (global.fetch as Mock).mockResolvedValueOnce({
                ok: true,
                text: () => Promise.resolve('A single text line'),
            });

            renderWithAuthProvider(DisplayDocumentation, null, {
                initialFile: 'README.txt',
            });

            await waitFor(() => {
                const preElement = screen.getByText('A single text line');
                expect(preElement.tagName).toBe('P');
            });
        });
    });
});
