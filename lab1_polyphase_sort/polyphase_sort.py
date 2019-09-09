import random


def merge_sort(container):
    if len(container) > 1:
        lt_part, rt_part = container[:len(container)//2], container[len(container)//2:]

        merge_sort(lt_part)
        merge_sort(rt_part)

        i = j = k = 0

        while i < len(lt_part) and j < len(rt_part):
            if lt_part[i] < rt_part[j]:
                container[k] = lt_part[i]
                i += 1
            else:
                container[k] = rt_part[j]
                j += 1
            k += 1

        while i < len(lt_part):
            container[k] = lt_part[i]
            i += 1
            k += 1

        while j < len(rt_part):
            container[k] = rt_part[j]
            j += 1
            k += 1


def read_block(file):
    read_value = ''

    while True:
        sym = file.read(1)
        if len(sym) == 0 or sym == ' ':
            break
        read_value += sym

    return eval(read_value) if len(read_value) != 0 else None


def write_block(file, block):
    file.write(repr(block) + ' ')


def read_portion(file, size: 'int > 0'):
    portion = []
    i = 0

    while i < size:
        block = read_block(file)
        if block is None:
            break
        portion.append(block)
        i += 1

    return portion if len(portion) != 0 else None


def write_portion(file, portion):
    file.write(' '.join(repr(i) for i in portion) + ' ')


def clear(*files):
    for file in files:
        file.seek(0)
        file.truncate(0)


def divide_input_file(f, a, b, size: 'int > 0'):
    cur_out, s = a, 0

    while True:
        portion = read_portion(f, size)
        if portion is None:
            break
        s += len(portion)
        merge_sort(portion)
        write_portion(cur_out, portion)
        cur_out = a if cur_out is b else b

    return s


def poly_phase_sort(filename: str, s: 'int > 0'):
    if s <= 0:
        raise ValueError('Non-positive size number was passed')

    with open('a.txt', 'r+') as a, open('b.txt', 'r+') as b, open('c.txt', 'r+') as c, open('d.txt', 'r+') as d, \
            open(filename, 'r+') as f:
        number_of_blocks = divide_input_file(f, a, b, s)
        input1, input2, cur_out = a, b, c
        size, block_count = s, 0

        while block_count < number_of_blocks:
            input1.seek(0)
            input2.seek(0)

            if input1 is a:
                clear(c, d)
            else:
                clear(a, b)

            count_read = 0

            while count_read < number_of_blocks:

                block1, block2 = read_block(input1), read_block(input2)
                i, j = 0 if block1 is None else 1, 0 if block2 is None else 1

                while (i <= size or j <= size) and (block1 is not None or block2 is not None):
                    if block1 is not None and (block2 is None or block1 < block2):
                        write_block(cur_out, block1)
                        if i + 1 <= size:
                            block1 = read_block(input1)
                            i += 0 if block1 is None else 1
                        else:
                            block1 = None
                    elif block2 is not None:
                        write_block(cur_out, block2)
                        if j + 1 <= size:
                            block2 = read_block(input2)
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

        cur_out = a if cur_out is c else c
        cur_out.seek(0)
        clear(f)
        block = read_block(cur_out)
        while block is not None:
            write_block(f, block)
            block = read_block(cur_out)
        clear(a, b, c, d)


def test_poly_phase():
    test_file = 'test.txt'

    test_list = [random.randint(-1000, 1000) for i in range(100)]
    test_list.sort()

    test_list_copy = list(test_list)
    for i in range(5):
        random.shuffle(test_list_copy)

        with open(test_file, 'r+') as f:
            clear(f)
            write_portion(f, test_list_copy)

        sort_res = []
        poly_phase_sort(test_file, random.randint(1, 11))
        with open(test_file) as f:
            sort_res = read_portion(f, len(test_list))

        if sort_res != test_list:
            return False

    return True

test_res = test_poly_phase()
print('OK' if test_res == True else 'FAILED')
