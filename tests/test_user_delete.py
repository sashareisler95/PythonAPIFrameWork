import time

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_delete_user_no_auth(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post('/user/login', data=data)
        Assertions.assert_status_code(response, 200)
        user_id = self.get_json_value(response, 'user_id')
        auth_sid = self.get_cookie(response, 'auth_sid')
        token = self.get_header(response, 'x-csrf-token')
        response = MyRequests.delete(f"/user/{user_id}", headers={'x-csrf-token': token},
                                     cookies={'auth_sid': auth_sid})
        Assertions.assert_status_code(response, 400)
        assert response.text == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', 'You can delete test users with ID 1, 2, 3, 4 or 5.'

    def test_delete_user_successfully(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')
        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response = MyRequests.post('/user/login', data=login_data)
        Assertions.assert_status_code(response, 200)
        auth_sid = self.get_cookie(response, 'auth_sid')
        token = self.get_header(response, 'x-csrf-token')

        # DELETE
        response = MyRequests.delete(f"/user/{user_id}", headers={'x-csrf-token': token},
                                     cookies={'auth_sid': auth_sid})
        Assertions.assert_status_code(response, 200)

        # GET USER DATA
        response = MyRequests.get(f"/user/{user_id}",
                                  headers={'x-csrf-token': token},
                                  cookies={'auth_sid': auth_sid})
        Assertions.assert_status_code(response, 404)
        assert response.text == 'User not found', 'The user was not deleted'

    def test_delete_user_by_another_user(self):
        # REGISTER USER 0
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')
        user_id_0 = self.get_json_value(response, 'id')
        time.sleep(2)

        # REGISTER USER 1
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')
        email = register_data['email']
        password = register_data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response = MyRequests.post('/user/login', data=login_data)
        Assertions.assert_status_code(response, 200)
        auth_sid = self.get_cookie(response, 'auth_sid')
        token = self.get_header(response, 'x-csrf-token')

        # DELETE
        response = MyRequests.delete(f"/user/{user_id_0}", headers={'x-csrf-token': token},
                                     cookies={'auth_sid': auth_sid})
        Assertions.assert_status_code(response, 200)
        # GET USER DATA
        response = MyRequests.get(f"/user/{user_id_0}",
                                  headers={'x-csrf-token': token},
                                  cookies={'auth_sid': auth_sid})
        Assertions.assert_status_code(response, 200)
        assert response.text == '{"username":"learnqa"}', 'You can remove a user from under another user'
