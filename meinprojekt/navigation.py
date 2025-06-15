from meinprojekt.models_sqlalchemy import NAVIGATION_DATA_PROVIDER

all_nv_items = NAVIGATION_DATA_PROVIDER.get_all_items()

root_items = [i for i in all_nv_items if i["parent"] == 0]


def process_nav(item, all_items):
    children = [process_nav(i, all_items) for i in all_items if i["parent"] == item["id"]]
    return {"id": item["id"], "parent": item["parent"], "name": item["nav_name"], "url": item["url"],
            "children": children}


NAVIGATION_DATA = []
for i in root_items:
    NAVIGATION_DATA.append(process_nav(i, all_nv_items))
