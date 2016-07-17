
form_registry = {}


def register_form(cls):
    form_registry[cls.__name__] = cls()
    return cls
