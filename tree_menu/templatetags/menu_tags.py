from django import template
from django.urls import resolve
from tree_menu.models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_tree': [], 'current_path': '', 'menu_name': menu_name}

    menu_items = list(MenuItem.objects.filter(menu=menu).select_related('parent').order_by('order'))

    request = context.get('request')
    current_path = request.path if request else ""

    items_by_id = {item.id: item for item in menu_items}
    children_map = {item.id: [] for item in menu_items}
    root_items = []

    for item in menu_items:
        if item.parent_id:
            children_map[item.parent_id].append(item)
        else:
            root_items.append(item)

    active_ids = set()
    def find_active_chain(items):
        for item in items:
            url = item.get_absolute_url()
            if url and url != '#' and current_path and current_path.rstrip('/') == url.rstrip('/'):
                return [item.id]
            subchain = find_active_chain(children_map[item.id])
            if subchain:
                return [item.id] + subchain
        return []
    active_chain = find_active_chain(root_items)
    active_ids = set(active_chain)

    def build_tree(items, level=0, parent_in_active_chain=False):
        tree = []
        for item in items:
            is_active = item.id in active_ids
            expand = is_active or (level == 1 and parent_in_active_chain)
            node = {
                'item': item,
                'children': build_tree(children_map[item.id], level+1, is_active),
                'expanded': expand,
                'active': (item.id == active_chain[-1] if active_chain else False),
                'in_active_chain': is_active,
                'level': level,
            }
            tree.append(node)
        return tree

    menu_tree = build_tree(root_items)
    return {
        'menu_tree': menu_tree,
        'current_path': current_path,
        'menu_name': menu_name,
    }