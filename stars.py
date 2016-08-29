#!/usr/bin/env spack python
import os
import glob
import json
from datetime import datetime

from llnl.util.filesystem import mkdirp
from spack.util.executable import which
curl = which('curl')


def get_all_pages(url, headers=[], per_page=100):
    def get_page(url, i):
        url += '?page=%d' % i
        url += '&per_page=%d' % per_page

        args = []
        for header in headers:
            args += ['-H', header]
        args += [url]

        string = curl(*args, output=str)
        return json.loads(string)

    all_pages = []
    i = 1
    page = get_page(url, i)
    while page:
        all_pages.extend(page)
        i += 1
        page = get_page(url, i)

    return all_pages


def get_stars(*repos):
    def load_json(repo):
        cache_path = os.path.join('repos/%s.json' % repo)

        parent = os.path.dirname(cache_path)
        if not os.path.exists(parent):
            mkdirp(parent)

        if not os.path.exists(cache_path):
            json_data = get_all_pages(
                'https://api.github.com/repos/%s/stargazers' % repo,
                headers=['Accept: application/vnd.github.v3.star+json'])
            with open(cache_path, 'w') as f:
                f.write(json.dumps(json_data))
            return json_data
        else:
            with open(cache_path, 'r') as f:
                return json.load(f)

    jdata = reduce(lambda x,y:x+y, [load_json(r) for r in repos])

    users = set()
    unique_stars = []
    for js in jdata:
        username = js['user']['login']
        if username not in users:
            unique_stars.append(
                datetime.strptime(js['starred_at'], '%Y-%m-%dT%H:%M:%SZ'))
        users.add(username)

    return sorted(unique_stars)
