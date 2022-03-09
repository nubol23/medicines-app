class ValidateMedicine:
    @classmethod
    def validate(cls, testcase, medicine_obj, medicine_dict):
        testcase.assertIsInstance(medicine_dict, dict)

        testcase.assertEqual(medicine_obj.name, medicine_dict.pop("name"))
        testcase.assertEqual(medicine_obj.maker, medicine_dict.pop("maker"))
        testcase.assertEqual(medicine_obj.quantity, medicine_dict.pop("quantity"))
        testcase.assertEqual(medicine_obj.unit, medicine_dict.pop("unit"))

        testcase.assertFalse(medicine_dict)
