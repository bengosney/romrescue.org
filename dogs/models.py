from __future__ import unicode_literals

from bs4 import BeautifulSoup

import os

from datetime import date
try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

from django.db import models
from django_extensions.db import fields
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from image_cropping import ImageRatioField
from ckeditor_uploader.fields import RichTextUploadingField as RichTextField

from icons.icons import ICON_CHOICE

from modulestatus.models import statusMixin

class Filter(models.Model):    
    name = models.CharField(_("Name"), max_length=30)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)
    slug = fields.AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name
    
    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Filter')
        verbose_name_plural = _('Filters')


class KeyPoints(statusMixin, models.Model):
    title = models.CharField(_("Title"), max_length=150)
    details = models.CharField(_("Details"), max_length=400)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)
    icon = models.CharField(_("Icon"), max_length=120, blank=True, choices=ICON_CHOICE)

    def __str__(self):
        return self.title

    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Key Point')
        verbose_name_plural = _('Key Points')


class Status(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    show_arrival_date = models.BooleanField(_("Show arrival date"), default=False)
    body = RichTextField(_("Body"), blank=True, null=True)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title

    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Status/Location')
        verbose_name_plural = _('Status/Locations')



class Rescue(models.Model):
    name = models.CharField(_("Name"), max_length=30)
    logo = models.ImageField(_("Logo"), upload_to='uploads/rescue')
    website = models.URLField(_("Website"))

    logo_big = ImageSpecField(source='logo',
                              processors=[ResizeToFit(350, 150)],
                              format='PNG',
                              options={'quality': 70})

    logo_small = ImageSpecField(source='logo',
                                processors=[ResizeToFit(100, 75)],
                                format='PNG',
                                options={'quality': 70})


    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name = _('Rescue')
        verbose_name_plural = _('Rescues')

        
class Dog(statusMixin, models.Model):
    DEFAULT_COST = 265
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

    name = models.CharField(_("Name"), max_length=30)
    dob = models.DateField(_("DOB"), blank=True, null=True)
    gender = models.CharField(_("Gender"), max_length=6, choices=GENDERS)
    size = models.CharField(_("Size"), max_length=15, choices=SIZES)
    location = models.ForeignKey(Status, on_delete=models.PROTECT)
    arrival = models.DateField(_("Arrival Date"), blank=True, null=True)
    description = RichTextField(_("Body"))
    dogStatus = models.CharField(_("Status"),
        max_length=8,
        choices=STATUS,
        default=STATUS_LOOKING)

    keypoints = models.ManyToManyField(KeyPoints, blank=True)

    reserved = models.BooleanField(default=False)
    hold = models.BooleanField(_('Medical Hold'), default=False)
    promoted = models.BooleanField(_("Promoted on homepage"), default=False)

    neutered = models.BooleanField(_("Neutered"), default=True)
    standard_info = models.BooleanField(_("Standard Info"), default=True)
    cost = models.FloatField(_("Cost"), default=DEFAULT_COST)

    rescue = models.ForeignKey(Rescue, blank=True, null=True, on_delete=models.PROTECT)

    filters = models.ManyToManyField(Filter, blank=True)

    slug = fields.AutoSlugField(populate_from='name')
    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Dog')
        verbose_name_plural = _('Dogs')


    @property
    def is_success(self):
        return self.dogStatus == self.STATUS_SUCCESS

    @property
    def title(self):
        return self.name

    @property
    def url(self):
        return reverse_lazy('dogs:DogDetails', kwargs={'slug': self.slug})

    @property
    def succcess_url(self):
        return reverse_lazy('dogs:SuccessDetail', kwargs={'slug': self.slug})

    @property
    def correct_url(self):
        if self.is_success:
            return self.succcess_url
        else:
            return self.url

    @property
    def age(self):
        today = date.today()

        if isinstance(self.dob, (int)):
            self.dob = today.replace(self.dob)

        try:
            age = today.year - self.dob.year - \
                ((today.month, today.day) < (self.dob.month, self.dob.day))
        except:
            return None

        diff = 'year'
        plural = 's'

        if age == 0:
            age = today.month - self.dob.month

            if age < 0:
                age += 12
            
            diff = 'month'

        if age == 1:
            plural = ''

        return '%d %s%s' % (age, diff, plural)
    
    @property
    def all_filters(self):
        return ", ".join([f.name for f in self.filters.all()])

    @property
    def sheet_id(self):
        return "ID~%s" % self.id

    @property
    def raw_description(self):
        soup = BeautifulSoup(self.description)

        return "".join(soup.find('p').getText())
    
    @property
    def show_arrival_date(self):
        return (self.location.show_arrival_date and self.arrival and self.arrival > date.today())

    @property
    def homepageImage(self):
        return self.dogphoto_set.all().order_by('-promoted', 'position')[0]
    
    @property
    def homepageSubtitle(self):
        return "{} old {}".format(self.age.replace('s', ''), self.gender)
    
    @classmethod
    def get_homepage_dogs(cls):
        return cls.objects.filter(dogStatus=Dog.STATUS_LOOKING).exclude(reserved=True).order_by('-position')[:4]
    
    @classmethod
    def get_homepage_header_dogs(cls):
        return cls.objects.filter(dogStatus=Dog.STATUS_LOOKING).exclude(reserved=True).order_by('-promoted', 'created')[:4]
    

class DogPhoto(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.PROTECT)
    promoted = models.BooleanField(_("Promoted on homepage"), default=False)
    image = models.ImageField(upload_to='uploads/dogs')

    main = ImageSpecField(source='image',
                          processors=[ResizeToFit(600, 400)],
                          format='JPEG',
                          options={'quality': 70})

    thumbnail = ImageRatioField('image', '375x300')
    homepage = ImageRatioField('image', '1110x624')

    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return os.path.basename(self.image.url)

    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

        
class YoutubeVideo(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.PROTECT)
    url = models.CharField(_("Youtube url"), max_length=150)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def get_id(self):
        u_pars = urlparse(self.url)
        quer_v = parse_qs(u_pars.query).get('v')
        if quer_v:
            return quer_v[0]
        pth = u_pars.path.split('/')
        if pth:
            return pth[-1]

    def __str__(self):
        return self.get_id()

    class Meta(object):
        ordering = ('position',)
        verbose_name = _('Youtube Video')
        verbose_name_plural = _('Youtube Videos')
