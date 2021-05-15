# Django
from django.shortcuts import render

# Third Party
from icecream import ic

# First Party
from donate.models import DontateSettings


def donate(request):
    settings = DontateSettings.get_solo()

    ic(settings.values_set)
    context = {
        "donate": settings,
        "values": settings.values_set.all(),
    }

    return render(request, "donate/donate.html", context)
