from functools import reduce

FILENAME = '6.txt'


def read_data(fname: str):
    with open(fname, 'r') as f:
        contents = f.read()
    time, distance = contents.split('\n')
    time = time.split(':')[1].split()
    # Map time to int
    time = [int(x) for x in time]
    distance = distance.split(':')[1].split()
    distance = [int(x) for x in distance]
    return time, distance


def read_data2(fname: str):
    with open(fname, 'r') as f:
        contents = f.read()
    time, distance = contents.split('\n')
    time = time.split(':')[1].replace(' ', '')
    # Map time to int
    time = int(time)
    distance = distance.split(':')[1].replace(' ', '')
    distance = int(distance)
    return time, distance


def count_distance(speed, time):
    return speed * time


def hold_button(time):
    distance_traveled = []
    for t in range(time+1):
        speed = t
        remaining_time = time-t
        distance_traveled.append(count_distance(speed, remaining_time))
    return distance_traveled


def hold_until_win(time, distance):
    for t in range(time+1):
        speed = t
        remaining_time = time-t
        if (count_distance(speed, remaining_time)) > distance:
            return t
    return time


def filter_faster(times, distances):
    ways_of_winning = []
    for t, d in zip(times, distances):
        distances = hold_button(t)
        ways_of_winning.append(list(filter(lambda x: x > d, distances)))
    return ways_of_winning


# First part
times, distances = read_data(FILENAME)
ff = filter_faster(times, distances)
margin_of_error = reduce(lambda x, y: x*y, [len(f) for f in ff])
print(margin_of_error)

# Second part
time, distance = read_data2(FILENAME)
print(time+1-2*hold_until_win(time, distance))
