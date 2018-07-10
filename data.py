import csv
import linecache


class RandomCSVReader:
    def __init__(self, csvfile):
        with open(csvfile) as f:
            self._total = len(f.readlines())
        self._csvfile = csvfile

    def __len__(self):
        return self._total

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            return [self._get_line(i) for i in range(start, stop, step)]
        else:
            return self._get_line(index)

    def _get_line(self, i):
        return next(csv.reader([linecache.getline(self._csvfile, i + 1)]))
