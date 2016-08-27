#!/usr/bin/env spack-python
import sys
sys.path += ['.']
import matplotlib.pyplot as plt
from stars import get_stars


lines = []
def plot(label, repos):
    dates = get_stars(*repos)
    count = range(1, len(dates) + 1)
    line, = plt.plot(dates, count, label=label)
    lines.append(line)

locs, labels = plt.xticks()
plt.setp(labels, rotation=45)


plot('spack', ['LLNL/spack'])
plot('easybuild (all)', ['hpcugent/easybuild',
                         'hpcugent/easybuild-framework',
                         'hpcugent/easybuild-easyblocks',
                         'hpcugent/easybuild-easyconfigs'])
plot('easybuild (main only)', ['hpcugent/easybuild'])

plt.legend(loc='upper left')
plt.savefig('spack_vs_eb.pdf')
