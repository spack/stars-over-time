#!/usr/bin/env spack-python
from __future__ import division

import os
import json
import sys
from github import Github
from datetime import timedelta as td

import numpy as np
import matplotlib.pyplot as plt

from llnl.util.filesystem import mkdirp


def dump(data, out):
    json.dump(data, out, indent=True, separators=(',', ': '))


def get_token():
    token_file = os.path.expanduser('~/.github/analysis-token')
    with open(token_file) as f:
        return f.read().strip()

#: GitHub object for fetching data about repos
gh = Github(get_token())

#: cache of repo star data
cache = {}

def get_stargazers_with_dates(repo_name):
    """Get data about a repository from GitHub"""
    stargazers = cache.get(repo_name)
    if not stargazers:
        repo = gh.get_repo(repo_name)
        stargazers = repo.get_stargazers_with_dates()
        cache[repo_name] = stargazers
    return stargazers


def get_stars(*repos):
    """Get the dates that users *first* starred *any* of a list of repos."""
    repo_stars = []

    users_to_stars = {}
    for repo_name in repos:
        stargazers = get_stargazers_with_dates(repo_name)
        for sg in stargazers:
            users_to_stars.setdefault(sg.user.login, []).append(sg.starred_at)

    return sorted(min(v) for v in users_to_stars.values())


def stars_per_day(dates, count, window=60):
    """Compute a moving, centered average of stars per day.

    Average stars per day is always over the window *preceding* each
    point in the input array.
    """
    def days(td):
        return td.total_seconds() / 86400

    spd = [float('nan')] * len(count)
    pairs = zip(dates, count)

    # start after the first window
    start = 0
    while start < len(count) and days(dates[start] - dates[0]) < window:
        start += 1

    # now slide the window over remaining data points.  Window is always
    # in the past.
    for i, (d, c) in enumerate(pairs[start:], start):
        # prefer a window behind the current data point
        lo = i - 1
        while lo > 0 and days(dates[i] - dates[lo]) < window:
            lo -= 1

        stars = count[i] - count[lo]
        delta = days(dates[i] - dates[lo])
        spd[i] = stars / delta

    return spd


def do_plots(*label_repo_list_tuples):
    over_time_fig, over_time_ax = plt.subplots(figsize=(8, 4), dpi=320)
    per_day_fig, per_day_ax = plt.subplots(figsize=(8, 4), dpi=320)
    window = 60

    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45)
    for label, repo_list in label_repo_list_tuples:
        dates = get_stars(*repo_list)
        counts = range(1, len(dates) + 1)
        spd = stars_per_day(dates, counts, window=window)

        print "%-40s%d" % (label, len(counts))
        over_time_ax.plot(dates, counts, label=label)
        per_day_ax.plot(dates, spd, label=label)

    # first figure
    over_time_ax.set_title('GitHub Stars')
    over_time_ax.legend(loc='upper left')
    over_time_ax.spines['top'].set_visible(False)
    over_time_ax.spines['right'].set_visible(False)
    over_time_ax.grid(axis='y')

    over_time_fig.tight_layout()
    over_time_fig.savefig('stars-over-time.pdf')

    # second figure
    per_day_ax.set_title('GitHub stars per day (%d-day window)' % window)
    per_day_ax.legend(loc='upper left')
    per_day_ax.spines['top'].set_visible(False)
    per_day_ax.spines['right'].set_visible(False)
    per_day_ax.grid(axis='y')

    per_day_fig.tight_layout()
    per_day_fig.savefig('stars-per-day.pdf')


do_plots(
    ('spack', ['spack/spack']),
    ('openhpc/ohpc', ['openhpc/ohpc']),
    ('open-mpi/ompi', ['open-mpi/ompi']),
    ('sylabs/singularity', ['sylabs/singularity']),
    ('easybuild (all 4 repos)', ['easybuilders/easybuild',
                                 'easybuilders/easybuild-framework',
                                 'easybuilders/easybuild-easyblocks',
                                 'easybuilders/easybuild-easyconfigs']),
    ('easybuild (main repo)', ['easybuilders/easybuild']),
    ('mfem', ['mfem/mfem']),
    ('ck', ['ctuning/ck']),

#    ('hashdist', ['hashdist/hashdist']),
#    ('trilinos', ['trilinos/Trilinos']),
#    ('rose', ['rose-compiler/rose']),
#    ('conda', ['conda/conda']),
#    ('linuxbrew', ['linuxbrew/brew']),
#    ('kubernetes', ['kubernetes/kubernetes']),
#    ('zfsonlinux/zfs', ['zfsonlinux/zfs']),
#    ('homebrew/brew', ['homebrew/brew']),
)
