# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Third Party
from ckeditor_uploader.fields import RichTextUploadingField as RichTextField
from django_extensions.db import fields
from solo.models import SingletonModel


class DontateSettings(SingletonModel):
    title = models.CharField(_("Title"), max_length=255, default="Donate to SOS Romanian Rescues South West")
    body = RichTextField(_("Body"))

    button_text = models.CharField(_("Button Text"), max_length=255, default="Donate to SOS Romanian Rescue")

    modified = fields.ModificationDateTimeField()

    def __str__(self):
        return "Donation Configuration"

    class Meta:
        verbose_name = "Donation Configuration"


class Values(models.Model):
    amount = models.IntegerField(_("Amount"))
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    dontate_settings = models.ForeignKey(DontateSettings, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"£{self.amount}"

    class Meta:
        ordering = ("position",)
