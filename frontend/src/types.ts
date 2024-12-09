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

export type TCityOptionProps = {
    name: string;
    onClick: (name: string) => void;
};
