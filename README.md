# Stars over time

This script plots github stars over time, as well as the *rate* of star accumulation over time.

Usage:

```console
$ ./stars-over-time.py
(spackle):stars> ./stars-over-time.py
singularity                             2134
spack                                   2134
chapel                                  1323
openmpi                                 1298
openhpc                                 572
easybuild (all 4 repos)                 561
mpich                                   305
shifter                                 315
charliecloud                            212
singularityCE                           55
```

This creates two files:
* `stars-over-time.pdf` will have plots of the *cumulative* stars over time.
* `stars-per-day.pdf` has a plot of the stars added to the repo per-day, averaged over a 60-day
   sliding window (otherwise it's too noisy for most repos).

They look like this:

<img src="https://raw.githubusercontent.com/spack/stars-over-time/main/images/stars-over-time.svg" width="384" valign="middle" alt="Plot of cumulative stars over time for above repositories"/>   <img src="https://raw.githubusercontent.com/spack/stars-over-time/main/images/stars-per-day.svg" width="384" valign="middle" alt="Plot of stars per day for above repositories"/>

## License

This project is part of Spack. Spack is distributed under the terms of both the
MIT license and the Apache License (Version 2.0). Users may choose either
license, at their option.

All new contributions must be made under both the MIT and Apache-2.0 licenses.

See LICENSE-MIT, LICENSE-APACHE, COPYRIGHT, and NOTICE for details.

SPDX-License-Identifier: (Apache-2.0 OR MIT)

LLNL-CODE-811652
