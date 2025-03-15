from uuid import uuid4

from tests.conftest import create_test_auth_headers_for_user
from tests.conftest import create_user_in_database


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
        "is_active": True,
        "hashed_password": "string",
    }
    await create_user_in_database(**user_data)
    resp = client.delete(
        f"/user/?user_id={user_data["user_id"]}",
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_delete_user_not_found(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Admin",
        "surname": "Adminov",
        "email": "admin@kek.com",
        "is_active": True,
        "hashed_password": "string",
    }
    await create_user_in_database(**user_data)
    user_id = uuid4()
    resp = client.delete(
        f"/user/?user_id={user_id}",
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )
    assert resp.status_code == 404
    data_from_resp = resp.json()
    assert data_from_resp == {"detail": f"User with id {user_id} not found"}


async def test_delete_user_bad_creds(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Admin",
        "surname": "Adminov",
        "email": "admin@kek.com",
        "is_active": True,
        "hashed_password": "string",
    }
    await create_user_in_database(**user_data)
    user_id = uuid4()
    resp = client.delete(
        f"/user/?user_id={user_id}",
        headers=create_test_auth_headers_for_user(user_data["email"] + "a"),
    )
    assert resp.status_code == 401
    data_from_resp = resp.json()
    assert data_from_resp == {"detail": "Could not validate credentials"}


async def test_delete_user_unauth(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Admin",
        "surname": "Adminov",
        "email": "admin@kek.com",
        "is_active": True,
        "hashed_password": "string",
    }
    await create_user_in_database(**user_data)
    user_id = uuid4()
    bad_auth_headers = create_test_auth_headers_for_user(user_data["email"])
    bad_auth_headers["Authorization"] += "a"
    resp = client.delete(
        f"/user/?user_id={user_id}",
        headers=bad_auth_headers,
    )
    assert resp.status_code == 401
    data_from_resp = resp.json()
    assert data_from_resp == {"detail": "Could not validate credentials"}


async def test_delete_user_no_token(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Admin",
        "surname": "Adminov",
        "email": "admin@kek.com",
        "is_active": True,
        "hashed_password": "string",
    }
    await create_user_in_database(**user_data)
    user_id = uuid4()
    resp = client.delete(
        f"/user/?user_id={user_id}",
    )
    assert resp.status_code == 401
    data_from_resp = resp.json()
    assert data_from_resp == {"detail": "Not authenticated"}


async def test_delete_user_id_validation_error(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Admin",
        "surname": "Adminov",
        "email": "admin@kek.com",
        "is_active": True,
        "hashed_password": "string",
    }
    await create_user_in_database(**user_data)
    resp = client.delete(
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
