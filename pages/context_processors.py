# First Party
from pages.models import Node


def get_nav_items(request):
    nodes = Node.objects.all()

    id = 0
    for nav_node in nodes:
        if nav_node.url == request.get_full_path():
            nav_node.nav_class = "active"
            id = nav_node.lft
            break

    for nav_node in nodes:
        if nav_node.lft < id and nav_node.rght > id:
            nav_node.nav_class = "active"

    return nodes


def get_breadcrumbs(request):
    full_path = request.get_full_path()

    if full_path == "/":
        return None

    for nav_node in Node.objects.all():
        if nav_node.url == full_path:
            return nav_node.get_ancestors(include_self=True)


def nav_items(request):
    return {
        "nav_items": get_nav_items(request),
        "breadcrumbs": get_breadcrumbs(request),
    }
