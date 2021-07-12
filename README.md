# Stars over time

This script plots github stars over time, as well as the *rate* of star accumulation over time.

Usage:

```
$ ./stars-over-time.py
spack                                   838
openhpc/ohpc                            367
open-mpi/ompi                           713
sylabs/singularity                      1041
easybuild (all 4 repos)                 412
mfem                                    283
ck                                      263
$ ls
README.md  requirements.txt  stargazers/  stars-over-time.pdf  stars-over-time.py*  stars-per-day.pdf
```

`stars-over-time.pdf` will have plots of the *cumulative* stars over time, while stars-per-day has
a plot of the stars added to the repo per-day, averaged over a 60-day sliding window (otherwise
it's too noisy for most repos).


## License

This project is part of Spack. Spack is distributed under the terms of both the
MIT license and the Apache License (Version 2.0). Users may choose either
license, at their option.

All new contributions must be made under both the MIT and Apache-2.0 licenses.

See LICENSE-MIT, LICENSE-APACHE, COPYRIGHT, and NOTICE for details.

SPDX-License-Identifier: (Apache-2.0 OR MIT)

LLNL-CODE-811652
