from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.functional import lazy

from django_extensions.db import fields

from ckeditor_uploader.fields import RichTextUploadingField as RichTextField
from polymorphic_tree.models import PolymorphicMPTTModel
from polymorphic_tree.models import PolymorphicTreeForeignKey

from image_cropping import ImageRatioField

from .decorators import get_registered_list_views

from modulestatus.models import statusMixin


class node(PolymorphicMPTTModel, statusMixin):
    ICONS = [
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
    ]

    parent = PolymorphicTreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='children',
        verbose_name=_('parent')
    )

    title = models.CharField(
        _("Title"),
        max_length=200
    )

    nav_title = models.CharField(
        _("Navigation Title"),
        max_length=200,
        blank=True,
        null=True
    )

    nav_icon = models.CharField(
        _("Navigation Icon"),
        choices=ICONS,
        max_length=200,
        blank=True,
        null=True
    )

    nav_icon_only = models.BooleanField(
        _("Icon Only"),
        default=False
    )

    slug = fields.AutoSlugField(
        populate_from='title'
    )

    title_tag = models.CharField(
        _("Title Tag"),
        max_length=200,
        null=True,
        blank=True
    )

    meta_description = models.TextField(
        null=True,
        blank=True
    )

    active_url_helper = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    is_home_page = models.BooleanField(default=False)

    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("Site node")
        verbose_name_plural = _("Site nodes")

    def __unicode__(self):
        return self.title

    @property
    def url(self):
        if self.is_home_page:
            return '/'

        try:
            url = reverse(
                'pages:%s' %
                self.__class__.__name__.lower(),
                kwargs={
                    'slug': self.slug})
        except:
            url = reverse('pages:page', kwargs={'slug': self.slug})

        return url

    @property
    def nav_title_actual(self):
        if self.nav_title:
            return self.nav_title
        else:
            return self.title

    def save(self, *args, **kwargs):
        if self.is_home_page:
            try:
                temp = node.objects.get(is_home_page=True)
                if self != temp:
                    temp.is_home_page = False
                    temp.save()
            except node.DoesNotExist:
                pass
        super(node, self).save(*args, **kwargs)

    @staticmethod
    def get_nav_tree():
        pass


class Empty(node):

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("Empty Item")
        verbose_name_plural = _("Empty Items")

    def __unicode__(self):
        return '%s - Empty Node' % self.title

    @property
    def url(self):
        return '#%s' % self.slug


class ExternalLink(node):
    URL = models.URLField(_("URL"))

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("External Link")
        verbose_name_plural = _("External Links")

    @property
    def url(self):
        return self.URL


class SocialLink(node):
    TYPES = [

        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
    ]

    social = models.CharField(_("Social Type"), choices=TYPES, max_length=200)

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("Social Link")
        verbose_name_plural = _("Social Links")

    def __unicode__(self):
        return self.social


class Page(node):
    FORM_CHOICES = (
        ('ContactForm', 'Contact Form'),
        ('FosteringForm', 'Fostering Form'),
    )

    body = RichTextField(_("Body"))
    form = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=FORM_CHOICES)
    success_message = RichTextField(
        _("Success Message"), blank=True, null=True)

    def getFormClass(self):
        from . import forms

        return getattr(forms, self.form)

    @property
    def success_url(self):
        return reverse('pages:page_success', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")


class ModuleList(node):
    module = models.CharField(
        _("Module"),
        max_length=200,
    )

    body = RichTextField(
        _("Body"),
        null=True,
        blank=True
    )

    def __init__(self, *args, **kwargs):
        super(ModuleList, self).__init__(*args, **kwargs)
        self._meta.get_field_by_name('module')[0].choices = lazy(
            get_registered_list_views, list)()
    

    class Meta:
        verbose_name = _("Module List")
        verbose_name_plural = _("Module Lists")


class ContactSubmission(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=100, blank=True, null=True)
    enquiry = models.TextField(_("Enquiry"))

    created = fields.CreationDateTimeField()

    def __unicode__(self):
        return self.name


class HomePageHeader(models.Model):
    image = models.ImageField(upload_to='images')
    cropped = ImageRatioField('image', '1110x624')
    strapline = models.CharField(_("Strap Line"), max_length=200)
    subline = models.CharField(_("Sub Line"), max_length=400)
    itemlink = models.ForeignKey(node, null=True, blank=True)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __unicode__(self):
        return self.strapline

    def admin_image(self):
        return '<img src="%s" height="75"/>' % self.image.url
    admin_image.allow_tags = True

    class Meta(object):
        ordering = ('position',)


class FosteringSubmission(models.Model):
    name = models.CharField(_("Full Name"), max_length=150)
    email = models.EmailField(_("Email"))
    contact_number = models.CharField(_("Contact Number"), max_length=20)

    created = fields.CreationDateTimeField()

    def __unicode__(self):
        return self.name
