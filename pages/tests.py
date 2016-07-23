from .admin import ContactAdmin
from .models import *

import mock

from django.test import TestCase
from django.core.files import File
from django.contrib.admin.sites import AdminSite


class PageMethodTests(TestCase):

    def test_nav_title_title(self):
        """
        Page nav title should return title
        """

        expected = 'just title'
        page = Page(title=expected)

        self.assertEqual(page.nav_title_actual, expected)

    def test_nav_title_nav(self):
        """
        Page nav title should return nav_title
        """

        expected = 'nav title'
        title = 'just title'
        page = Page(title=title, nav_title=expected)

        self.assertEqual(page.nav_title_actual, expected)
        self.assertNotEqual(page.nav_title_actual, title)

    def test_url(self):
        """
        Page url
        """

        expected = 'title'
        page = Page(title=expected)
        page.save()

        self.assertEqual(page.url, '/%s/' % expected)

    def test_unicode(self):
        """
        _unicode_
        """

        expected = 'title'
        page = Page(title=expected)

        self.assertEqual(unicode(page), expected)


class SocialMethodTests(TestCase):

    def test_url(self):
        expected = 'title'
        social = SocialLink(title=expected)
        social.save()

        self.assertEqual(social.url, '/%s/' % expected)


class EmptyNodeMethodTests(TestCase):

    def test_unicode(self):
        """
        _unicode_
        """

        expected = 'title'
        empty = Empty(title=expected)

        self.assertEqual(unicode(empty), '%s - Empty Node' % expected)

    def test_url(self):
        """
        Test the #URL
        """

        expected = 'bob'
        empty = Empty(title=expected)
        empty.save()

        self.assertEqual(empty.url, '#%s' % expected)


class SocialNodeMethodTests(TestCase):

    def test_unicode(self):
        """
        _unicode_
        """

        expected = 'bob'
        empty = SocialLink(social=expected)

        self.assertEqual(unicode(empty), expected)


class ContactSubmissionMethodTest(TestCase):

    def test_unicode(self):
        """
        _unicode_
        """

        expected = 'title'
        name = ContactSubmission(name=expected)

        self.assertEqual(unicode(name), expected)


class ContactAdmminMethodTest(TestCase):

    def setUp(self):
        self.site = AdminSite

    def test_permissions(self):
        """
        make sure permissions are correct
        """

        admin = ContactAdmin(ContactSubmission, self.site)

        self.assertFalse(admin.has_add_permission(None, None))
        self.assertFalse(admin.has_delete_permission(None, None))
