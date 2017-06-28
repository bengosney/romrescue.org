from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from django_extensions.db import fields
from ckeditor_uploader.fields import RichTextUploadingField as RichTextField

from modulestatus.models import statusMixin


class competition(statusMixin, models.Model):
    title = models.CharField(max_length=150)
    description = RichTextField(_("Body"), blank=True)

    slug = fields.AutoSlugField(populate_from='title')
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    @property
    def url(self):
        return reverse_lazy('photocomp:CompitionDetails', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.title

    class Meta(object):
        ordering = ('position',)
    
    

class category(statusMixin, models.Model):
    title = models.CharField(max_length=150)
    description = RichTextField(_("Body"), blank=True)
    competition = models.ForeignKey(competition)

    slug = fields.AutoSlugField(populate_from='title')
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    @property
    def url(self):
        return reverse_lazy('photocomp:CategoryDetails', kwargs={
            'slug': self.slug,
            'comp_slug': self.competition.slug,
        })

    @property
    def new_submission_url(self):
        return reverse_lazy('photocomp:CategorySubmission', kwargs={
            'slug': self.slug,
            'comp_slug': self.competition.slug,
        })

    
    @property    
    def full_title(self):
        return "%s - %s" % (self.competition.title, self.title)
    
    def __unicode__(self):
        return self.title

    class Meta(object):
        ordering = ('position',)
    

class user(statusMixin, models.Model):
    email = models.EmailField()

    def __unicode__(self):
        return self.email    

    
class submission(statusMixin, models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(category)
    user = models.ForeignKey(user)

    def __unicode__(self):
        return self.email    
