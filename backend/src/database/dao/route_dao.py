"""Data Access Object for Routes"""

from typing import cast

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from backend.src.database.dao.user_dao import UserDao
from backend.src.database.schema.route import Route
from backend.src.database.schema.route import RouteFilter


class RouteDao:
    """Data Access Object for Routes"""

    @staticmethod
    def save_route(route: Route, session: Session) -> Route:
        """Save a new route"""
        session.add(route)
        session.commit()
        return route

    @staticmethod
    def get_route_by_id(route_id: int, session: Session) -> Route | None:
        """Retrieve a route by its ID"""
        return session.query(Route).filter_by(id=route_id).first()

    @staticmethod
    def get_routes(filter_params: RouteFilter, session: Session) -> list[Route]:
        """
        Retrieve a list of routes for a user, with optional filtering and sorting.

        This method fetches a user's route history based on various criteria such as date range,
        startpoint, or endpoint. Results can be sorted by a specified field and limited to a maximum
        number of entries.

        :param filter_params: An instance of RouteFilter containing:
            - user_id: The ID of the user whose routes are being queried.
            - field: The field to sort by ("created_at" (default), "startpoint", or "endpoint").
            - limit: Maximum number of results to return (default: 10, capped at 100).
            - descending: Whether to sort in descending order (default: True).
            - from_date: Start of the date range for filtering (optional).
            - to_date: End of the date range for filtering (optional).
            - startpoint: Filter by route starting point (optional).
            - endpoint: Filter by route ending point (optional).
        :param session: db session.

        :return: A list of Route objects matching the filters and sorted by the specified field.
        :raises ValueError: If an invalid sorting field is provided.
        """
        (
            user_id,
            field,
            limit,
            descending,
            from_date,
            to_date,
            startpoint,
            endpoint,
        ) = filter_params.destructure()

        # Enforce a max limit of 100
        limit = min(limit, 100)

        # Validate the sorting field
        if field not in ["created_at", "startpoint", "endpoint"]:
            raise ValueError(f"Invalid sorting field: {field}")

        # Dynamically determine the sorting column
        sort_column = getattr(Route, field)
        order = desc(sort_column) if descending else asc(sort_column)

        # Build dynamic filter conditions
        conditions = [Route.user_id == user_id]

        if from_date:
            conditions.append(Route.created_at >= from_date)
        if to_date:
            conditions.append(Route.created_at <= to_date)
        if startpoint:
            conditions.append(Route.startpoint == startpoint)
        if endpoint:
            conditions.append(Route.endpoint == endpoint)

        # Apply conditions and sorting, then limit results - handle everything in one go,
        # letting the DBMS optimize as much as possible
        return cast(
            list[Route],
            session.query(Route).filter(*conditions).order_by(order).limit(limit).all(),
        )

    @staticmethod
    def delete_route_by_id(route_id: int, session: Session) -> bool:
        """Delete a specific route by its ID, return True if deleted, else False"""
        route = session.query(Route).filter_by(id=route_id).first()
        if route:
            session.delete(route)
            session.commit()
            return True
        return False

    @staticmethod
    def delete_routes_by_ids(route_ids: list[int], session: Session) -> int:
        """Delete multiple routes by their IDs,
        return number of deleted routes"""
        deleted_count = (
            session.query(Route)
            .filter(Route.id.in_(route_ids))
            .delete(synchronize_session=False)
        )
        session.commit()
        return deleted_count

    @staticmethod
    def delete_user_route_history(
        session: Session, user_id: int = None, username: str = None
    ) -> int:
        """
        Delete all routes for a user by user_id or username and return number of routes deleted.
        """
        if not user_id and not username:
            raise ValueError("Either 'user_id' or 'username' must be provided.")

        if username:
            user = UserDao.get_user_by_username(username, session)
            if not user:
                raise ValueError(f"User with username '{username}' does not exist.")
            user_id = user.id

        deleted_count = session.query(Route).filter_by(user_id=user_id).delete()
        session.commit()
        return deleted_count
