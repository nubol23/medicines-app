from utils.tests.validation import BaseValidator


class ValidateMedicine(BaseValidator):
    @staticmethod
    def _perform_validation(testcase, medicine_obj, medicine_dict):
        testcase.assertEqual(str(medicine_obj.id), medicine_dict.pop("id"))
        testcase.assertEqual(medicine_obj.name, medicine_dict.pop("name"))
        testcase.assertEqual(medicine_obj.maker, medicine_dict.pop("maker"))
        testcase.assertEqual(medicine_obj.quantity, medicine_dict.pop("quantity"))
        testcase.assertEqual(medicine_obj.unit, medicine_dict.pop("unit"))
