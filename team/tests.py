from django.test import TestCase

from hypothesis.strategies import text
from hypothesis import given

from .models import TeamMember


class TeamMemberTests(TestCase):
    @given(text())
    def test_name(self, name):
        team = TeamMember(name=name)

        self.assertEqual(unicode(team), name)
