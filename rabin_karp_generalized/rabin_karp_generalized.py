import random
import string


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


def rabin_karp_generalized(strings, pattern):
    """Returns list of all matches with pattern
    """

    q = 1_000_000_007
    x = random.randint(0, q - 1)

    m1, m2 = len(pattern), len(pattern[0])

    key_sym, key_num = lambda sym: ord(sym), lambda num: num

    #getting array of pattern strings hashes and calculating hash of the array
    tmp_arr = [hash(s, 0, m2, x, q, key=key_sym) for s in pattern]
    hash_val = hash(tmp_arr, 0, m1, x, q, key=key_num)

    #getting matrix of hashes for substrings of length m2 and calculating hash matrix of this string
    #if there're matches with pattern hash value will be in hash_matrix
    tmp_matrix = build_hash_matrix(strings, m2, x, q, key=key_sym)
    hash_matrix = build_hash_matrix(tmp_matrix, m1, x, q, key=key_num)

    matched_hash = []
    for i, row in enumerate(hash_matrix):
        try:
            j = row.index(hash_val)
        except ValueError:
            pass
        else:
            matched_hash.append((i, j))

    matched_res = []
    for i, j in matched_hash:
        if check_string(strings, pattern, i, j):
            matched_res.append((i, j))

    return matched_res


#test functions
def rand_str(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def test():
    m1, m2 = random.randint(1, 12), random.randint(1, 12)
    n1, n2 = random.randint(20, 25), random.randint(20, 25)
    i, j = random.randint(0, n1 - m1), random.randint(0, n2 - m2)

    pattern = [rand_str(m2) for _ in range(m1)]
    strings = [rand_str(n2) for _ in range(i)]
    pattern_copy = list(pattern)

    for p in range(len(pattern_copy)):
        pattern_copy[p] = rand_str(j) + pattern_copy[p] + rand_str(n2 - j - len(pattern_copy[p]))

    strings.extend(pattern_copy)
    strings.extend(rand_str(n2) for _ in range(n1 - m1 - i))

    res = rabin_karp_generalized(strings, pattern)
    print('OK' if (i, j) in res else 'FAILED')

    return (pattern, pattern_copy, (i, j), res)


if __name__ == '__main__':
    for _ in range(100):
        test()