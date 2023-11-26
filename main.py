import json
import time

import requests

with open('dump.json', 'r') as f:
    j = json.load(f)


def get_title(t):
    s = ""
    for i in t:
        s += i['plain_text']

    return s


all = dict()

# print(res)
for x in j:
    if x['object'] == 'page':
        if x['parent']['type'] == 'database_id':
            for p in x['properties'].values():
                if p['type'] == 'title':
                    title = get_title(p['title'])
                    break
        else:
            title = get_title(x['properties']['title']['title'])
    elif x['object'] == 'database':
        title = get_title(x['title'])
    else:
        print(x['object'])

    all[x['id']] = {'name': title, 'parent': x['parent'], 'object': x['object'], 'url': x['public_url']}

# print(json.dumps(all, indent=2))

with open('blocks.json', 'r') as f:
    blockparents = json.load(f)


def getparent(x):
    if x['parent']['type'] == 'page_id':
        return x['parent']['page_id']
    elif x['parent']['type'] == 'database_id':
        return x['parent']['database_id']
    elif x['parent']['type'] == 'block_id':
        blockid = x['parent']['block_id']
        while blockid in blockparents:
            blockid = blockparents[blockid]
            if blockid in all:
                break
        return blockid
    elif x['parent']['type'] == 'workspace':
        workspaces.append(i)


workspaces = []

for i, x in all.items():
    if x['parent']['type'] == 'block_id':
        blockid = x['parent']['block_id']
        while blockid in blockparents:
            blockid = blockparents[blockid]
            if blockid in all:
                break
        paren = all[blockid]
        x['parent'] = {'type': "{}_id".format(paren['object']), "{}_id".format(paren['object']): blockid}

for i, x in all.items():
    parent = getparent(x)

    if parent is not None:
        if 'children' not in all[parent]:
            all[parent]['children'] = []

        all[parent]['children'].append(i)

with open('all.json', 'w') as f:
    json.dump(all, f, indent=2, sort_keys=True)

private = set()

session = requests.Session()
for i, x in all.items():
    url = x['url']
    print("Querying {}".format(url))
    while True:
        res = session.head(url)
        if res.status_code == 429:
            print("Sleeping")
            time.sleep(float(res.headers['Retry-After']))
        elif res.status_code == 404:
            print("Private")
            private.add(i)
            break
        else:
            print("Public")
            break

# for p in private:
#     del all[p]


with open('public.json', 'w') as f:
    json.dump(all, f, indent=2, sort_keys=True)

tree = dict()


def rec(page, level, t):
    cur = t[page['name']] = dict()
    # print("{}{}".format("\t" * level, page['name']))
    if 'children' not in page:
        return

    for child in page['children']:
        rec(all[child], level + 1, cur)


for x in workspaces:
    rec(all[x], 0, tree)

with open('tree.json', 'w') as f:
    json.dump(tree, f, indent=2, sort_keys=True)
