import json
import time

import requests


def make_title(title: list) -> str:
    return "".join([title_element['plain_text'] for title_element in title])


def get_title(item: dict) -> str:
    if item['object'] == 'page':
        if item['parent']['type'] == 'database_id':
            for p in item['properties'].values():
                if p['type'] == 'title':
                    return make_title(p['title'])
        else:
            return make_title(item['properties']['title']['title'])
    elif item['object'] == 'database':
        return make_title(item['title'])


def get_block_parent_id(block: dict, blocks: dict, items: dict) -> str:
    block_id = block['parent']['block_id']
    while block_id in blocks:
        block_id = blocks[block_id]
        if block_id in items:
            break
    return block_id


def get_parent_id(item: dict, blocks: dict, items: dict):
    if item['parent']['type'] == 'page_id':
        return item['parent']['page_id']
    elif item['parent']['type'] == 'database_id':
        return item['parent']['database_id']
    elif item['parent']['type'] == 'block_id':
        return get_block_parent_id(item, blocks, items)


def main():
    with open('dump.json', 'r') as f:
        all_results = json.load(f)
    with open('blocks.json', 'r') as f:
        blocks = json.load(f)

    items = {item['id']: {'name': get_title(item),
                          'parent': item['parent'],
                          'object': item['object'],
                          'url': item['url'],
                          'public_url': item.get('public_url')} for item in all_results}

    # replace block parents with page/database
    for item in items.values():
        if item['parent']['type'] == 'block_id':
            block_id = get_block_parent_id(item, blocks, items)
            parent_item = items[block_id]
            item['parent'] = {'type': "{}_id".format(parent_item['object']),
                              "{}_id".format(parent_item['object']): block_id}

    # link parent to children
    for item_id, item in items.items():
        parent = get_parent_id(item, blocks, items)

        if parent is not None:
            if 'children' not in items[parent]:
                items[parent]['children'] = []

            items[parent]['children'].append(item_id)

    with open('all.json', 'w') as f:
        json.dump(items, f, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
