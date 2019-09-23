import uuid
import os
import filetools as ftools
from arr_sort import quick_sort
import time


def divide_input_file(f, a, b, size: 'int > 0'):
    cur_out, s = a, 0

    chunk = ftools.read_chunk(f, size)
    while len(chunk) > 0:
        s += len(chunk)
        quick_sort(chunk)
        chunk.tofile(cur_out)
        cur_out = a if cur_out is b else b
        chunk = ftools.read_chunk(f, size)

    return s


def poly_phase_sort(filename: str, s: 'int > 0'):
    if s <= 0:
        raise ValueError('Non-positive size number was passed')

    part1_start = time.time()

    temp_files_dir = str(uuid.uuid4().hex)

    part1_end = time.time()

    print('Generated temp dir and calculated distribution:', part1_end - part1_start, 's')
    with ftools.create_temp_files(temp_files_dir, 4) as [a, b, c, d], open(filename, 'rb+') as f:
        number_of_blocks = divide_input_file(f, a, b, s)

        part2_end = time.time()
        print('Generated tmp files and filled them:', part2_end - part1_end, 's')

        input1, input2, cur_out = a, b, c
        size, block_count = s, 0

        while block_count < number_of_blocks:
            input1.seek(0)
            input2.seek(0)

            if input1 is a:
                ftools.clear(c, d)
            else:
                ftools.clear(a, b)

            count_read = 0

            while count_read < number_of_blocks:

                block1, block2 = ftools.read(input1), ftools.read(input2)
                i, j = 0 if block1 is None else 1, 0 if block2 is None else 1

                while (i <= size or j <= size) and (block1 is not None or block2 is not None):
                    if block1 is not None and (block2 is None or block1 < block2):
                        ftools.write(cur_out, block1)
                        if i + 1 <= size:
                            block1 = ftools.read(input1)
                            i += 0 if block1 is None else 1
                        else:
                            block1 = None
                    elif block2 is not None:
                        ftools.write(cur_out, block2)
                        if j + 1 <= size:
                            block2 = ftools.read(input2)
                            j += 0 if block2 is None else 1
                        else:
                            block2 = None

                block_count = i + j
                count_read += block_count

                if cur_out is a:
                    cur_out = b
                elif cur_out is b:
                    cur_out = a
                elif cur_out is c:
                    cur_out = d
                elif cur_out is d:
                    cur_out = c

            size *= 2
            if input1 is a:
                input1, input2, cur_out = c, d, a
            else:
                input1, input2, cur_out = a, b, c

        part3_end = time.time()
        print('Sorted all elements:', part3_end - part2_end, 's')

        cur_out = a if cur_out is c else c
        cur_out.seek(0)
        res_file = str(uuid.uuid4().hex) + '.bin'
        with open(res_file, 'wb') as res:
            block = ftools.read(cur_out)
            while block is not None:
                ftools.write(res, block)
                block = ftools.read(cur_out)
        ftools.clear(a, b, c, d)

        part4_end = time.time()
        print('Written to res file:', part4_end - part3_end, 's')
        print('Total:', part4_end - part1_end, 's')

        return res_file


def test_poly_phase(el_q, run_s):
    print(f'TESTING POLY PHASE SORT: el_q={el_q}, run_s={run_s}')

    test_file = 'test_files/test.bin'
    ftools.generate_test_file(test_file, el_q)
    res_file = poly_phase_sort(test_file, run_s)
    sort_el, start_el = [], []
    with open(test_file, 'rb') as test:
        num = ftools.read(test)
        while num is not None:
            start_el.append(num)
            num = ftools.read(test)

    with open(res_file, 'rb') as res:
        num = ftools.read(res)
        while num is not None:
            sort_el.append(num)
            num = ftools.read(res)

    os.remove(test_file)
    os.remove(res_file)

    print('OK' if sorted(start_el) == sort_el else 'FAILED')


test_poly_phase(1_500_000, 10000)
print(f"Res file: {poly_phase_sort('test_files/15mb.bin', 20000)}")