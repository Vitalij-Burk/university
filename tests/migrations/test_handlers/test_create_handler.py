import json

import pytest


async def test_create_user(client, get_user_from_database):
    user_data = {
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
        "password": "string",
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


async def test_create_user_duplicate_email_error(client, get_user_from_database):
    user_data = {
        "name": "Mikhail",
        "surname": "Eblan",
        "email": "mikhail@eblan.com",
        "password": "string",
    }
    user_data_same_email = {
        "name": "Petr",
        "surname": "Suka",
        "email": "mikhail@eblan.com",
        "password": "string",
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    resp = client.post("/user/", data=json.dumps(user_data_same_email))
    assert resp.status_code == 503
    data_from_resp = resp.json()
    assert (
        'duplicate key value violates unique constraint "users_email_key"'
        in data_from_resp["detail"]
    )


@pytest.mark.parametrize(
    "user_data_for_creation, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "input": {},
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "surname"],
                        "msg": "Field required",
                        "input": {},
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "email"],
                        "msg": "Field required",
                        "input": {},
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "password"],
                        "msg": "Field required",
                        "input": {},
                    },
                ]
            },
        ),
        (
            {"name": 123, "surname": 456, "email": "lol", "password": "string"},
            422,
            {
                "detail": [
                    {
                        "type": "string_type",
                        "loc": ["body", "name"],
                        "msg": "Input should be a valid string",
                        "input": 123,
                    },
                    {
                        "type": "string_type",
                        "loc": ["body", "surname"],
                        "msg": "Input should be a valid string",
                        "input": 456,
                    },
                    {
                        "type": "value_error",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: An email address must have an @-sign.",
                        "input": "lol",
                        "ctx": {"reason": "An email address must have an @-sign."},
                    },
                ]
            },
        ),
        (
            {"name": "123", "surname": "456", "email": "lol", "password": "string"},
            422,
            {"detail": "Name should contains only letters"},
        ),
        (
            {"name": "Nikolai", "surname": 456, "email": "lol", "password": "string"},
            422,
            {
                "detail": [
                    {
                        "type": "string_type",
                        "loc": ["body", "surname"],
                        "msg": "Input should be a valid string",
                        "input": 456,
                    },
                    {
                        "type": "value_error",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: An email address must have an @-sign.",
                        "input": "lol",
                        "ctx": {"reason": "An email address must have an @-sign."},
                    },
                ]
            },
        ),
        (
            {"name": "Nikolai", "surname": "456", "email": "lol", "password": "string"},
            422,
            {"detail": "Surname should contains only letters"},
        ),
        (
            {
                "name": "Nikolai",
                "surname": "Sviridov",
                "email": "lol",
                "password": "string",
            },
            422,
            {
                "detail": [
                    {
                        "type": "value_error",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: An email address must have an @-sign.",
                        "input": "lol",
                        "ctx": {"reason": "An email address must have an @-sign."},
                    }
                ]
            },
        ),
        (
            {
                "name": "Nikolai",
                "surname": "",
                "email": "lol@kek.com",
                "password": "string",
            },
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
            {
                "name": "",
                "surname": "Sviridov",
                "email": "lol@kek.com",
                "password": "string",
            },
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
        (
            {
                "name": "name",
                "surname": "Sviridov",
                "email": "lol@kek.com",
                "password": "",
            },
            422,
            {
                "detail": [
                    {
                        "type": "string_too_short",
                        "loc": ["body", "password"],
                        "msg": "String should have at least 1 character",
                        "input": "",
                        "ctx": {"min_length": 1},
                    }
                ]
            },
        ),
    ],
)
async def test_create_user_validation_error(
    client, user_data_for_creation, expected_status_code, expected_detail
):
    resp = client.post("/user/", data=json.dumps(user_data_for_creation))
    data_from_resp = resp.json()
    assert resp.status_code == expected_status_code
    assert data_from_resp == expected_detail
