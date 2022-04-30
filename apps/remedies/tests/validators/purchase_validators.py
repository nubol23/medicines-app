from apps.families.tests.validators import ValidateShortFamily
from apps.remedies.tests.validators.medicine_validators import ValidateMedicine
from apps.users.tests.validators import ValidateUser
from utils.tests.validation import BaseValidator, ValidateDateTime


class ValidatePurchase(BaseValidator):
    @staticmethod
    def _perform_validation(testcase, purchase_obj, purchase_dict):
        testcase.assertEqual(str(purchase_obj.id), purchase_dict.pop("id"))

        ValidateMedicine.validate(
            testcase, purchase_obj.medicine, purchase_dict.pop("medicine")
        )
        ValidateUser.validate(testcase, purchase_obj.user, purchase_dict.pop("user"))
        ValidateShortFamily.validate(
            testcase, purchase_obj.family, purchase_dict.pop("family")
        )

        ValidateDateTime.validate(
            testcase, purchase_obj.buy_date, purchase_dict.pop("buy_date")
        )
        ValidateDateTime.validate(
            testcase, purchase_obj.expiration_date, purchase_dict.pop("expiration_date")
        )
        testcase.assertEqual(purchase_obj.units, purchase_dict.pop("units"))
        testcase.assertEqual(purchase_obj.consumed, purchase_dict.pop("consumed"))
        testcase.assertEqual(purchase_obj.is_expired, purchase_dict.pop("is_expired"))
