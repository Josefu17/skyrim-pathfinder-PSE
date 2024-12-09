import winston from 'winston';

// configure Log-Level and -Format
export const logger = winston.createLogger({
    level: 'info', // Standard-Log-Level
    transports: [
        new winston.transports.Console({
            format: winston.format.combine(
                winston.format.colorize(),
                winston.format.simple()
            ),
        }),
    ],
});
