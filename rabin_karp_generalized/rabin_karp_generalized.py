import random
import string
import time
import worst_case


KEY_SYM, KEY_NUM = lambda sym: ord(sym), lambda num: num


def hash(seq, st_index, sub_len, x, q, key):
    """Returns polynomial hash of seq[st_index:st_index + sub_len]

    q - usually a prime number
    x - random number in range [0, q - 1]
    I am not using sequence slicing, because it creates a subsequence copy
    """

    #expression under sum - generator -> it doesn't create all sequence, yields elements one by one
    return sum(key(seq[st_index + i]) * (x ** (sub_len - i - 1)) for i in range(sub_len)) % q


def next_hash(pr_hash, pr_sym, nx_sym, sub_len, x, q, key):
    return ((pr_hash - key(pr_sym) * (x ** (sub_len - 1))) * x + key(nx_sym)) % q


def build_hash_matrix(matrix, sub_len, x, q, key):
    hash_matrix, max_i, max_j = [[hash(row, 0, sub_len, x, q, key) for row in matrix]], len(matrix[0]), len(matrix)

    for i in range(1, max_i - sub_len + 1):
        next_row = [next_hash(hash_matrix[i - 1][j], matrix[j][i - 1], matrix[j][i + sub_len - 1],
                              sub_len, x, q, key) for j in range(max_j)]
        hash_matrix.append(next_row)

    return hash_matrix


def check_string(strings, pattern, i, j):
    for p in range(len(pattern)):
        for q in range(len(pattern[0])):
            if strings[i + p][j + q] != pattern[p][q]:
                return False

    return True


def check_matches(strings, pattern, matched_hash):
    matched_res = []
    for i, j in matched_hash:
        if check_string(strings, pattern, i, j):
            matched_res.append((i, j))

    return matched_res


def rabin_karp_generalized_v1(strings, pattern):
    """Returns list of all matches with pattern
    """

    q = 1_000_000_007
    x = random.randint(0, q - 1)

    m1, m2 = len(pattern), len(pattern[0])

    #getting array of pattern strings hashes and calculating hash of the array
    tmp_arr = [hash(s, 0, m2, x, q, key=KEY_SYM) for s in pattern]
    hash_val = hash(tmp_arr, 0, m1, x, q, key=KEY_NUM)

    #getting matrix of hashes for substrings of length m2 and calculating hash matrix of this string
    #if there're matches with pattern hash value will be in hash_matrix
    tmp_matrix = build_hash_matrix(strings, m2, x, q, key=KEY_SYM)
    hash_matrix = build_hash_matrix(tmp_matrix, m1, x, q, key=KEY_NUM)

    matched_hash = []
    for i, row in enumerate(hash_matrix):
        for j, cur_hash in enumerate(row):
            if cur_hash == hash_val:
                matched_hash.append((i, j))

    return check_matches(strings, pattern, matched_hash)


def rabin_karp_generalized_v2(strings, pattern):
    q = 1_000_000_007
    x = random.randint(0, q - 1)

    pattern_m, pattern_n = len(pattern[0]), len(pattern)
    max_m, max_n = len(strings[0]) - pattern_m + 1, len(strings) - pattern_n + 1

    hash_val = hash(pattern[0], 0, pattern_m, x, q, key=KEY_SYM)
    hash_arr, matched_hash = [], []

    for i in range(max_n):
        cur_hash = hash(strings[i], 0, pattern_m, x, q, key=KEY_SYM)
        hash_arr.append(cur_hash)

        if cur_hash == hash_val:
            matched_hash.append((i, 0))

    for i in range(max_n):
        prev_hash = hash_arr[i]

        for j in range(1, max_m):
            cur_hash = next_hash(prev_hash, strings[i][j - 1], strings[i][j + pattern_m - 1],
                                 pattern_m, x, q, key=KEY_SYM)

            if cur_hash == hash_val:
                matched_hash.append((i, j))

            prev_hash = cur_hash

    return check_matches(strings, pattern, matched_hash)


#test functions
def rand_str(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def test(m1, m2, n1, n2, algorithm):
    i, j = random.randint(0, n1 - m1), random.randint(0, n2 - m2)

    pattern = [rand_str(m2) for _ in range(m1)]
    strings = [rand_str(n2) for _ in range(i)]
    pattern_copy = list(pattern)

    for p in range(len(pattern_copy)):
        pattern_copy[p] = rand_str(j) + pattern_copy[p] + rand_str(n2 - j - len(pattern_copy[p]))

    strings.extend(pattern_copy)
    strings.extend(rand_str(n2) for _ in range(n1 - m1 - i))

    res = algorithm(strings, pattern)
    print('OK' if (i, j) in res else '\nFAILED\n' + str(pattern) + '\n' + str(strings) + '\n', end=' ')

    return (pattern, pattern_copy, (i, j), res)


def test_worst_case(algorithm):
    start = time.perf_counter()

    pattern_m, pattern_n = len(worst_case.pattern[0]), len(worst_case.pattern)
    res_row = len(worst_case.strings) - pattern_n
    expected_res = [(res_row, i) for i in range(len(worst_case.strings[0]) - len(worst_case.pattern[0]) + 1)]

    res = algorithm(worst_case.strings, worst_case.pattern)
    print('OK' if expected_res == res else 'FAILED')

    print(time.perf_counter() - start)

    return res


def test_average(algorithm):
    start = time.perf_counter()

    for _ in range(100):
        test(51, 23, 103, 101, algorithm)

    print()
    print(time.perf_counter() - start)


if __name__ == '__main__':
    print('VERSION 1 (HASHING ALL STRINGS -> HASH MATRIX -> HASHING HASHES IN HASH MATRIX -> MATRIX OF MATCHES')
    print('WORST CASE')
    test_worst_case(rabin_karp_generalized_v1)
    print('AVERAGE CASE 100 RUNS')
    test_average(rabin_karp_generalized_v1)

    print()

    print('VERSION 2 (HASHING ONLY FIRST STRING IN PATTERN -> FINDING MATCHES')
    print('WORST CASE')
    test_worst_case(rabin_karp_generalized_v2)
    print('AVERAGE CASE 100 RUNS')
    test_average(rabin_karp_generalized_v2)
