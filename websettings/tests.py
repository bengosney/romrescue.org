# Standard Library
import string

# Third Party
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import text

# Locals
from .models import setting


def sane_text():
    return text(
        min_size=1,
        max_size=100,
        alphabet=string.printable
    )


class WebSettingsTests(TestCase):
    @given(name=sane_text())
    def test_new_setting(self, name):
        self.assertEqual(setting.getValue(name), "")

    @given(name=sane_text(), value=sane_text())
    def test_excisting_setting(self, name, value):
        name = name.replace('\x00', 'NUL')
        value = value.replace('\x00', 'NUL')
        s = setting(title=name, value=value)
        s.save()

        self.assertEqual(setting.getValue(name), value)

    @given(name=sane_text(), value=sane_text())
    def test_new_setting_with_default(self, name, value):
        self.assertEqual(setting.getValue(name, value), value)
