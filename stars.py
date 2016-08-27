#!/usr/bin/env spack python
import os
import glob
import json
from datetime import datetime
from llnl.util.filesystem import mkdirp
from spack.util.executable import which
curl = which('curl')


def get_stars(*repos, **kwargs):
    per_page = kwargs.get('per_page', 100)

    def get(repo, i):
        url = 'https://api.github.com/repos/%s/stargazers' % repo
        url += '?page=%d' % i
        url += '&per_page=%d' % per_page
        string = curl(
            '-H', 'Accept: application/vnd.github.v3.star+json', url,
            output=str)

        return json.loads(string)

    def load_json(repo):
        cache_path = os.path.join('repos/%s.json' % repo)

        parent = os.path.dirname(cache_path)
        if not os.path.exists(parent):
            mkdirp(parent)

        if not os.path.exists(cache_path):
            cache = []
            i = 1
            stamps = get(repo, i)
            while stamps:
                cache.extend(stamps)
                i += 1
                stamps = get(repo, i)

            with open(cache_path, 'w') as f:
                f.write(json.dumps(cache))
            return cache
        else:
            with open(cache_path, 'r') as f:
                return json.load(f)

    jdata = reduce(lambda x,y:x+y, [load_json(r) for r in repos])
    return sorted(datetime.strptime(js['starred_at'], '%Y-%m-%dT%H:%M:%SZ')
                  for js in jdata)


x = get_stars('hpcugent/easybuild')
print x
print len(x)
