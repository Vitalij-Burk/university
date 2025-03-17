from uuid import uuid4

from db.models import PortalRole
from tests.conftest import create_test_auth_headers_for_user


async def test_get_user(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
        "is_active": True,
        "hashed_password": "string",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    resp = client.get(
        f"/user/?user_id={user_data["user_id"]}",
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp["user_id"] == str(user_data["user_id"])
    assert data_from_resp["name"] == str(user_data["name"])
    assert data_from_resp["surname"] == str(user_data["surname"])
    assert data_from_resp["email"] == str(user_data["email"])
    assert data_from_resp["is_active"] == user_data["is_active"]


async def test_get_user_id_validation_error(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
        "is_active": True,
        "hashed_password": "string",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    resp = client.get(
        f"/user/?user_id=123",
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )
    assert resp.status_code == 422
    data_from_resp = resp.json()
    assert data_from_resp == {
        "detail": [
            {
                "type": "uuid_parsing",
                "loc": ["query", "user_id"],
                "msg": "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 3",
                "input": "123",
                "ctx": {
                    "error": "invalid length: expected length 32 for simple format, found 3"
                },
            }
        ]
    }


async def test_get_user_not_found(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
        "is_active": True,
        "hashed_password": "string",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    user_id_for_finding = uuid4()
    resp = client.get(
        f"/user/?user_id={user_id_for_finding}",
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )
    assert resp.status_code == 404
    data_from_resp = resp.json()
    assert data_from_resp == {"detail": f"User with id {user_id_for_finding} not found"}


async def test_get_user_bad_creds(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Admin",
        "surname": "Adminov",
        "email": "admin@kek.com",
        "is_active": True,
        "hashed_password": "string",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    user_id = uuid4()
    resp = client.get(
        f"/user/?user_id={user_id}",
        headers=create_test_auth_headers_for_user(user_data["email"] + "a"),
    )
    assert resp.status_code == 401
    data_from_resp = resp.json()
    assert data_from_resp == {"detail": "Could not validate credentials"}


async def test_get_user_unauth(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Admin",
        "surname": "Adminov",
        "email": "admin@kek.com",
        "is_active": True,
        "hashed_password": "string",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    user_id = uuid4()
    bad_auth_headers = create_test_auth_headers_for_user(user_data["email"])
    bad_auth_headers["Authorization"] += "a"
    resp = client.get(
        f"/user/?user_id={user_id}",
        headers=bad_auth_headers,
    )
    assert resp.status_code == 401
    data_from_resp = resp.json()
    assert data_from_resp == {"detail": "Could not validate credentials"}


async def test_get_user_no_token(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Admin",
        "surname": "Adminov",
        "email": "admin@kek.com",
        "is_active": True,
        "hashed_password": "string",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    user_id = uuid4()
    resp = client.get(
        f"/user/?user_id={user_id}",
    )
    assert resp.status_code == 401
    data_from_resp = resp.json()
    assert data_from_resp == {"detail": "Not authenticated"}
