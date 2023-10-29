import time

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')
        email = register_data['email']
        first_name = register_data['firstName']
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

        # EDIT
        new_name = 'Changed_name'
        response = MyRequests.put(f"/user/{user_id}",
                                  data={'firstName': new_name},
                                  headers={'x-csrf-token': token},
                                  cookies={'auth_sid': auth_sid})
        Assertions.assert_status_code(response, 200)

        # GET USER DATA
        response = MyRequests.get(f"/user/{user_id}",
                                  headers={'x-csrf-token': token},
                                  cookies={'auth_sid': auth_sid})
        Assertions.assert_json_has_keys(response, ('username', 'email', 'firstName', 'lastName'))
        Assertions.assert_json_value_by_name(response, 'firstName', new_name,
                                             f"Wrong name of the user after changing name")

    def test_edit_user_not_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')
        user_id = self.get_json_value(response, 'id')

        # EDIT
        new_name = 'Changed_name'
        response = MyRequests.put(f"/user/{user_id}", data={'firstName': new_name})
        Assertions.assert_status_code(response, 400)
        assert response.content.decode('UTF8') == 'Auth token not supplied', 'Wrong text in response'

    def test_edit_from_another_user(self):
        # REGISTER FIRST USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')
        email1 = register_data['email']
        password1 = register_data['password']
        time.sleep(2)

        # REGISTER SECOND USER
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, 'id')
        user_2_id = self.get_json_value(response2, 'id')
        username = register_data['username']

        # LOGIN FIRST USER
        login_data = {
            'email': email1,
            'password': password1
        }
        response3 = MyRequests.post('/user/login', data=login_data)
        Assertions.assert_status_code(response3, 200)
        auth_sid = self.get_cookie(response3, 'auth_sid')
        token = self.get_header(response3, 'x-csrf-token')

        # EDIT SECOND USER
        new_name = 'Changed_name'
        response4 = MyRequests.put(f"/user/{user_2_id}",
                                   data={'username': new_name},
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})
        Assertions.assert_status_code(response4, 200)

        # GET USER DATA
        response5 = MyRequests.get(f"/user/{user_2_id}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})
        Assertions.assert_json_has_key(response5, 'username')
        Assertions.assert_json_has_no_keys(response2, ('email', 'firstName', 'lastName'))
        Assertions.assert_json_value_by_name(response5, 'username', username,
                                             f"Username changed when edited by another user")

    def test_edit_user_incorrect_email(self):
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

        # EDIT
        new_email = 'learninggmail.com'
        response = MyRequests.put(f"/user/{user_id}",
                                  data={'email': new_email},
                                  headers={'x-csrf-token': token},
                                  cookies={'auth_sid': auth_sid})
        Assertions.assert_status_code(response, 400)
        assert response.content.decode('UTF8') == 'Invalid email format', 'User email has been changed to incorrect'

    def test_edit_user_with_short_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')
        email = register_data['email']
        first_name = register_data['firstName']
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

        # EDIT
        new_name = 'C'
        response = MyRequests.put(f"/user/{user_id}",
                                  data={'firstName': new_name},
                                  headers={'x-csrf-token': token},
                                  cookies={'auth_sid': auth_sid})
        a = response.content.decode('UTF8')
        Assertions.assert_status_code(response, 400)
        assert response.text == '{"error":"Too short value for field firstName"}', 'The username can be changed to a very short one'
