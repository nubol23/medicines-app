from apps.families.models import FamilyInvitation, InvitationStatus
from utils.tests.validation import BaseValidator


class ValidateMember(BaseValidator):
    @staticmethod
    def _perform_validation(testcase, obj, dict_entry):
        def _get_status(obj):
            email = obj.user.email
            invitation = FamilyInvitation.objects.filter(email=email).first()
            if invitation and invitation.status == InvitationStatus.PENDING:
                return "pending"
            else:
                return ""

        testcase.assertEqual(_get_status(obj), dict_entry.pop("status"))
        testcase.assertEqual(obj.user.first_name, dict_entry.pop("first_name"))
        testcase.assertEqual(obj.user.last_name, dict_entry.pop("last_name"))
        testcase.assertEqual(obj.user.phone_number, dict_entry.pop("phone_number"))
        testcase.assertEqual(obj.user.email, dict_entry.pop("email"))
