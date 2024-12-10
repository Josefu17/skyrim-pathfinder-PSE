"""simple integration tests to cover basic and edge cases for the RouteDao"""

from datetime import datetime, timedelta, timezone

import pytest

from backend.src.database.dao.route_dao import RouteDao
from backend.src.database.schema.route import Route, RouteFilter
from backend.src.database.schema.user import User


def test_save_route(db):
    """Test saving a new route."""
    # Arrange
    user = User(username="test_user")
    db.add(user)
    db.commit()

    route = Route(
        user_id=user.id,
        startpoint="Whiterun",
        endpoint="Riften",
        created_at=datetime.now(timezone.utc),
        route={"route": {}, "distance": 100},
    )

    # Act
    saved_route = RouteDao.save_route(route, db)

    # Assert
    assert saved_route.id is not None
    assert saved_route.startpoint == "Whiterun"


def test_get_route_by_id(db):
    """Test retrieving a route by its ID."""
    # Arrange
    user = User(username="test_user")
    db.add(user)
    db.commit()

    fabricate_basic_routes_and_commit(
        db, datetime.now(timezone.utc), datetime.now(timezone.utc), user
    )

    # Act - retrieve the first one
    retrieved_route = RouteDao.get_route_by_id(1, db)

    # Assert
    assert retrieved_route is not None
    assert retrieved_route.startpoint == "Riverwood"


def test_delete_route_by_id_success(db):
    """Test deleting a route by its ID."""
    # Arrange
    user = User(username="test_user")
    db.add(user)
    db.commit()

    route = Route(
        user_id=user.id,
        startpoint="Riften",
        endpoint="Markarth",
        created_at=datetime.now(timezone.utc),
        route={"route": {}, "distance": 300},
    )
    db.add(route)
    db.commit()

    # Act
    result = RouteDao.delete_route_by_id(route.id, db)
    deleted_route = RouteDao.get_route_by_id(route.id, db)

    # Assert
    assert result is True
    assert deleted_route is None


def test_delete_route_by_id_no_match(db):
    """Test delete_route_by_id returns False when no route matches the given ID."""
    # Arrange
    user = User(username="test_user")
    db.add(user)
    db.commit()

    route = Route(
        user_id=user.id,
        startpoint="Solitude",
        endpoint="Whiterun",
        created_at=datetime.now(timezone.utc),
        route={"route": {}, "distance": 300},
    )
    db.add(route)
    db.commit()

    invalid_route_id = route.id + 1  # A non-existent route ID

    # Act
    result = RouteDao.delete_route_by_id(invalid_route_id, db)

    # Assert
    assert result is False


def test_delete_user_route_history_by_user_id(db):
    """Test deleting all routes for a user by user_id."""
    # Arrange
    user = User(username="test_user")
    db.add(user)
    db.commit()

    routes = [
        Route(
            user_id=user.id,
            startpoint="Whiterun",
            endpoint="Riften",
            created_at=datetime.now(timezone.utc),
            route={"route": {}, "distance": 100},
        ),
        Route(
            user_id=user.id,
            startpoint="Markarth",
            endpoint="Solitude",
            created_at=datetime.now(timezone.utc) - timedelta(days=1),
            route={"route": {}, "distance": 200},
        ),
    ]
    db.add_all(routes)
    db.commit()

    # Act
    deleted_count = RouteDao.delete_user_route_history(db, user_id=user.id)

    # Assert
    assert deleted_count == 2
    assert not RouteDao.get_routes(RouteFilter(user_id=user.id), db)


def test_delete_user_route_history_by_username(db):
    """Test deleting all routes for a user by username."""
    # Arrange
    user = User(username="test_user")
    db.add(user)
    db.commit()

    route = Route(
        user_id=user.id,
        startpoint="Riverwood",
        endpoint="Helgen",
        created_at=datetime.now(timezone.utc),
        route={"route": {}, "distance": 50},
    )
    db.add(route)
    db.commit()

    # Act
    deleted_count = RouteDao.delete_user_route_history(db, username=user.username)

    # Assert
    assert deleted_count == 1
    assert not RouteDao.get_routes(RouteFilter(user_id=user.id), db)


def test_delete_user_route_history_no_user_id_or_username(db):
    """Test ValueError when neither user_id nor username is provided."""
    # Act & Assert
    with pytest.raises(
        ValueError, match="Either 'user_id' or 'username' must be provided."
    ):
        RouteDao.delete_user_route_history(db)


def test_delete_user_route_history_invalid_username(db):
    """Test ValueError when the username does not exist."""
    # Arrange
    invalid_username = "nonexistent_user"

    # Act & Assert
    with pytest.raises(
        ValueError, match=f"User with username '{invalid_username}' does not exist."
    ):
        RouteDao.delete_user_route_history(db, username=invalid_username)


def test_get_routes_with_to_date(db):
    """Test filtering routes by to_date."""
    # Arrange
    user = User(username="test_user")
    db.add(user)
    db.commit()

    recent_date = datetime.now(timezone.utc)
    old_date = recent_date - timedelta(days=5)

    fabricate_basic_routes_and_commit(db, old_date, recent_date, user)

    optional_filters = {"to_date": recent_date - timedelta(days=3)}
    filter_params = RouteFilter(user_id=user.id, optional_filters=optional_filters)

    # Act
    retrieved_routes = RouteDao.get_routes(filter_params, db)

    # Assert
    assert len(retrieved_routes) == 1
    assert retrieved_routes[0].startpoint == "Winterhold"


