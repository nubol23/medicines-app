from utils.tests.validation import BaseValidator


class ValidateUser(BaseValidator):
    @staticmethod
    def _perform_validation(testcase, user_obj, user_dict):
        testcase.assertEqual(str(user_obj.id), user_dict.pop("id"))
        testcase.assertEqual(user_obj.first_name, user_dict.pop("first_name"))
        testcase.assertEqual(user_obj.last_name, user_dict.pop("last_name"))
        testcase.assertEqual(user_obj.email, user_dict.pop("email"))
        testcase.assertEqual(user_obj.phone_number, user_dict.pop("phone_number"))
