import re

form_registry = {}
list_view_registry = []


def register_form(cls):
    form_registry[cls.__name__] = cls()
    return cls


def register_list_view(cls):
    value = "%s.%s" % (cls.__module__, cls.__name__)
    name = " ".join(re.findall('[A-Z][^A-Z]*', cls.__name__))
    list_view_registry.append((value, name))

    return cls


def get_registered_list_views():
    return list_view_registry
