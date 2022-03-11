from apps.families.tests.validators import ValidateShortFamily
from apps.users.tests.validators import ValidateUser
from utils.tests.validation import BaseValidator


class ValidateFamilyInvitationCreation(BaseValidator):
    @staticmethod
    def _perform_validation(testcase, invitation_obj, invitation_dict):
        testcase.assertEqual(invitation_obj.email, invitation_dict.pop("email", None))
        testcase.assertEqual(
            invitation_obj.first_name, invitation_dict.pop("first_name", None)
        )
        testcase.assertEqual(
            invitation_obj.last_name, invitation_dict.pop("last_name", None)
        )
        testcase.assertEqual(
            invitation_obj.phone_number, invitation_dict.pop("phone_number", None)
        )

        ValidateShortFamily.validate(
            testcase, invitation_obj.family, invitation_dict.pop("family", None)
        )

        testcase.assertEqual(invitation_obj.status, invitation_dict.pop("status", None))

        ValidateUser.validate(
            testcase, invitation_obj.invited_by, invitation_dict.pop("invited_by", None)
        )


class ValidateFamilyInvitation(BaseValidator):
    @staticmethod
    def _perform_validation(testcase, invitation_obj, invitation_dict):
        testcase.assertEqual(str(invitation_obj.id), invitation_dict.pop("id", None))

        testcase.assertEqual(invitation_obj.email, invitation_dict.pop("email", None))
        testcase.assertEqual(
            invitation_obj.first_name, invitation_dict.pop("first_name", None)
        )
        testcase.assertEqual(
            invitation_obj.last_name, invitation_dict.pop("last_name", None)
        )
        testcase.assertEqual(
            invitation_obj.phone_number, invitation_dict.pop("phone_number", None)
        )

        ValidateShortFamily.validate(
            testcase, invitation_obj.family, invitation_dict.pop("family", None)
        )

        testcase.assertEqual(invitation_obj.status, invitation_dict.pop("status", None))

        ValidateUser.validate(
            testcase, invitation_obj.invited_by, invitation_dict.pop("invited_by", None)
        )