def test_get_routes_with_combination_filters(db):
    """Test filtering routes by startpoint and endpoint."""
    # Arrange
    user1 = User(username="user1")
    user2 = User(username="user2")
    db.add_all([user1, user2])
    db.commit()

    routes = [
        Route(
            user_id=user1.id,
            startpoint="Whiterun",
            endpoint="Riften",
            created_at=datetime.now(timezone.utc),
            route={"route": {}, "distance": 100},
        ),
        Route(
            user_id=user1.id,
            startpoint="Markarth",
            endpoint="Solitude",
            created_at=datetime.now(timezone.utc) - timedelta(days=1),
            route={"route": {}, "distance": 200},
        ),
        Route(
            user_id=user2.id,
            startpoint="Riverwood",
            endpoint="Falkreath",
            created_at=datetime.now(timezone.utc) - timedelta(days=2),
            route={"route": {}, "distance": 50},
        ),
        Route(
            user_id=user2.id,
            startpoint="Whiterun",
            endpoint="Riften",
            created_at=datetime.now(timezone.utc),
            route={"route": {}, "distance": 150},
        ),
    ]
    db.add_all(routes)
    db.commit()

    optional_filters = {"startpoint": "Whiterun", "endpoint": "Riften"}
    filter_params = RouteFilter(user_id=user1.id, optional_filters=optional_filters)

    # Act
    retrieved_routes = RouteDao.get_routes(filter_params, db)

    # Assert
    assert len(retrieved_routes) == 1
    assert retrieved_routes[0].user_id == user1.id
    assert retrieved_routes[0].startpoint == "Whiterun"


def test_get_routes_with_date_range(db):
    """Test retrieving routes within a specific date range."""
    # Arrange
    user = User(username="test_user")
    db.add(user)
    db.commit()

    recent_date = datetime.now(timezone.utc)
    old_date = recent_date - timedelta(days=10)

    fabricate_basic_routes_and_commit(db, old_date, recent_date, user)

    optional_filters = {"from_date": recent_date}
    filter_params = RouteFilter(user_id=user.id, optional_filters=optional_filters)

    # Act
    retrieved_routes = RouteDao.get_routes(filter_params, db)

    # Assert
    assert len(retrieved_routes) == 1
    assert retrieved_routes[0].startpoint == "Riverwood"

    # Act
    retrieved_routes = RouteDao.get_routes(filter_params, db)

    # Assert
    assert len(retrieved_routes) == 1
    assert retrieved_routes[0].startpoint == "Riverwood"


def test_get_routes_sorted_by_endpoint(db):
    """Test retrieving routes sorted by endpoint."""
    # Arrange
    user = User(username="test_user")
    db.add(user)
    db.commit()

    routes = [
        Route(
            user_id=user.id,
            startpoint="Falkreath",
            endpoint="Alduin's Wall",
            created_at=datetime.now(timezone.utc),
            route={"route": {}, "distance": 500},
        ),
        Route(
            user_id=user.id,
            startpoint="Falkreath",
            endpoint="Ivarstead",
            created_at=datetime.now(timezone.utc) - timedelta(hours=1),
            route={"route": {}, "distance": 300},
        ),
    ]
    db.add_all(routes)
    db.commit()

    filter_params = RouteFilter(user_id=user.id, field="endpoint", descending=False)

    # Act
    retrieved_routes = RouteDao.get_routes(filter_params, db)

    # Assert
    assert len(retrieved_routes) == 2
    assert retrieved_routes[0].endpoint == "Alduin's Wall"


def test_get_routes_limit_and_sorting(db):
    """Test limiting the number of routes returned and sorting by created_at."""
    # Arrange
    user = User(username="test_user")
    db.add(user)
    db.commit()

    routes = [
        Route(
            user_id=user.id,
            startpoint="Markarth",
            endpoint="Riften",
            created_at=datetime.now(timezone.utc),
            route={"route": {}, "distance": 150},
        ),
        Route(
            user_id=user.id,
            startpoint="Whiterun",
            endpoint="Winterhold",
            created_at=datetime.now(timezone.utc) - timedelta(days=1),
            route={"route": {}, "distance": 250},
        ),
    ]
    db.add_all(routes)
    db.commit()

    filter_params = RouteFilter(
        user_id=user.id, limit=1, field="created_at", descending=True
    )

    # Act
    retrieved_routes = RouteDao.get_routes(filter_params, db)

    # Assert
    assert len(retrieved_routes) == 1
    assert retrieved_routes[0].startpoint == "Markarth"


def test_get_routes_with_invalid_sort_field(db):
    """Test behavior when an invalid sorting field is provided."""
    # Arrange
    user = User(username="test_user")
    db.add(user)
    db.commit()

    filter_params = RouteFilter(user_id=user.id, field="invalid_field")

    # Act & Assert
    try:
        RouteDao.get_routes(filter_params, db)
    except ValueError as e:
        assert str(e) == "Invalid sorting field: invalid_field"


def fabricate_basic_routes_and_commit(db, old_date, recent_date, user):
    """Helper to create routes and commit them to the RAM-Database"""
    routes = [
        Route(
            user_id=user.id,
            startpoint="Riverwood",
            endpoint="Helgen",
            created_at=recent_date,
            route={"route": {}, "distance": 50},
        ),
        Route(
            user_id=user.id,
            startpoint="Winterhold",
            endpoint="Dawnstar",
            created_at=old_date,
            route={"route": {}, "distance": 75},
        ),
    ]
    db.add_all(routes)
    db.commit()
