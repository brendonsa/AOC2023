import numpy as np

FILENAME = '9.txt'

def read_data(filename):
    inputs = []
    with open(FILENAME, 'r') as f:
        for line in f:
            inputs.append(np.fromstring(line, sep=' ', dtype=np.int64))
    
    return np.vstack(inputs)


arrays = read_data(FILENAME)

# First part
inferred_values_all = []
for a in arrays:
    diff = np.diff(a)
    diffs = [diff]
    while(diff.any()):
        diff = np.diff(diffs[-1])
        diffs.append(diff)
    inferred_values = [0]
    for idx in range(len(diffs)-2,-1,-1):
        inferred_values.append(inferred_values[-1]+diffs[idx][-1])
    inferred_values.append(a[-1]+inferred_values[-1])
    inferred_values_all.append(inferred_values)

print(sum([a[-1] for a in inferred_values_all]))


# Second part

inferred_values_all = []
for a in arrays:
    a = a[::-1]
    diff = np.diff(a)
    diffs = [diff]
    while(diff.any()):
        diff = np.diff(diffs[-1])
        diffs.append(diff)
    inferred_values = [0]
    for idx in range(len(diffs)-2,-1,-1):
        inferred_values.append(inferred_values[-1]+diffs[idx][-1])
    inferred_values.append(a[-1]+inferred_values[-1])
    inferred_values_all.append(inferred_values)

print(sum([a[-1] for a in inferred_values_all]))


