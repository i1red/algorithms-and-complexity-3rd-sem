def quick_sort_rec(arr, begin, end):
    if begin < end:
        last_smaller = begin - 1
        pivot = arr[end]

        for j in range(begin, end):
            if arr[j] <= pivot:
                last_smaller += 1
                arr[last_smaller], arr[j] = arr[j], arr[last_smaller]

        arr[last_smaller + 1], arr[end] = arr[end], arr[last_smaller + 1]
        quick_sort_rec(arr, begin, last_smaller)
        quick_sort_rec(arr, last_smaller + 2, end)


def quick_sort(arr):
    quick_sort_rec(arr, 0, len(arr) - 1)




