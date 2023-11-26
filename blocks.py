import json
import os

from notion_client import Client


def find_parent(notion: Client, parents: dict, block: dict, initial: bool = True) -> None:
    block_id = block['id']
    if block['parent']['type'] == 'block_id':
        block_id = block['id']
        parent_id = block['parent']['block_id']
        parents[block_id] = parent_id
        print("Added {} -> {}".format(block_id, parent_id))

        parent = notion.blocks.retrieve(parent_id)
        find_parent(notion, parents, parent, False)
    elif not initial:
        if block['parent']['type'] == 'page_id':
            parents[block_id] = block['parent']['page_id']
            print("Added {} -> {}".format(block_id, block['parent']['page_id']))
        elif block['parent']['type'] == 'database_id':
            parents[block_id] = block['parent']['database_id']
            print("Added {} -> {}".format(block_id, block['parent']['database_id']))


def main():
    """
    Given a dump of notion page metadata, writes block parent data to `blocks.json`.
    """

    with open('dump.json', 'r') as f:
        j = json.load(f)

    notion = Client(auth=os.environ.get('NOTION_INTEGRATION_TOKEN'))

    parents = dict()

    for x in j:
        find_parent(notion, parents, x)

    with open('blocks.json', 'w') as f:
        json.dump(parents, f, indent=2)


if __name__ == '__main__':
    main()
