# Third Party
from vanilla import ListView

# First Party
from pages.decorators import register_list_view
from team.models import TeamMember


@register_list_view
class TeamList(ListView):
    model = TeamMember
    template_name = "team/list.html"
