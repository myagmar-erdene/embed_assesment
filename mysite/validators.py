from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def __init__(self,
                 count_of_numbers=1,
                 count_of_lower_letters=1,
                 count_of_capital_letters=1,
                 count_of_symbols=1,
                 symbols="~`! @#$%^&*()_-+={[}]|\\:;\"'<,>.?/"):
        self.count_of_numbers = count_of_numbers
        self.count_of_lower_letters = count_of_lower_letters
        self.count_of_capital_letters = count_of_capital_letters
        self.count_of_symbols = count_of_symbols
        self.symbols = symbols

    def validate(self, password, user=None):
        numbers = [char for char in password if char.isnumeric()]
        lowers = [char for char in password if char.islower()]
        capitals = [char for char in password if char.isupper()]
        symbols = [char for char in password if char in self.symbols]

        if len(numbers) < self.count_of_numbers:
            raise ValidationError(
                _("This password must contain at least "
                  "%(min_length)d numbers."),
                code='password_too_short',
                params={'min_length': self.count_of_numbers},
            )

        if len(lowers) < self.count_of_lower_letters:
            raise ValidationError(
                _("This password must contain at least "
                  "%(min_length)d lower letters."),
                code='password_too_short',
                params={'min_length': self.count_of_lower_letters},
            )

        if len(capitals) < self.count_of_capital_letters:
            raise ValidationError(
                _("This password must contain at least "
                  "%(min_length)d capital letters."),
                code='password_too_short',
                params={'min_length': self.count_of_capital_letters},
            )

        if len(symbols) < self.count_of_symbols:
            raise ValidationError(
                _("This password must contain at least "
                  "%(min_length)d symbols."),
                code='password_too_short',
                params={'min_length': self.count_of_symbols},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least "
            "%(count_of_numbers)d numbers and "
            "%(count_of_lower_letters)d lower letters and "
            "%(count_of_capital_letters)d capital letters and "
            "%(count_of_symbols)d symbols."
            % {'count_of_numbers': self.count_of_numbers,
               'count_of_lower_letters': self.count_of_lower_letters,
               'count_of_capital_letters': self.count_of_capital_letters,
               'count_of_symbols': self.count_of_symbols}
        )
