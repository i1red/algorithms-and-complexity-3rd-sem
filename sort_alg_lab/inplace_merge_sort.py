import sys


sys.setrecursionlimit(10**5)


def insertion_sort(arr, begin, end):
    for i in range(begin + 1, end):
        tmp = arr[i]
        j = i - 1
        while j >= begin and tmp[0] < arr[j][0]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = tmp


def inplace_merge(arr, begin, mid, end):
    if end - begin < 2 or arr[mid - 1][0] <= arr[mid][0]:
        return

    if end - begin < 16:
        insertion_sort(arr, begin, end)
    else:
        lt, rt = mid - 1, mid
        while lt > begin and rt + 1 < end:
            if arr[lt - 1][0] > arr[rt + 1][0]:
                lt -= 1
                rt += 1
            else:
                break
        step = mid - lt
        for i in range(lt, mid):
            arr[i + step], arr[i] = arr[i], arr[i + step]
        inplace_merge(arr, begin, lt, mid)
        inplace_merge(arr, mid, rt + 1, end)


def inplace_msort(arr, begin, end):
    if end - begin < 2:
        return

    if end - begin < 16:
        insertion_sort(arr, begin, end)
    else:
        mid = (begin + end) // 2
        inplace_msort(arr, begin, mid)
        inplace_msort(arr, mid, end)
        inplace_merge(arr, begin, mid, end)


def inplace_merge_sort(arr):
    inplace_msort(arr, 0, len(arr))

