# Django
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import get_template
from django.urls import reverse
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _

# Third Party
from ckeditor_uploader.fields import RichTextUploadingField as RichTextField
from django_extensions.db import fields
from image_cropping import ImageRatioField
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey

# First Party
from modulestatus.models import statusMixin
from pages.decorators import get_registered_list_views


class Node(PolymorphicMPTTModel, statusMixin):
    ICONS = [
        ("twitter", "Twitter"),
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
    ]

    parent = PolymorphicTreeForeignKey(
        "self",
        blank=True,
        null=True,
        related_name="children",
        verbose_name=_("parent"),
        on_delete=models.PROTECT,
    )
    title = models.CharField(_("Title"), max_length=200)
    nav_title = models.CharField(_("Navigation Title"), max_length=200, blank=True, default="")
    nav_icon = models.CharField(_("Navigation Icon"), choices=ICONS, max_length=200, blank=True, default="")
    nav_icon_only = models.BooleanField(_("Icon Only"), default=False)
    slug = fields.AutoSlugField(populate_from="title")
    title_tag = models.CharField(_("Title Tag"), max_length=200, blank=True, default="")
    meta_description = models.TextField(blank=True, default="")
    active_url_helper = models.CharField(max_length=255, blank=True, default="")
    is_home_page = models.BooleanField(default=False)

    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("Site node")
        verbose_name_plural = _("Site nodes")

    def __str__(self):
        return self.title

    @property
    def url(self):
        if self.is_home_page:
            return "/"

        try:
            url = reverse(f"pages:{self.__class__.__name__.lower()}", kwargs={"slug": self.slug})
        except BaseException:
            url = reverse("pages:page", kwargs={"slug": self.slug})

        return url

    @property
    def nav_title_actual(self):
        return self.nav_title or self.title

    def save(self, *args, **kwargs):
        if self.is_home_page:
            try:
                temp = Node.objects.get(is_home_page=True)
                if self != temp:
                    temp.is_home_page = False
                    temp.save()
            except Node.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    @staticmethod
    def get_nav_tree():
        pass


class Empty(Node):
    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("Empty Item")
        verbose_name_plural = _("Empty Items")

    def __str__(self):
        return f"{self.title} - Empty Node"

    @property
    def url(self):
        return f"#{self.slug}"


class ExternalLink(Node):
    URL = models.URLField(_("URL"))

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("External Link")
        verbose_name_plural = _("External Links")

    @property
    def url(self):
        return self.URL


class SocialLink(Node):
    TYPES = [
        ("twitter", "Twitter"),
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
    ]

    social = models.CharField(_("Social Type"), choices=TYPES, max_length=200)

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("Social Link")
        verbose_name_plural = _("Social Links")

    def __str__(self):
        return self.social


class Page(Node):
    FORM_CHOICES = (
        ("ContactForm", "Contact Form"),
        ("FosteringForm", "Fostering Form"),
    )

    body = RichTextField(_("Body"))
    form = models.CharField(max_length=100, blank=True, default="", choices=FORM_CHOICES)
    success_message = RichTextField(_("Success Message"), blank=True, null=True)

    def get_form_class(self):
        # First Party
        from pages import forms

        return getattr(forms, self.form)

    @property
    def success_url(self):
        return reverse("pages:page_success", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")


class ModuleList(Node):
    module = models.CharField(
        _("Module"),
        max_length=200,
    )

    body = RichTextField(_("Body"), null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field("module").choices = lazy(get_registered_list_views, list)()

    class Meta:
        verbose_name = _("Module List")
        verbose_name_plural = _("Module Lists")


class ContactSubmission(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=100, blank=True, default="")
    enquiry = models.TextField(_("Enquiry"))
    consent = models.BooleanField(
        _(
            "I give consent for data I enter into this form to be stored and "
            "processed by SOS Romanian Rescue South West and I am over 18"
        )
    )

    created = fields.CreationDateTimeField()

    def __str__(self):
        return self.name

    def send_email(self):
        template = get_template("pages/email-submission.html")
        context = {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "enquiry": self.enquiry,
        }
        content = template.render(context)

        email = EmailMessage(
            "New contact form submission",
            content,
            "info@romrescue.org",
            ["info@romrescue.org"],
            headers={"Reply-To": self.email},
        )

        email.send()


class HomePageHeader(models.Model):
    image = models.ImageField(upload_to="images")
    cropped = ImageRatioField("image", "1110x624")
    strapline = models.CharField(_("Strap Line"), max_length=200)
    subline = models.CharField(_("Sub Line"), max_length=400)
    itemlink = models.ForeignKey(Node, null=True, blank=True, on_delete=models.PROTECT)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ("position",)

    def __str__(self):
        return self.strapline

    def admin_image(self):
        return f'<img src="{self.image.url}" height="75"/>'

    admin_image.allow_tags = True


class FosteringSubmission(models.Model):
    name = models.CharField(_("Full Name"), max_length=150)
    email = models.EmailField(_("Email"), blank=True)
    contact_number = models.CharField(_("Contact Number"), max_length=20, blank=True)

    created = fields.CreationDateTimeField()

    def __str__(self):
        return self.name


class IntrestSubmission(models.Model):
    name = models.CharField(_("Full Name"), max_length=150)
    email = models.EmailField(_("Email"), blank=True)
    contact_number = models.CharField(_("Contact Number"), max_length=20, blank=True)

    adopting = models.BooleanField(_("Adopting"), default=True)
    fostering = models.BooleanField(_("Fostering"), default=False)
    other = models.BooleanField(_("Other"), default=False)

    created = fields.CreationDateTimeField()
    slug = fields.AutoSlugField(populate_from="name")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("pages:intrest_success", kwargs={"slug": self.slug})

    @property
    def url(self):
        return self.get_absolute_url()
