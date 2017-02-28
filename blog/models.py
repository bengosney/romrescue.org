from __future__ import unicode_literals

from django.db import models

from modulestatus.models import statusMixin

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django_extensions.db import fields
from ckeditor_uploader.fields import RichTextUploadingField as RichTextField

class Blog(statusMixin, models.Model):
    title = models.CharField(_('Title'), max_length=50)
    body = RichTextField(_("Body"), blank=True, null=True)
    slug = fields.AutoSlugField(populate_from='name')

    def __unicode__(self):
        return self.title

    class Meta(object):
        verbose_name = _('News Item')
        verbose_name_plural = _('News Items')

    @property
    def url(self):
        return reverse_lazy('blog:BlogDetails', kwargs={'slug': self.slug})
