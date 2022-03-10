from utils.tests.validation import BaseValidator


class ValidateShortFamily(BaseValidator):
    @staticmethod
    def _perform_validation(testcase, family_obj, family_dict):
        testcase.assertEqual(family_obj.family_name, family_dict.pop("family_name"))
