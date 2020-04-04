# Standard Library
import datetime

# Django
from django.db import transaction
from django.test import Client
from django.urls import reverse

# Third Party
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import text

# Locals
from .models import Dog, KeyPoints, Status


class DogTests(TestCase):
    STATUS_TITLE = "test status"

    @staticmethod
    def get_dog(name, dob="2015-01-01", arrival="2025-01-01", status_arrival=False):
        test_status = Status(title="test status", body="test body", show_arrival_date=status_arrival)
        test_status.save()

        return Dog(
            name=name,
            dob=dob,
            arrival=arrival,
            gender=Dog.GENDERS[1][0],
            size=Dog.SIZES[1][0],
            location=test_status,
            description="body text",
            dogStatus=Dog.STATUS_LOOKING
        )

    @given(text())
    def test_name(self, name):
        dog = self.get_dog(name)

        self.assertEqual(str(dog), name)

    @given(text())
    def test_title(self, name):
        dog = self.get_dog(name)

        self.assertEqual(dog.title, name)

    def test_url(self):
        dog = self.get_dog('rover')
        with transaction.atomic():
            dog.save()
        url = reverse('dogs:DogDetails', kwargs={'slug': dog.slug})

        self.assertEqual(dog.url, url)

    def test_succcess_url(self):
        dog = self.get_dog('rover')
        with transaction.atomic():
            dog.save()
        url = reverse('dogs:SuccessDetail', kwargs={'slug': dog.slug})

        self.assertEqual(dog.succcess_url, url)

    def test_month_negative_age(self):
        first_of_month = datetime.date.today().replace(day=28)
        one_month = first_of_month + datetime.timedelta(days=5)
        one_month = one_month - datetime.timedelta(days=366)

        dog = self.get_dog('rover', one_month)
        self.assertEqual(dog.age, '11 months')

    def test_age_one_month(self):
        first_of_month = datetime.date.today().replace(day=1)
        one_month = first_of_month - datetime.timedelta(days=1)

        dog = self.get_dog('rover', one_month)
        self.assertEqual(dog.age, '1 month')

    def test_age_two_months(self):
        first_of_month = datetime.date.today().replace(day=1)
        one_month = first_of_month - datetime.timedelta(days=1)

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

    def test_arrival_date_future_status_no(self):
        one_week = datetime.date.today() + datetime.timedelta(days=7)
        dog = self.get_dog('rover', arrival=one_week)

        self.assertEqual(dog.show_arrival_date, False)

    def test_arrival_date_past_status_no(self):
        one_week = datetime.date.today() - datetime.timedelta(days=7)
        dog = self.get_dog('rover', arrival=one_week)

        self.assertEqual(dog.show_arrival_date, False)

    def test_arrival_date_future_status_yes(self):
        one_week = datetime.date.today() + datetime.timedelta(days=7)
        dog = self.get_dog('rover', arrival=one_week, status_arrival=True)

        self.assertEqual(dog.show_arrival_date, True)

    def test_arrival_date_past_status_yes(self):
        one_week = datetime.date.today() - datetime.timedelta(days=7)
        dog = self.get_dog('rover', arrival=one_week, status_arrival=True)

        self.assertEqual(dog.show_arrival_date, False)

    def test_promoted_get_only4(self):
        for i in range(1, 5):
            dog = self.get_dog('rover{}'.format(i))
            dog.save()

        promoted = Dog.get_homepage_header_dogs()

        self.assertEqual(len(promoted), 4)

    def test_promoted_get_only_looking(self):
        for i in range(1, 4):
            dog = self.get_dog('rover{}'.format(i))
            if i == 1:
                dog.dogStatus = Dog.STATUS_FOUND

            if i == 2:
                dog.dogStatus = Dog.STATUS_SUCCESS

            dog.save()

        promoted = Dog.get_homepage_header_dogs()

        for dog in promoted:
            self.assertEqual(dog.dogStatus, Dog.STATUS_LOOKING)

    def test_promoted_get_no_hold(self):
        for i in range(1, 4):
            dog = self.get_dog('rover{}'.format(i))
            dog.hold = (i == 2)
            dog.save()

        promoted = Dog.get_homepage_header_dogs()

        for dog in promoted:
            self.assertEqual(dog.hold, False)

    def test_promoted_get_oldest_first(self):
        for i in range(1, 5):
            dog = self.get_dog('rover{}'.format(i))
            dog.save()

        promoted = Dog.get_homepage_header_dogs()

        i = 0
        for dog in promoted:
            i += 1
            self.assertEqual(str(dog), 'rover{}'.format(i))

    def test_promoted_get_promoted_first(self):
        for i in range(1, 5):
            dog = self.get_dog('rover{}'.format(i))
            if i == 4:
                dog.promoted = True
            dog.save()

        promoted = Dog.get_homepage_header_dogs()
        order = [4, 1, 2, 3]

        for dog, i in zip(promoted, order):
            self.assertEqual(str(dog), 'rover{}'.format(i))

    def test_homepage_get_only4(self):
        for i in range(1, 5):
            dog = self.get_dog('rover{}'.format(i))
            dog.save()

        promoted = Dog.get_homepage_dogs()

        self.assertEqual(len(promoted), 4)

    def test_homepage_get_only_looking(self):
        for i in range(1, 4):
            dog = self.get_dog('rover{}'.format(i))
            if i == 1:
                dog.dogStatus = Dog.STATUS_FOUND

            if i == 2:
                dog.dogStatus = Dog.STATUS_SUCCESS

            dog.save()

        promoted = Dog.get_homepage_dogs()

        for dog in promoted:
            self.assertEqual(dog.dogStatus, Dog.STATUS_LOOKING)

    def test_homepage_get_no_hold(self):
        for i in range(1, 4):
            dog = self.get_dog('rover{}'.format(i))
            dog.hold = (i == 2)
            dog.save()

        promoted = Dog.get_homepage_dogs()

        for dog in promoted:
            self.assertEqual(dog.hold, False)

    def test_homepage_get_oldest_first(self):
        for i in range(1, 5):
            dog = self.get_dog('rover{}'.format(i))
            dog.save()

        promoted = Dog.get_homepage_dogs()

        i = 0
        for dog in promoted:
            i += 1
            self.assertEqual(str(dog), 'rover{}'.format(i))


class KeyPointsTests(TestCase):

    @given(text())
    def test_keypoint_title(self, title):
        point = KeyPoints(title=title)
        self.assertEqual(str(point), point.title)


class StatusTests(TestCase):

    @given(text())
    def test_status_title(self, title):
        status = Status(title=title)
        self.assertEqual(str(status), status.title)


class DetailViewTests(TestCase):
    def test_status_looking(self):
        dog = DogTests.get_dog('rover')
        dog.dogStatus = Dog.STATUS_LOOKING

        dog.save()

        client = Client()
        response = client.get(dog.url)

        self.assertEqual(response.status_code, 200)

    def test_status_found(self):
        dog = DogTests.get_dog('rover')
        dog.dogStatus = Dog.STATUS_FOUND

        dog.save()

        client = Client()
        response = client.get(dog.url)

        self.assertEqual(response.status_code, 410)
