import React from 'react';
import { JSONObject, JSONValue } from '../types';
import '../styles/displayJSON.css';

export const DisplayJSON = ({ json }: { json: JSONObject | string }) => {
    console.log(json);
    const parsedJson: JSONObject =
        typeof json === 'string'
            ? JSON.parse(
                  json.replace('Infinity', '"Infinity"').replace('NaN', '"NaN"')
              )
            : json;

    const renderJSON = (
        value: JSONValue,
        depth: number = 0
    ): React.ReactNode => {
        if (typeof value === 'object') {
            if (Array.isArray(value)) {
                return (
                    <ul style={{ paddingLeft: `${depth * 1}rem` }}>
                        {value.map((item) => (
                            <li key={JSON.stringify(item)}>
                                {renderJSON(item, depth + 1)}
                            </li>
                        ))}
                    </ul>
                );
            }
            return (
                <ul style={{ paddingLeft: `${depth * 1}rem` }}>
                    {Object.entries(value).map(([key, val]) => (
                        <li key={key}>
                            <strong>{key}: </strong>
                            {renderJSON(val, depth + 1)}
                        </li>
                    ))}
                </ul>
            );
        }
        return <span>{value === Infinity ? '∞' : String(value)}</span>;
    };

    return (
        <article className="json-display">
            <section>{renderJSON(parsedJson)}</section>
        </article>
    );
};
