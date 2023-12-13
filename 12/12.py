import re
from functools import cache
from itertools import product
FILENAME = '12.txt'


def read_data(filename):
    initial = []
    counts = []
    with open(filename, 'r') as f:
        for line in f:
            i, c = line.strip().split(' ')
            initial.append(i)
            c = list(map(int, c.split(',')))
            counts.append(c)
    return initial, counts


pattern = re.compile(r'#+')


def confirm_broken(string, configuration):
    found = re.findall(pattern, string)
    for f, c in zip(found, configuration):
        if len(f) != c:
            return False
    return True


def find_combinations(initial, counts):
    comb_found = []
    unk_count = initial.count('?')
    initial_count = initial.count('#')
    final_count = sum(counts)
    diff = final_count - initial_count
    for comb in filter(lambda x: x.count('#') == diff, product(('#', '.'), repeat=unk_count)):
        new_string = initial
        for c in comb:
            new_string = new_string.replace('?', c, 1)
        if confirm_broken(new_string, counts):
            comb_found.append(new_string)
    return comb_found


found_combinations = 0
initial, counts = read_data(FILENAME)

for i, c in zip(initial, counts):
    found_combinations += len(find_combinations(i, c))

print(found_combinations)


@cache
def find_combinations_cached(springs, counts, depth=0):
    # Return condition
    if len(springs) == 0:
        if (len(counts) == 1 and counts[0] == depth):
            # If its the last count that is equal to window length (depth)
            return 1
        elif (len(counts) == 0 and depth == 0):
            # If there will not be any more broken springs and the window is empty
            return 1
        else:
            return 0

    if len(counts) == 0:
        counts = tuple([0])
    if springs[0] == '?':
        return find_combinations_cached(springs.replace('?', '#', 1), counts, depth) + find_combinations_cached(springs.replace('?', '.', 1), counts, depth)
    if springs[0] == '#':
        if depth > counts[0]:
            return 0
        else:
            return find_combinations_cached(springs[1:], counts, depth+1)
    if springs[0] == '.':
        if depth == 0:
            return find_combinations_cached(springs[1:], counts, 0)
        if depth == counts[0]:
            return find_combinations_cached(springs[1:], counts[1:], 0)
        return 0


counts = [tuple(c*5)for c in counts]
found_combinations = 0

for i, c in zip(initial, counts):
    found_combinations += find_combinations_cached('?'.join([i]*5), c)
print(found_combinations)
