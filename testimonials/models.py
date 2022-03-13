# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third Party
from django_extensions.db import fields

# First Party
from modulestatus.models import statusMixin


class Testimonial(statusMixin, models.Model):
    name = models.CharField(_("Name"), max_length=150)
    body = models.TextField(_("Body"))

    created = fields.CreationDateTimeField()
    modified = fields.ModificationDateTimeField()
    position = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ("position",)
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")

    def __str__(self) -> str:
        return self.name
