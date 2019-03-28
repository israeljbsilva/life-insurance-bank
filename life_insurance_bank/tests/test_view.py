from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from django.conf import settings

import requests_mock
import json


invite_path = '/api/v1/invites'


def test_should_get_ping(client):
    # GIVEN

    # WHEN
    response = client.get('/ping')

    # THEN
    assert response.status_code == HTTP_200_OK


def test_should_get_user_code_not_exist(customer_client):
    # GIVEN

    # WHEN
    response = customer_client.get(f'{invite_path}/1')

    # THEN
    assert response.status_code == HTTP_200_OK


def test_should_get_user_code_exist(customer_client):
    # GIVEN
    data = {'social_security': '09487722980', 'code': '000000'}

    # WHEN
    customer_client.post(invite_path, data=json.dumps(data), content_type='application/json')
    response = customer_client.get(f'{invite_path}/09487722980')

    # THEN
    assert response.status_code == HTTP_200_OK
    assert response.data == {'code': '000000'}


def test_should_create_user(customer_client):
    # GIVEN
    data = {'social_security': '09487722980', 'code': '000000'}

    # WHEN
    response = customer_client.post(invite_path, data=json.dumps(data), content_type='application/json')

    # THEN
    assert response.status_code == HTTP_201_CREATED
    assert response.data == {'code': '000000', 'message': 'User createad.', 'user': '09487722980'}


def test_should_not_reached_friends_limit(customer_client):
    # GIVEN
    data = {'social_security': '09487722980', 'code': '000000'}

    # WHEN
    customer_client.post(invite_path, data=json.dumps(data), content_type='application/json')
    response = customer_client.post(invite_path, data=json.dumps(data), content_type='application/json')

    # THEN
    assert response.status_code == HTTP_200_OK
    assert response.data == {'message': 'User already exists!', 'code': '000000'}


def test_should_credit_points(customer_client, user_friend_dict, list_earnings_dict):
    cadun_url = settings.CADUN_URL
    nix_loyalty_program_url = settings.NIX_LOYALTY_PROGRAM_URL

    # GIVEN
    data = {'social_security': '09487722980', 'code': '000000'}

    # WHEN
    customer_client.post(invite_path, data=json.dumps(data), content_type='application/json')
    with requests_mock.Mocker() as m:
        m.get(f'{cadun_url}/users/05598444097/', text=json.dumps(user_friend_dict))
        m.get(f'{nix_loyalty_program_url}/clients/20f445a4-4636-49df-a7ed-7d387e2731eb/earnings?code=103',
              text=json.dumps(list_earnings_dict))
        m.post(f'{nix_loyalty_program_url}/clients/20f445a4-4636-49df-a7ed-7d387e2731eb/credits',
               text=json.dumps({'amount': '100.00'}))

        response = customer_client.put(
            f'{invite_path}/05598444097', data=json.dumps(data), content_type='application/json')

        assert response.status_code == HTTP_200_OK
        assert response.data == 'Points Credited'


def test_should_not_credit_points_user_does_not_exist(customer_client, user_friend_dict, ):
    # GIVEN
    data = {'social_security': '09487722980', 'code': '000000'}

    # WHEN
    customer_client.post(invite_path, data=json.dumps(data), content_type='application/json')

    response = customer_client.put(
        f'{invite_path}/05598444097', data=json.dumps(data), content_type='application/json')

    # THEN
    assert response.status_code == HTTP_200_OK
    assert response.data == {'message': 'User not registered', 'data': '05598444097'}
