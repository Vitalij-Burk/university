import json
from uuid import uuid4

import pytest


async def test_update_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
        "is_active": True,
    }
    user_data_updated = {
        "name": "Misha",
        "surname": "Debil",
        "email": "misha@debil.com",
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data["user_id"]}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_updated["name"]
    assert user_from_db["surname"] == user_data_updated["surname"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data["is_active"]
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_update_user_check_one_is_updated(
    client, create_user_in_database, get_user_from_database
):
    user_data1 = {
        "user_id": uuid4(),
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
        "is_active": True,
    }
    user_data2 = {
        "user_id": uuid4(),
        "name": "Petr",
        "surname": "Suka",
        "email": "petr@suka.com",
        "is_active": True,
    }
    user_data_updated = {
        "name": "Misha",
        "surname": "Debil",
        "email": "misha@debil.com",
    }
    for user_data in [user_data1, user_data2]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data1["user_id"]}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == 200
    data_from_resp = resp.json()
    assert data_from_resp["updated_user_id"] == str(user_data1["user_id"])
    users_from_db = await get_user_from_database(user_data1["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_updated["name"]
    assert user_from_db["surname"] == user_data_updated["surname"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data1["is_active"]
    assert user_from_db["user_id"] == user_data1["user_id"]

    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data2["name"]
    assert user_from_db["surname"] == user_data2["surname"]
    assert user_from_db["email"] == user_data2["email"]
    assert user_from_db["is_active"] is user_data2["is_active"]
    assert user_from_db["user_id"] == user_data2["user_id"]


@pytest.mark.parametrize(
    "user_data_updated, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": "At least one parameter for user update info should be provided"
            },
        ),
        ({"name": "123"}, 422, {"detail": "Name should contains only letters"}),
        (
            {"email": ""},
            422,
            {
                "detail": [
                    {
                        "type": "value_error",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: An email address must have an @-sign.",
                        "input": "",
                        "ctx": {"reason": "An email address must have an @-sign."},
                    }
                ]
            },
        ),
        (
            {"surname": ""},
            422,
            {
                "detail": [
                    {
                        "type": "string_too_short",
                        "loc": ["body", "surname"],
                        "msg": "String should have at least 1 character",
                        "input": "",
                        "ctx": {"min_length": 1},
                    }
                ]
            },
        ),
        (
            {"name": ""},
            422,
            {
                "detail": [
                    {
                        "type": "string_too_short",
                        "loc": ["body", "name"],
                        "msg": "String should have at least 1 character",
                        "input": "",
                        "ctx": {"min_length": 1},
                    }
                ]
            },
        ),
        ({"surname": "123"}, 422, {"detail": "Surname should contains only letters"}),
        (
            {"email": "123"},
            422,
            {
                "detail": [
                    {
                        "type": "value_error",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: An email address must have an @-sign.",
                        "input": "123",
                        "ctx": {"reason": "An email address must have an @-sign."},
                    }
                ]
            },
        ),
    ],
)
async def test_update_user_validation_error(
    client,
    create_user_in_database,
    user_data_updated,
    expected_status_code,
    expected_detail,
):
    user_data = {
        "user_id": uuid4(),
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
        "is_active": True,
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data["user_id"]}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == expected_status_code
    data_from_resp = resp.json()
    assert data_from_resp == expected_detail


async def test_update_user_id_validation_error(client):
    user_data_updated = {
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
    }
    resp = client.patch(f"/user/?user_id=123", data=json.dumps(user_data_updated))
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


async def test_update_user_not_found_error(client):
    user_data_updated = {
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
    }
    user_id = uuid4()
    resp = client.patch(f"/user/?user_id={user_id}", data=json.dumps(user_data_updated))
    assert resp.status_code == 404
    data_from_resp = resp.json()
    assert data_from_resp == {"detail": f"User with id {user_id} not found"}


async def test_update_user_duplicate_email_error(client, create_user_in_database):
    user_data1 = {
        "user_id": uuid4(),
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
        "is_active": True,
    }
    user_data2 = {
        "user_id": uuid4(),
        "name": "Petr",
        "surname": "Suka",
        "email": "petr@suka.com",
        "is_active": True,
    }
    user_data_updated = {"email": user_data2["email"]}
    for user_data in [user_data1, user_data2]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data1["user_id"]}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == 503
    data_from_resp = resp.json()
    assert (
        'duplicate key value violates unique constraint "users_email_key"'
        in data_from_resp["detail"]
    )
