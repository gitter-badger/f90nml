"""f90nml.findex
   =============

   Column-major Fortran iterator of indices across multipe dimensions.

   :copyright: Copyright 2015 Marshall Ward, see AUTHORS for details.
   :license: Apache License, Version 2.0, see LICENSE for details.
"""


class FIndex(object):
    """Column-major multidimensional index iterator"""

    def __init__(self, bounds):
        self.start = [1 if b[0] is None else b[0] for b in bounds]
        self.end = [b[1] for b in bounds]
        self.step = [1 if b[2] is None else b[2] for b in bounds]

        self.current = self.start[:]

        # Default global starting index (assumes 1-indexing)
        self.first = [min(1, s) for s in self.start]

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if self.end[-1] and self.current[-1] >= self.end[-1]:
            raise StopIteration

        state = self.current[:]
        # Allow the final index to exceed self.end[-1] as a finalisation check
        for rank, idx in enumerate(self.current):
            if ((not self.end[rank] or idx < (self.end[rank] - 1)) or
                    rank == (len(self.current) - 1)):
                self.current[rank] = idx + self.step[rank]
                break
            else:
                self.current[rank] = self.start[rank]

        return state
