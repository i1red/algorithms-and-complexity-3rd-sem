import os
import math
import uuid
import fibo_sort_lab.filetools as ftools
import fibo_sort_lab.priorityqueue as pq
import time
from array import array

END = -1


def merge_sort(arr):
    if len(arr) < 2:
        return

    mid = len(arr) // 2
    left_part, right_part = arr[:mid], arr[mid:]
    merge_sort(left_part)
    merge_sort(right_part)

    i = j = k = 0
    while i < len(left_part) and j < len(right_part):
        if left_part[i] < right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1

    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1


def hor_distr(runs_quantity, files_quantity):
    distribution = [0 for i in range(files_quantity)]
    tmp = list(distribution)
    distribution[0] = 1

    while sum(distribution) < runs_quantity:
        max_val = max(distribution)
        index = distribution.index(max_val)
        for i in range(files_quantity):
            tmp[i] = 0 if i == index else tmp[i] + max_val
        distribution = list(tmp)

    return sorted(distribution, reverse=True)


def dummy_distr(hor_distr, runs_quantity, files_quantity):
    dummy_q = sum(hor_distr) - runs_quantity
    dummy_p = math.ceil(dummy_q / (files_quantity - 1))
    dummy = []
    for i in range(files_quantity - 1):
        if dummy_q > 0:
            dummy.append(dummy_p if dummy_q - dummy_p > 0 else dummy_q)
            dummy_q -= dummy_p
        else:
            dummy.append(0)
    dummy.append(0)
    return dummy


def fibo_sort(source_file: str, run_size: 'int > 0', files_quantity: 'int > 2'):
    part1_start = time.time()
    temp_files_dir = str(uuid.uuid4().hex)
    runs_quantity = math.ceil(os.path.getsize(source_file) / (run_size * 4))

    distr = hor_distr(runs_quantity, files_quantity)
    dummy = dummy_distr(distr, runs_quantity,files_quantity)
    part1_end = time.time()
    print('Generated temp dir and calculated distribution:', part1_end - part1_start, 's')

    with ftools.create_temp_files(temp_files_dir, files_quantity) as files:
        for i in range(files_quantity - 1):
            for dum in range(dummy[i]):
                ftools.write(files[i], END)

        with open(source_file, 'rb') as source:
            for i in range(files_quantity - 1):
                for run in range(distr[i] - dummy[i]):
                    chunk = ftools.read_chunk(source, run_size)
                    merge_sort(chunk)
                    chunk.tofile(files[i])
                    ftools.write(files[i], END)

        part2_end = time.time()
        print('Generated tmp files and filled them:', part2_end -part1_end, 's')

        qu = pq.PriorityQueueBST()

        file_ptrs = [0 for i in range(files_quantity)]

        output = 0
        while max(distr) != 1 or distr.count(0) != len(distr) - 1:
            for i, f in enumerate(files):
                f.seek(file_ptrs[i])

            output = distr.index(0)

            while min(distr[:output] + distr[output+1:]) != 0:
                runs_ended = [False for i in range(files_quantity)]
                for i in range(files_quantity):
                    if i != output:
                        num = ftools.read(files[i])
                        if num is None or num == END:
                            runs_ended[i] = True
                        else:
                            qu.append(num, i)

                while len(qu) > 0:
                    min_el_val, min_el_index = qu.pop()
                    ftools.write(files[output], min_el_val)
                    if not runs_ended[min_el_index]:
                        num = ftools.read(files[min_el_index])
                        if num is None or num == END:
                            runs_ended[min_el_index] = True
                        else:
                            qu.append(num, min_el_index)

                ftools.write(files[output], END)

                for i in range(files_quantity):
                    distr[i] = distr[i] - 1 if i != output else distr[i] + 1
                    if i != output:
                        file_ptrs[i] = files[i].tell()

        part3_end = time.time()
        print('Sorted all elements:', part3_end - part2_end, 's')

        files[output].seek(file_ptrs[output])
        with open('res.bin', 'wb') as res:
            num = ftools.read(files[output])
            while num is not None and num != END:
                ftools.write(res, num)
                num = ftools.read(files[output])

        part4_end = time.time()
        print('Written to res file:' ,part4_end - part3_end, 's')
        print('Total:', part4_end - part1_end, 's')



