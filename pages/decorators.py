
form_registry = {}
list_view_registry = []

def register_form(cls):
    form_registry[cls.__name__] = cls()
    return cls

def register_list_view(Cls):
    list_view_registry.append((Cls.__name__, Cls.__name__))
            
    return Cls


def get_registered_list_views():
    return list_view_registry
