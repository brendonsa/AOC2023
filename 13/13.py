import math
import numpy as np
FILENAME = "13.txt"


def read_data(filename):
    lines_all = []
    lines = []
    with open(filename) as f:
        for line in f:
            if len(line.strip()) == 0:
                lines_all.append(np.vstack(lines))
                lines = []
            else:
                lines.append(
                    list(map(int, list(line.strip().replace('#', '1').replace('.', '0')))))
    if len(lines) > 0:
        lines_all.append(np.vstack(lines))
    return lines_all


def transform_binary_list_to_int(data):
    new_data = np.zeros(len(data))
    for idx, d in enumerate(data):
        new_data[idx] = int(''.join(list(map(str, d))), 2)
    return new_data


def horizontal_mirror(data):
    data = transform_binary_list_to_int(data)
    idxes = []
    for idx in range(len(data)-1):
        if data[idx] == data[idx+1]:
            left = idx
            right = idx+1
            # Split data to left and right
            data_left = data[:left+1]
            data_right = data[right:]
            length_diff = len(data_left) - len(data_right)
            if length_diff > 0:
                data_left = data_left[length_diff:]
            elif length_diff < 0:
                data_right = data_right[:length_diff]
            # Reverse data
            data_left = data_left[::-1]
            if all(data_left == data_right):
                return idx+1
    raise ValueError("There is no horizontal mirror")


def find_mirrors(data):
    mirror = None
    try:
        mirror = horizontal_mirror(data)*100
    except ValueError:
        try:
            mirror = horizontal_mirror(data.T)
        except:
            print('No mirror found')
    return mirror


data = read_data(FILENAME)

sum_mirrors = 0
for d in data:
    sum_mirrors += find_mirrors(d)

print(sum_mirrors)

# Part 2


def difference_is_log2(n):
    count_zeroes = sum(n == 0)
    if count_zeroes < len(n)-1:
        return False
    n = sum(n)
    if n == 0:
        return False
    return math.log(n, 2).is_integer()


def horizontal_mirror_smudge(data):
    data = transform_binary_list_to_int(data)
    idxes = []
    points = []
    for idx in range(len(data)-1):
        left = idx
        right = idx+1
        data_left = data[:left+1]
        data_right = data[right:]
        length_diff = len(data_left) - len(data_right)
        if length_diff > 0:
            data_left = data_left[length_diff:]
        elif length_diff < 0:
            data_right = data_right[:length_diff]
        # Reverse data
        data_left = data_left[::-1]
        if difference_is_log2(np.abs(data_left - data_right)):
            idxes.append(idx+1)
            points.append(np.abs(data_left-data_right))

    if len(idxes) == 0:
        raise ValueError("There is no horizontal mirror")
    if len(idxes) > 1:
        # THIS IS A STRANGE PART
        # We return idx where points len is longer
        # SOMEHOW SOME OF THE COMBINATIONS CAN BE MIRRORED MORE THAN ONCE
        # AND IT LOOKS LIKE THEY WANT BIGGEST MIRROR
        return idxes[np.argmax(list(map(lambda x: len(x), points)))]
    return idxes[0]


def find_mirrors_smudge(data):
    mirror = None
    try:
        mirror = horizontal_mirror_smudge(data.T)
    except ValueError:
        try:
            mirror = horizontal_mirror_smudge(data)*100
        except:
            print('No mirror found')
    return mirror


sum_mirrors = 0
for d in data:
    sum_mirrors += find_mirrors_smudge(d)

print(sum_mirrors)
