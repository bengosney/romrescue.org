
# Third Party
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import text

# Locals
from .models import TeamMember


class TeamMemberTests(TestCase):
    @given(text())
    def test_name(self, name):
        team = TeamMember(name=name)

        self.assertEqual(str(team), name)
