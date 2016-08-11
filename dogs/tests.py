import datetime
import string

from django.test import TestCase
from django.core.files import File
from .models import *

from django.core.urlresolvers import reverse, reverse_lazy

from hypothesis.extra.django.models import models
from hypothesis.extra.django.models import add_default_field_mapping
from hypothesis.strategies import text, just, one_of
from hypothesis.extra.datetime import datetimes
from hypothesis import given

from ckeditor_uploader.fields import RichTextUploadingField as RichTextField
from django_extensions.db import fields

import mock

add_default_field_mapping(RichTextField, text())
add_default_field_mapping(fields.AutoSlugField, text())
add_default_field_mapping(fields.CreationDateTimeField, datetimes())
add_default_field_mapping(fields.ModificationDateTimeField, datetimes())


class DogTests(TestCase):
    STATUS_TITLE = "test status"

    @staticmethod
    def get_dog(name, dob="2015-01-01"):
        test_status = Status(title="test status", body="test body")
        test_status.save()

        return Dog(
            name=name, 
            dob=dob,
            gender=Dog.GENDERS[1][0],
            size=Dog.SIZES[1][0],
            location=test_status,
            description="body text",
            status=Dog.STATUS_LOOKING
        )

    @given(text())
    def test_name(self, name):
        dog = self.get_dog(name)

        self.assertEqual(unicode(dog), name)

    def test_age_one_month(self):
        one_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)

        dog = self.get_dog('rover', one_month)
        self.assertEqual(dog.age, '1 month')

    def test_age_two_months(self):
        one_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
        two_months = one_month.replace(day=1) - datetime.timedelta(days=1)

        dog = self.get_dog('rover', two_months)
        self.assertEqual(dog.age, '2 months')

    def test_age_one_year(self):
        one_year = datetime.date.today() - datetime.timedelta(days=366)

        dog = self.get_dog('rover', one_year)
        self.assertEqual(dog.age, '1 year')

    def test_age_two_years(self):
        two_years = datetime.date.today() - datetime.timedelta(days=731)

        dog = self.get_dog('rover', two_years)
        self.assertEqual(dog.age, '2 years')


    def test_age_invalid(self):
        dog = self.get_dog('rover', 'invalid')

        self.assertEqual(dog.age, None)

    def test_age_year_only(self):
        two_years = datetime.date.today() - datetime.timedelta(days=731)
        dog = self.get_dog('rover', two_years.year)

        self.assertEqual(dog.age, '2 years')

class DogPhotoTests(TestCase):
    def setUp(self):
        self.dog = DogTests.get_dog('rover')
        self.dog.save()


    def skip_test_photo_name(self):
        filename = 'dog-photo'
        file_mock = mock.MagicMock(spec=File, name=filename)
        file_mock.name = "%s.jpg" % filename

        dog_photo = DogPhoto(image=file_mock, dog=self.dog)

        self.assertEqual(unicode(dog_photo), file_mock.name)


class KeyPointsTests(TestCase):
    @given(models(KeyPoints))
    def test_keypoint_title(self, point):
        self.assertEqual(unicode(point), point.title)


class StatusTests(TestCase):
    @given(models(Status))
    def test_status_title(self, status):
        self.assertEqual(unicode(status), status.title)

