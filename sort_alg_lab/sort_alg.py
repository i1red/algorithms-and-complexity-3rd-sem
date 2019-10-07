import collections
import itertools
import random
import time
from inplace_merge_sort import inplace_merge_sort


def bubble_sort(arr):
    for i in range(1, len(arr) - 1):
        swapped = False
        for j in range(len(arr) - i):
            if arr[j][0] > arr[j + 1][0]:
                arr[j + 1], arr[j] = arr[j], arr[j + 1]
                swapped = True
        if not swapped:
            break


def fast_inplace_sort(arr):
    lt, rt = 0, len(arr) - 1
    while lt < rt:
        while arr[lt][0] == 0:
            lt += 1
        while arr[rt][0] == 1:
            rt -= 1
        if lt < rt:
            arr[lt], arr[rt] = arr[rt], arr[lt]


def fast_stable_sort(arr):
    buckets = [collections.deque(), collections.deque()]
    for i in range(len(arr)):
        buckets[arr[i][0]].append(arr[i])

    arr.clear()
    arr.extend(itertools.chain(*buckets))


def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i][0] > arr[i + 1][0]:
            return False

    return True


def test_sort_alg(alg, el_q, is_stable=False):
    start_gen = time.perf_counter()

    start_el = [(random.randint(0, 1), random.randint(-el_q, el_q)) for _ in range(el_q)]

    finish_gen = time.perf_counter()
    print(f'Generated test sequence in {finish_gen - start_gen} s')

    #built in sorted function is stable
    start_sort = time.perf_counter()

    sort_el = sorted(start_el, key=lambda x: x[0])

    finish_sort = time.perf_counter()
    print(f'Sorted with built-in function in {finish_sort - start_sort} s')

    start = time.perf_counter()

    alg(start_el)

    finish = time.perf_counter()
    print(f'Sorted with {alg.__name__} in {finish - start} s')
    print('OK' if is_sorted(start_el) and (not is_stable or start_el == sort_el) else 'FAILED')


test_sort_alg(inplace_merge_sort, 10000, is_stable=True)


