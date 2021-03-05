# Django
from django import template

register = template.Library()


@register.filter
def possess(word):
    if word[-1] == "s":
        return f"{word}'"
    else:
        return f"{word}'s"
