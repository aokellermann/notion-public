# notion-public

Query notion to determine which pages are public and private.

Create a token here: https://www.notion.so/my-integrations.

Then, connect your top level pages with this integration (on each page,
click 3 dots in top right corner, click add connections, choose this integration).
Only top level pages need to be connected because their children will also be connected.

```console
# https://www.notion.so/my-integrations
export NOTION_INTEGRATION_TOKEN=XYZ

# install python packages
pip install -r requirements.txt

# find all notion items
python dump.py

# find parent items for blocks
python blocks.py

# build tree for all notion items
python all.py

# optional: manually determine whether notion items are public or private
python private.py

# build tree
python tree.py
```

## private.py

I have no idea why, but the first time I used `dump.py`,
every single item contained non-`null` `public_url`, so I thought that wouldn't
be usable as an indicator of publicity. Therefore, I wrote `private.py` which
will perform an HTTP HEAD on the URL and if it 404s, it is private. However,
now when I run `dump.py`, the private items have `public_url` of `null`!
`tree.py` is designed to handle both cases.