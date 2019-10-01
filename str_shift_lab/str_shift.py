# Using Z algorithm
def is_substr(sample, substr):
    concat = substr + '$' + sample
    z_arr = [0 for _ in range(len(concat))]
    lt = rt = 0
    for i in range(1, len(concat)):
        if i > rt:
            lt = rt = i
            while rt < len(concat) and concat[rt - lt] == concat[rt]:
                rt += 1
            z_arr[i] = rt - lt
            rt -= 1
        else:
            k = i - lt
            if z_arr[k] <= rt - i:
                z_arr[i] = z_arr[k]
            else:
                lt = i
                while rt < len(concat) and concat[rt - lt] == concat[rt]:
                    rt += 1
                z_arr[i] = rt - lt
                rt -= 1

        if z_arr[i] == len(substr):
            return True

    return False


def is_shifted(sample, shift):
    if len(sample) != len(shift):
        return False

    return is_substr(sample * 2, shift)


def test_is_shifted():
    failed = ok = 0
    # test1
    sample = 'abcd'
    shift = 'cdab'
    if not is_shifted(sample, shift):
        print(f'TEST FAILED: {shift} is shifted {sample}, is_shifted returned False')
        failed += 1
    else:
        ok += 1

    # test2
    sample = 'aaaaaab'
    shift = 'aabaaaa'
    if not is_shifted(sample, shift):
        print(f'TEST FAILED: {shift} is shifted {sample}, is_shifted returned False')
        failed += 1
    else:
        ok += 1

    # test3
    sample = 'aaaab'
    shift = 'aaba'
    if is_shifted(sample, shift):
        print(f'TEST FAILED: {shift} is NOT shifted {sample}, is_shifted returned True')
        failed += 1
    else:
        ok += 1

    # test4
    sample = 'wyudwhddqiudwdqbwdwjxwqnababwdsb'
    shift = 'udwdqbwdwjxwqnababwdsbwyudwhddqi'
    if not is_shifted(sample, shift):
        print(f'TEST FAILED: {shift} is shifted {sample}, is_shifted returned False')
        failed += 1
    else:
        ok += 1

    # test5
    sample = 'wyudwhddqiudwdqbwdwjxwqnababwdsb'
    shift = 'udwdqbwdwjxwanqbabwdsbwyudwhddqi'
    if is_shifted(sample, shift):
        print(f'TEST FAILED: {shift} is NOT shifted {sample}, is_shifted returned True')
        failed += 1
    else:
        ok += 1

    print(f'RAN {ok + failed} TESTS\n{ok} - OK, {failed} - FAILED')


test_is_shifted()
