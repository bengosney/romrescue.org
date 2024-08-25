# Django
from django.apps import AppConfig

# Third Party
import wrapt


def test___lookup_wrapper(wrapped, instance, args, kwargs):
    try:
        return wrapped(*args, **kwargs)
    except Exception:
        pass


class PagesConfig(AppConfig):
    name = "pages"

    def ready(self) -> None:
        wrapt.patch_function_wrapper(
            "polymorphic.query",
            "PolymorphicQuerySet._process_aggregate_args.test___lookup",
            test___lookup_wrapper,
        )
        return super().ready()
