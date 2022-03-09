from utils.tests.validation import BaseValidator


class ValidateMember(BaseValidator):
    @staticmethod
    def _perform_validation(testcase, obj, dict_entry):
        testcase.assertEqual(obj.user.first_name, dict_entry.pop("first_name"))
        testcase.assertEqual(obj.user.last_name, dict_entry.pop("last_name"))
        testcase.assertEqual(obj.user.phone_number, dict_entry.pop("phone_number"))
        testcase.assertEqual(obj.user.email, dict_entry.pop("email"))
