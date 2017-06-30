from django.contrib.sitemaps import Sitemap

from dogs.models import Dog
from pages.models import Page, ModuleList

class romSitemap(Sitemap):
    def location(self, obj):
        return obj.url
    

class AdoptionSitemap(romSitemap):
    changefreq = "daily"
    priority = 0.75

    def items(self):
        return Dog.objects.filter(dogStatus=Dog.STATUS_LOOKING)
    
    def lastmod(self, obj):
        return obj.modified


class SuccessSitemap(romSitemap):
    changefreq = "weekly"
    priority = .5

    def items(self):
        return Dog.objects.filter(dogStatus=Dog.STATUS_SUCCESS)

    def location(self, obj):
        return obj.succcess_url


class PageSitemap(romSitemap):
    changefreq = "monthly"
    priority = .5

    def items(self):
        return Page.objects.all()


class ModuleListSitemap(romSitemap):
    changefreq = "weekly"
    priority = .5

    def items(self):
        return ModuleList.objects.all()
    
    
sitemaps = {
    'pages': PageSitemap,
    'modulelist': ModuleListSitemap,
    'adoption': AdoptionSitemap,
    'success': SuccessSitemap
}
