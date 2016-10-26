from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from image_cropping import ImageRatioField

class TeamMember(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    job = models.CharField(_("Job"), max_length=150)
    info = models.TextField(_("Info"), max_length=1000)

    image = models.ImageField(upload_to='images/team')
    cropped = ImageRatioField('image', '400x400')

    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __unicode__(self):
        return self.name

    def admin_image(self):
        return '<img src="%s" height="75"/>' % self.image.url
    admin_image.allow_tags = True

    class Meta(object):
        ordering = ('position',)
        verbose_name = _("Team Member")
        verbose_name_plural = _("Team Members")

        
