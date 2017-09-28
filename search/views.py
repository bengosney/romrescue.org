# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from dogs.models import Dog
from pages.models import Page

def results(request, term):
    query = SearchQuery(term)

    dog_vector = SearchVector('name', 'description')
    dogs = Dog.objects.annotate(rank=SearchRank(dog_vector,query), search=dog_vector).filter(search=query, dogStatus=Dog.STATUS_LOOKING).order_by('-rank')

    page_vector = SearchVector('title', 'body')
    pages = Page.objects.annotate(rank=SearchRank(page_vector,query), search=page_vector).filter(search=query).order_by('-rank')

    results = list(dogs) + list(pages)
    
    return render(request, "search/results.html", { 'term': term, 'results': results })
