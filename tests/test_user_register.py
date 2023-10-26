import random
import string

import pytest
import requests

from lib.base_case import BaseCase

data_list = [
        {'password': None, 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
        {'password': '123', 'username': None, 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
        {'password': '123', 'username': 'learnqa', 'firstName': None, 'lastName': 'learnqa', 'email': 'vinkotov@example.com'},
        {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': None, 'email': 'vinkotov@example.com'},
        {'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': None}
        ]
letters = string.ascii_lowercase
names = (''.join(random.choice(letters) for i in range(251)), ''.join(random.choice(letters) for i in range(1)))


class TestUserRegister(BaseCase):
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
                }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data, verify=False)
        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode(
            'UTF8') == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('data', data_list)
    def test_creating_a_user_with_an_empty_parameter(self, data):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data, verify=False)
        for key in data.keys():
            if data.get(key) == None:
                parameter = key
        assert response.status_code == 400, f"Incorrect response status code {response.status_code}"
        assert response.content.decode('UTF8') == f"The following required params are missed: {parameter}"

    @pytest.mark.parametrize('name', names)
    def test_create_user_with_short_or_long_name(self, name):
        data = {
            'password': '123',
            'username': name,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'testing@gmail.com'
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data, verify=False)
        assert response.status_code == 400, f"Incorrect response status code {response.status_code}"
        if len(name) > 1:
            assert response.content.decode('UTF8') == f"The value of 'username' field is too long", f"No limit on name length. Lenght - {len(name)}"
        else:
            assert response.content.decode(
                'UTF8') == f"The value of 'username' field is too short", f"No limit on name length. Length - {len(name)}"




