import json
import os

from notion_client import Client

with open('dump.json', 'r') as f:
    j = json.load(f)

notion = Client(auth=os.environ.get('NOTION_INTEGRATION_TOKEN'))

parents = dict()


def rec(block, initial=True):
    id = block['id']
    if block['parent']['type'] == 'block_id':
        id = block['id']
        parentid = block['parent']['block_id']
        parents[id] = parentid
        print("Added {} -> {}".format(id, parentid))

        parent = notion.blocks.retrieve(parentid)
        rec(parent, False)
    elif not initial:
        if block['parent']['type'] == 'page_id':
            parents[id] = block['parent']['page_id']
            print("Added {} -> {}".format(id, block['parent']['page_id']))
        elif block['parent']['type'] == 'database_id':
            parents[id] = block['parent']['database_id']
            print("Added {} -> {}".format(id, block['parent']['database_id']))


for x in j:
    rec(x)

with open('blocks.json', 'w') as f:
    json.dump(parents, f, indent=2)
