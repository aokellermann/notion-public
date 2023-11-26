import json
import os


def dfs(item_id, item, tree, items, private):
    cur = {'name': item['name'], 'public': item['public_url'] is not None and item_id not in private, 'children': []}
    tree.append(cur)
    if 'children' not in item:
        return

    for child in item['children']:
        dfs(child, items[child], cur['children'], items, private)


def main():
    with open('all.json', 'r') as f:
        dump = json.load(f)
    with open('all.json', 'r') as f:
        items = json.load(f)

    if os.path.exists('private.json'):
        with open('private.json', 'r') as f:
            private = set(json.load(f))
    else:
        private = set()

    tree = []
    for item_id, item in dump.items():
        if item['parent']['type'] == "workspace":
            dfs(item_id, items[item_id], tree, items, private)

    with open('tree.json', 'w') as f:
        json.dump(tree, f, indent=2)


if __name__ == '__main__':
    main()
