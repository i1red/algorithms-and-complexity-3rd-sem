import random
import time


class Bolt:
    def __init__(self, shaft_size):
        self._shaft_size = shaft_size

    def __repr__(self):
        return f'Bolt({self.shaft_size})'

    def compare_to(self, nut):
        return 1 if self.shaft_size > nut.hole_size else (0 if self.shaft_size == nut.hole_size else -1)

    @property
    def shaft_size(self):
        return self._shaft_size


class Nut:
    def __init__(self, hole_size):
        self._hole_size = hole_size

    def __repr__(self):
        return f'Nut({self.hole_size})'

    def compare_to(self, bolt):
        return 1 if self.hole_size > bolt.shaft_size else (0 if self.hole_size == bolt.shaft_size else - 1)

    @property
    def hole_size(self):
        return self._hole_size


def partition(col, begin, end, pivot):
    smaller = begin - 1
    for i in range(begin, end):
        if pivot.compare_to(col[i]) >= 0:
            smaller += 1
            col[smaller], col[i] = col[i], col[smaller]

    col[smaller + 1], col[end] = col[end], col[smaller + 1]
    return smaller + 1


def incomparable_sort(lcol, rcol, begin, end):
    if begin < end:
        lpivot, rpivot = lcol[end], None

        for i in range(begin, end + 1):
            if lpivot.compare_to(rcol[i]) == 0:
                rpivot = rcol[i]
                rcol[end], rcol[i] = rcol[i], rcol[end]
                break

        lpi = partition(lcol, begin, end, rpivot)
        partition(rcol, begin, end, lpivot)

        incomparable_sort(lcol, rcol, begin, lpi - 1)
        incomparable_sort(lcol, rcol, lpi + 1, end)



def bolts_and_nuts_sort(bolts, nuts):
    end = len(bolts) - 1
    incomparable_sort(bolts, nuts, 0, end)


if __name__ == '__main__':
    nums = [i for i in range(10_000)]
    random.shuffle(nums)
    bolts = [Bolt(i) for i in nums]
    random.shuffle(nums)
    nuts = [Nut(i) for i in nums]

    blt = sorted(bolts, key=lambda x: x.shaft_size)
    nt = sorted(nuts, key=lambda x: x.hole_size)

    start = time.perf_counter()
    bolts_and_nuts_sort(bolts, nuts)
    finish = time.perf_counter()

    print(f'Finished in {finish - start} s')
    print('OK' if bolts == blt and nuts == nt else 'FAILED')