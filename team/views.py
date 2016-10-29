from vanilla import ListView
from .models import TeamMember
from pages.decorators import register_list_view


@register_list_view
class TeamList(ListView):
    model = TeamMember
    template_name = 'team/list.html'
