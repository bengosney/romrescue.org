# Django
from django.shortcuts import render

# First Party
from donate.models import DontateSettings


def donate(request):
    settings = DontateSettings.get_solo()

    context = {
        "donate": settings,
        "values": settings.values_set.all(),
    }

    return render(request, "donate/donate.html", context)
