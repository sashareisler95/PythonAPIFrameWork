from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        assert name in response_as_dict, f"Response JSON doesn't have key {name}"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, key):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        assert key in response_as_dict, f"Response JSON doesn't have key {key}"

    @staticmethod
    def assert_json_has_keys(response: Response, keys):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        for key in keys:
            assert key in response_as_dict, f"Response JSON doesn't have key {key}"

    @staticmethod
    def assert_status_code(response: Response, ex_status_code):
        assert response.status_code == ex_status_code, "Unexpected status code {response.status_code}"

    @staticmethod
    def assert_json_has_no_keys(response: Response, keys):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"
        for key in keys:
            assert key not in response_as_dict, f"Response JSON have key {key}"
