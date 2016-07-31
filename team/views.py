from django.shortcuts import render
from vanilla import DetailView, ListView, CreateView
from .models import TeamMember


class TeamList(ListView):
    model = TeamMember
    template_name = 'team/list.html'
