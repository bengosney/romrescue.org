from __future__ import unicode_literals

import os
import importlib

from datetime import date

from django.db import models
from django_extensions.db import fields
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy

from imagekit.models import ImageSpecField
from imagekit.processors import *

from image_cropping import ImageRatioField

from ckeditor_uploader.fields import RichTextUploadingField as RichTextField

from icons.icons import ICON_CHOICE

class KeyPoints(models.Model):
    title = models.CharField(max_length=150)
    details = models.CharField(max_length=400)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)
    icon = models.CharField(max_length=120, blank=True, choices=ICON_CHOICE)

    def __unicode__(self):
        return self.title

    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Key Point')
        verbose_name_plural = _('Key Points')


class Status(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    body = RichTextField(_("Body"), blank=True)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __unicode__(self):
        return self.title

    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Status/Location')
        verbose_name_plural = _('Status/Locations')


class Dog(models.Model):
    GENDERS = [
        ('male', _('Male')),
        ('female', _('Female')),
    ]

    SIZES = [
        ('extra small', _('Extra Small')),
        ('small', _('Small')),
        ('medium', _('Medium')),
        ('large', _('Large')),
        ('extra large', _('Extra Large')),
    ]

    STATUS_LOOKING = 'looking'
    STATUS_FOUND = 'found'
    STATUS_SUCCESS = 'success'

    STATUS = [
        (STATUS_LOOKING, _('Looking for a home')),
        (STATUS_FOUND, _('Found a home')),
        (STATUS_SUCCESS, _('Success storie')),
    ]

    name = models.CharField(max_length=30)
    dob = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDERS)
    size = models.CharField(max_length=15, choices=SIZES)
    location = models.ForeignKey(Status)
    description = RichTextField(_("Body"))
    status = models.CharField(max_length=8, choices=STATUS, default=STATUS_LOOKING)

    keypoints = models.ManyToManyField(KeyPoints)

    slug = fields.AutoSlugField(populate_from='name')
    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()
    position = models.PositiveIntegerField(default=0, blank=False, null=False)


    def __unicode__(self):
       return self.name

    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Dog')
        verbose_name_plural = _('Dogs')


    @property
    def url(self):
        return reverse_lazy('dogs:DogDetails', kwargs={'slug':self.slug})

    @property
    def age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        diff = 'year'
        plural = 's'
        
        if age == 0:
            age = today.month - self.dob.month
            diff = 'month'

        if age == 1:
            plural = ''

        return '%d %s%s' % (age, diff, plural)


class DogPhoto(models.Model):
    dog = models.ForeignKey(Dog)
    image = models.ImageField(upload_to='uploads/dogs')

    main = ImageSpecField(source='image',
                          processors=[ResizeToFit(600, 400)],
                          format='JPEG',
                          options={'quality': 70})

    thumbnail = ImageRatioField('image', '375x300')


    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __unicode__(self):
        return os.path.basename(self.image.url)


    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
