FILENAME = "15.txt"


def hash_iter(value, char):

    value = value + ord(char)
    value = value * 17
    return value % 256


def hash(string):
    value = 0
    for char in string:
        value = hash_iter(value, char)
    return value


def read_data(filename):
    with open(filename) as f:
        data = f.read().split(',')
    return data


data = read_data(FILENAME)

sum = 0
for d in data:
    sum += hash(d)

print(sum)

# Second part
HASH_MAP = {i: [] for i in range(256)}
HASH_LENSES = {i: [] for i in range(256)}


def hash_map(string):
    if '-' in string:
        label = string[:-1]
        hash_val = hash(label)
        if label in HASH_MAP[hash_val]:
            index = HASH_MAP[hash_val].index(label)
            HASH_MAP[hash_val].pop(index)
            HASH_LENSES[hash_val].pop(index)
    elif '=' in string:
        label, focal_length = string.split('=')
        focal_length = int(focal_length)
        hash_val = hash(label)
        if label in HASH_MAP[hash_val]:
            index = HASH_MAP[hash_val].index(label)
            HASH_LENSES[hash_val][index] = focal_length
        else:
            HASH_MAP[hash_val].append(label)
            HASH_LENSES[hash_val].append(focal_length)


for d in data:
    hash_map(d)

sums = 0

for i in range(256):
    for j, focal_length in enumerate(HASH_LENSES[i]):
        sums += (i+1)*(j+1) * focal_length

print(sums)
