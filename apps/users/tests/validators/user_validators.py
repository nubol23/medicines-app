from utils.tests.validation import BaseValidator


class ValidateMedicine(BaseValidator):
    @staticmethod
    def _perform_validation(testcase, user_obj, user_dict):
        testcase.assertEqual(user_obj.first_name, user_dict.pop("first_name"))
        testcase.assertEqual(user_obj.last_name, user_dict.pop("last_name"))
        testcase.assertEqual(user_obj.email, user_dict.pop("email"))
        testcase.assertEqual(user_obj.phone_number, user_dict.pop("phone_number"))
