# Future

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third Party
from image_cropping import ImageRatioField


class TeamMember(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    job = models.CharField(_("Job"), max_length=150)
    info = models.TextField(_("Info"), max_length=1000)

    image = models.ImageField(upload_to="images/team", blank=True, default="")
    cropped = ImageRatioField("image", "400x400")

    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def admin_image(self):
        img = self.image.url if self.image else "http://placehold.it/75x75"
        return f'<img src="{img}" height="75"/>'

    admin_image.allow_tags = True

    class Meta:
        ordering = ("position",)
        verbose_name = _("Team Member")
        verbose_name_plural = _("Team Members")
