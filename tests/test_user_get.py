import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        user_id = '2'
        response = requests.get("https://playground.learnqa.ru/api/user/" + user_id, verify=False)
        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_no_keys(response, ('email', 'firstName', 'lastName'))

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data, verify=False)
        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth = self.get_json_value(response1, 'user_id')
        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_from_auth}",
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid},
                                 verify=False)
        Assertions.assert_json_has_keys(response2, ('username', 'email', 'firstName', 'lastName'))

    def test_getting_another_users_data(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data, verify=False)
        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        response2 = requests.get(f"https://playground.learnqa.ru/api/user/1",
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid},
                                 verify=False)
        Assertions.assert_json_has_key(response2, 'username')
        Assertions.assert_json_has_no_keys(response2, ('email', 'firstName', 'lastName'))



