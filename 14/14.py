import numpy as np

FILENAME = '14.txt'


def read_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            d = np.array(list(map(int, list(line.strip().replace(
                '.', '0').replace('#', '2').replace('O', '1')))))
            d[d == 2] = -1
            data.append(d)

    return np.vstack(data)


def push_north(data):
    data = data.T
    for idx in range(data.shape[0]):
        empty_space_run = 0
        for jdx in range(data.shape[1]):
            if data[idx][jdx] == 0:
                empty_space_run += 1
            elif data[idx][jdx] == 1 and empty_space_run > 0:
                data[idx, jdx-empty_space_run] = 1
                data[idx, jdx] = 0
            else:
                empty_space_run = 0
    return data.T


def push_west(data):
    return push_north(data.T).T


def push_east(data):
    return np.flip(push_west(np.flip(data)))


def push_south(data):
    return np.flipud(push_north(np.flipud(data)))


data = read_data(FILENAME)
data_new = push_north(data)

mask = np.tile(np.arange(data_new.shape[0], 0, -1),
               data_new.shape[1]).reshape(data_new.shape).T

data_new[data_new == -1] = 0
print((data_new*mask).sum())

# Second part


def push_west(data):
    return push_north(data.T).T


def push_east(data):
    return np.flip(push_west(np.flip(data)))


def push_south(data):
    return np.flipud(push_north(np.flipud(data)))


def cycle(data):
    return (push_east(push_south(push_west(push_north(data)))))


data = read_data(FILENAME)
mask = np.tile(np.arange(data.shape[0], 0, -1),
               data.shape[1]).reshape(data.shape).T

# Sample 500 of times
sums = np.zeros(500)
for i in range(500):
    data = cycle(data)
    data_n = data.copy()
    data_n[data_n == -1] = 0
    sums[i] = (data_n*mask).sum()


def find_period(sums, period_start=1):
    for i in range(1, len(sums)//2):
        sums_left = sums[period_start:i+period_start]
        sums_right = sums[period_start+i:period_start+2*i]
        if len(sums_left) != len(sums_right):
            continue
        if np.all(sums[period_start:i+period_start] == sums[period_start+i:period_start+2*i]):
            period_found = True
            for j in range(0, (len(sums)-period_start)//i):
                sums_left = sums[period_start+i*j:period_start+i*(j+1)]
                sums_right = sums[period_start+i*(j+1):period_start+i*(j+2)]
                if len(sums_left) != len(sums_right):
                    continue
                if not np.all(sums[period_start+i*j:period_start+i*(j+1)] == sums[period_start+i*(j+1):period_start+i*(j+2)]):
                    period_found = False
                    break
            if period_found:
                return i


# Find number bigger than period start by hand or by bruteforcing through numbers. Save guess is half of your samples
# (supposed that you have enough samples and period is not bigger than half of half)

period_start = len(sums)//2
period = find_period(sums, period_start)
period_nums = sums[period_start:period+period_start]
period_num = 1000000000 - period_start-1
print(int(period_nums[period_num % (period)]))
