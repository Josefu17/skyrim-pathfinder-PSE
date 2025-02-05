import { ReactNode } from 'react';
import { NavigateFunction } from 'react-router-dom';

export type JSONValue = string | number | boolean | JSONObject | JSONArray;

export type JSONObject = {
    [key: string]: JSONValue;
};

export type JSONArray = JSONValue[];

export type TConnection = {
    child_city_id: number;
    parent_city_id: number;
};

export type TConnections = TConnection[];

export type TCity = {
    id: number;
    name: string;
    position_x: number;
    position_y: number;
};

export type TCities = TCity[];

export type TRoute = {
    [key: string]: string;
};

export type TRouteData = {
    route: TRoute;
    distance: number;
    alternative_route: TRoute;
    alternative_distance: number;
};

export type TStrRouteData = {
    id: number;
    startpoint: string;
    endpoint: string;
    route: Record<string, unknown>; // serializable object for JSON
};

export type TStrRoutes = TStrRouteData[];

export type TCityOptionProps = {
    name: string;
    onClick: (name: string) => void;
};

export type TFilterOptions = {
    limit: number;
    descending: boolean;
    from_date: string;
    map_id: number;
    to_date: string;
    startpoint: string;
    endpoint: string;
};

export type TUser = {
    id: number;
    username: string;
};

export type TMap = {
    id: number;
    name: string;
    size_x?: number;
    size_y?: number;
};

export type TAuthContext = {
    user: TUser | null;
    setUser: (user: TUser | null) => void; // Function to update user
    loading: boolean;
};

export type TMapContext = {
    currentMap: TMap | null;
    setCurrentMap: (map: TMap | null) => void;
    loading: boolean;
};

export type ErrorBoundaryProps = {
    fallback: ReactNode; // UI, die angezeigt wird, wenn ein Fehler auftritt
    children: ReactNode; // Die Kinder, die von der ErrorBoundary geschützt werden
    navigate: NavigateFunction; // Navigationsfunktion von React Router
};

export type ErrorBoundaryState = {
    hasError: boolean; // Gibt an, ob ein Fehler aufgetreten ist
};

export type CustomNode = Node & {
    tagName: string;
    children: ChildNode[];
    properties: {
        id?: string;
        href: string;
        onClick?: (e: React.MouseEvent<HTMLAnchorElement>) => void;
        target?: '_self' | '_blank' | '_parent' | '_top';
        rel?: string | string[];
    };
};

type ChildNode = Node & {
    type: 'text' | 'element' | 'comment';
    value: string;
};
