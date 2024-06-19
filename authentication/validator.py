from django.core.exceptions import ValidationError


class ContainsLetterValidator:

    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                "Password must contain one letter.",
                code='password_no_letters'
            )

    def get_help_text(self):
        return "Password must contain 1 maj and one min."
