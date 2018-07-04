import csv
import linecache


class RandomCSVReader:
    def __init__(self, csvfile):
        with open(csvfile) as f:
            self._total = len(f.readlines()) - 1
        self._csvfile = csvfile

    def __len__(self):
        return self._total

    def __getitem__(self, index):
        def getline(i):
            return linecache.getline(self._csvfile, i + 1)

        if isinstance(index, slice):
            stop = len(self) + 1
            lines = [getline(i)
                     for i in range(index.start or 0,
                                    min(index.stop or stop, stop),
                                    index.step or 1)]
            data = [row for row in csv.reader(lines)]
        else:
            if index > len(self):
                raise IndexError
            data = next(csv.reader([getline(index)]))

        return data
