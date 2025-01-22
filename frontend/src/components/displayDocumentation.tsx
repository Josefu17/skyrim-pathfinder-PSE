import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeRewrite from 'rehype-rewrite';

import { CustomNode } from '../types';

export const DisplayDocumentation = ({
    initialFile = 'README.md',
}: {
    initialFile: string;
}) => {
    const [currentFile, setCurrentFile] = useState<string>(initialFile);
    const [content, setContent] = useState<string>(''); // Markdown content

    const loadMarkdown = async (filePath: string) => {
        try {
            if (filePath === '' && initialFile === '') filePath = 'README.md';

            console.log('Loading file:', filePath);

            const response = await fetch(filePath);
            if (!response.ok) {
                throw new Error(`File not found: ${filePath}`);
            }
            const text = await response.text();
            setContent(text);
        } catch (error) {
            console.error('Error loading markdown file:', error);
            setContent('# Error\nCould not load the file.');
        }
    };

    const updateRelativePath = (
        href: string,
        pathSegments: string[] = currentFile.split('/').filter(Boolean)
    ) => {
        // Entferne immer die Datei am Ende des aktuellen Pfads
        if (pathSegments.length > 0) {
            pathSegments.pop();
        }
        console.log('Path segments:', pathSegments);

        // Verarbeite den neuen `href`
        if (href.startsWith('../')) {
            // Navigiere eine Ebene höher
            href = href.replace('../', ''); // Entferne '../' aus dem href
            return updateRelativePath(href, pathSegments); // Rekursiver Aufruf mit aktualisierten Segmenten
        } else if (href.startsWith('./')) {
            // Ignoriere './', bleibe im aktuellen Ordner
            href = href.replace('./', '');
        }
        console.log('New href:', href);

        // Füge den verbleibenden Pfad an
        return `${[...pathSegments, href].join('/')}`;
    };

    useEffect(() => {
        loadMarkdown(currentFile);
    }, [currentFile]);

    return (
        <>
            <input
                type="button"
                value="Home"
                onClick={() => setCurrentFile('README.md')}
            />
            <section id="documentation">
                {/* Markdown-Rendering mit dynamischem Link-Handling */}
                <ReactMarkdown
                    rehypePlugins={[
                        [
                            rehypeRewrite,
                            {
                                rewrite: (node: CustomNode) => {
                                    // Verarbeite Anker-Links
                                    if (
                                        node.tagName === 'a' &&
                                        node.properties?.href
                                    ) {
                                        const href = node.properties.href;

                                        if (
                                            typeof href === 'string' &&
                                            href.startsWith('#')
                                        ) {
                                            // Interne Verweise (Anchor Links) - Standardverhalten
                                            node.properties.href = href;
                                        } else if (
                                            typeof href === 'string' &&
                                            (href.startsWith('http://') ||
                                                href.startsWith('https://'))
                                        ) {
                                            // Externe Verweise (z. B. YouTube) - Standardverhalten
                                            node.properties.target = '_blank'; // In neuem Tab öffnen
                                            node.properties.rel =
                                                'noopener noreferrer'; // Sicherheitsrichtlinien
                                        } else {
                                            // Externe Verweise auf andere Dateien - Dynamisches Laden
                                            node.properties.onClick = (e) => {
                                                e.preventDefault(); // Standard-Link-Verhalten verhindern
                                                const newPath =
                                                    updateRelativePath(href);
                                                setCurrentFile(newPath);
                                            };
                                            node.properties.href = '#'; // Dummy-URL setzen
                                        }
                                    }

                                    // Verarbeite Überschriften
                                    if (
                                        [
                                            'h1',
                                            'h2',
                                            'h3',
                                            'h4',
                                            'h5',
                                            'h6',
                                        ].includes(node.tagName)
                                    ) {
                                        const textContent = node.children
                                            .filter(
                                                (child) => child.type === 'text'
                                            )
                                            .map((child) => child.value)
                                            .join('');
                                        const id = textContent
                                            .toLowerCase()
                                            .replace(/\s+/g, '-') // Leerzeichen zu Bindestrich
                                            .replace(/[^\w-]+/g, ''); // Sonderzeichen entfernen
                                        node.properties = {
                                            ...node.properties,
                                            id,
                                        };
                                    }

                                    // Verarbeite <p>-Elemente mit mehreren Zeilen
                                    if (
                                        node.tagName === 'p' &&
                                        !currentFile.endsWith('.md')
                                    ) {
                                        const textContent = node.children
                                            .filter(
                                                (child) => child.type === 'text'
                                            )
                                            .map((child) => child.value)
                                            .join('\n'); // Verbinde die Texte mit Zeilenumbrüchen

                                        if (textContent.includes('\n')) {
                                            // Wenn das <p>-Element mehrere Zeilen hat, konvertiere es zu <pre>
                                            node.tagName = 'pre';
                                            node.children = [
                                                {
                                                    ...node,
                                                    type: 'text',
                                                    value: textContent,
                                                },
                                            ];
                                        }
                                    }
                                },
                            },
                        ],
                    ]}
                >
                    {content}
                </ReactMarkdown>
            </section>
        </>
    );
};
