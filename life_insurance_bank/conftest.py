import pytest


@pytest.fixture
def customer_client(db):
    """A Django test client logged in as an customer user."""

    from django.test.client import Client

    return Client()


@pytest.fixture
def user_friend_dict():
    return {
        "id": "e9dfc203-5212-4567-9612-1213b012ea7d",
        "createdTimestamp": 1534437037513,
        "username": "05598444097",
        "enabled": True,
        "totp": False,
        "emailVerified": True,
        "firstName": "Jânio",
        "lastName": "Silva",
        "email": "teste@teste.com",
        "attributes": {
            "birthday": [
                "18/08/1977"
            ],
            "phone": [
                "48999153481"
            ]
        },
        "disableableCredentialTypes": [
            "password"
        ],
        "requiredActions": [],
        "notBefore": 0,
        "access": {
            "manageGroupMembership": True,
            "view": True,
            "mapRoles": True,
            "impersonate": True,
            "manage": True
        }
    }


@pytest.fixture
def list_earnings_dict():
    return {
        "offset": 0,
        "limit": 50,
        "count": 1,
        "results": [
            {
                "id": "6244ced8-ece4-425a-99de-93000501f4bb",
                "created": "2019-03-26T11:02:59.278974-03:00",
                "modified": "2019-03-26T11:02:59.278985-03:00",
                "code": "103",
                "title": "Convite de amigos",
                "amount": "100.00",
                "description": "A cada novo amigo que você convidar e for ativado, você receberá 100 NIX Coins. ( "
                               "Limite máximo de 5 amigos ativados)",
                "enabled": "true",
                "conversion_rate_enabled": "false",
                "client": "20f445a4-4636-49df-a7ed-7d387e2731eb"
            }
        ]
    }
