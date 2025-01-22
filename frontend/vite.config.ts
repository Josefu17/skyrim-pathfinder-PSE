import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const enableRestrictDocsAccess = false;

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        react(),
        enableRestrictDocsAccess
            ? {
                  name: 'vite-plugin-restrict-docs-access',
                  configureServer(server) {
                      server.middlewares.use((req, res, next) => {
                          const restricted = [
                              '/docs/Postman/', // Verzeichnis blockieren
                              '.pdf', // Dateien mit der Endung .pdf blockieren
                          ];

                          if (
                              restricted.some((pattern) =>
                                  req.url?.includes(pattern)
                              )
                          ) {
                              res.statusCode = 403; // Forbidden error
                              res.end('Access to this file is restricted.');
                              return;
                          }

                          next();
                      });
                  },
              }
            : undefined,
    ],
    /*server: {
        fs: {
            allow: ['/', '../docs/', '../../README.md'], // allow access to specified folders and files
        },
    },*/
});
