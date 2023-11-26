import json
import time

import requests


def main():
    with open('all.json', 'r') as f:
        items = json.load(f)

    private = []

    session = requests.Session()
    for i, item in items.items():
        url = item['url']
        print("Querying {}".format(url))
        while True:
            res = session.head(url)
            if res.status_code == 429:
                print("Sleeping")
                time.sleep(float(res.headers['Retry-After']))
            elif res.status_code == 404:
                print("Private")
                private.append(i)
                break
            else:
                print("Public")
                break

    with open('private.json', 'w') as f:
        json.dump(private, f, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
