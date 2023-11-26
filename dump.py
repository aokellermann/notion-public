import json
import os

from notion_client import Client
from notion_client.helpers import collect_paginated_api

notion = Client(auth=os.environ.get('NOTION_INTEGRATION_TOKEN'))

all_results = collect_paginated_api(
    notion.search
)

with open('dump.json', 'w') as f:
    json.dump(all_results, f, indent=2)
