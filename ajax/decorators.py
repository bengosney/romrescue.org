
ajax_views = []


def ajax(cls):
    value = "%s.%s" % (cls.__module__, cls.__name__)
    ajax_views.append(value)

    return cls
