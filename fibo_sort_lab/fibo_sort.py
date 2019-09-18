import os
import math
import uuid
import fibo_sort_lab.filetools as ftools
import fibo_sort_lab.priorityqueue as pq

END = -1


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
    temp_files_dir = str(uuid.uuid4().hex)
    runs_quantity = math.ceil(os.path.getsize(source_file) / (run_size * 4))

    distr = hor_distr(runs_quantity, files_quantity)
    dummy = dummy_distr(distr, runs_quantity,files_quantity)

    with ftools.create_temp_files(temp_files_dir, files_quantity) as files:
        for i in range(files_quantity - 1):
            dummy_count = 0
            while dummy_count < dummy[i]:
                ftools.write(files[i], END)
                dummy_count += 1

        with open(source_file, 'rb') as source:
            for i in range(files_quantity - 1):
                run_count = 0
                while run_count < distr[i] - dummy[i]:
                    chunk, j = [], 0
                    while j < run_size:
                        num = ftools.read(source)
                        if num is not None:
                            chunk.append(num)
                        j += 1

                    chunk.sort()

                    for el in chunk:
                        ftools.write(files[i], el)
                    ftools.write(files[i], END)
                    run_count += 1


        qu = pq.PriorityQueueBST()

        file_ptrs = [0 for i in range(files_quantity)]

        output = 0
        while max(distr) != 1 or distr.count(0) != len(distr) - 1:
            for i, f in enumerate(files):
                f.seek(file_ptrs[i])

            output = distr.index(0)

            while min(dst for i, dst in enumerate(distr) if i != output) != 0:
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


        files[output].seek(file_ptrs[output])
        with open('res.bin', 'wb') as res:
            num = ftools.read(files[output])
            while num is not None and num != END:
                ftools.write(res, num)
                num = ftools.read(files[output])



