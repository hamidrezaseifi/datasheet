from meinprojekt.models_sqlalchemy import NAVIGATION_DATA_PROVIDER

all_nv_items = NAVIGATION_DATA_PROVIDER.get_all_items()

root_items = [i for i in all_nv_items if i["parent"] == 0]


def process_nav(item, all_items):
    children = [process_nav(i, all_items) for i in all_items if i["parent"] == item["id"]]
    nav_item = {"id": item["id"], "parent": item["parent"], "name": item["nav_name"],
                "start_page": item["start_page"] == 1, "last_parent": False,
                "url": item["url"], "children": children}

    if len(nav_item["children"]) > 0:
        lst = [i for i in nav_item["children"] if len(i["children"]) > 0]
        nav_item["last_parent"] = len(lst) > 0
    return nav_item


NAVIGATION_DATA = []
for i in root_items:
    NAVIGATION_DATA.append(process_nav(i, all_nv_items))
