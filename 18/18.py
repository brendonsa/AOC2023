import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm

FILENAME = '18.txt'


def read_data(filename):
    moves = []
    steps = []
    colors = []
    with open(filename, 'r') as f:
        for line in f:
            move, step, color = line.strip().split(' ')
            step = int(step)
            moves.append(move)
            steps.append(step)
            colors.append(color)
    return moves, steps, colors


def prep_np(moves, steps):
    current_horizontal = 1
    current_vertical = 1
    max_r = 0
    max_l = 0
    max_up = 0
    max_down = 0
    for s, m in zip(steps, moves):
        match s:
            case 'R':
                current_horizontal += m
                if current_horizontal > max_r:
                    max_r = current_horizontal
            case 'L':
                current_horizontal -= m
                if current_horizontal < 0 and abs(current_horizontal) > max_l:
                    max_l = abs(current_horizontal)
            case 'U':
                current_vertical -= m
                if current_vertical < 0 and abs(current_vertical) > max_up:
                    max_up = abs(current_vertical)
            case 'D':
                current_vertical += m
                if current_vertical > max_down:
                    max_down = current_vertical
    # Returns bigger array than needed, just to skip the start point search. Start point should be max_left and max_down. The dig function will adjust for this
    # At the time I could not care about making dimensions too big, because I was sure, that I wouldnt need doing this in second part.
    start_point = np.array([max_l, max_down])
    return np.zeros((2*(max_down+max_up), 2*(max_r+max_l))), start_point


def cut(array):
    non_zero_rows = np.any(array != 0, axis=1)
    non_zero_columns = np.any(array != 0, axis=0)
    result_matrix = array[non_zero_rows][:, non_zero_columns]
    return result_matrix


def dig(moves, steps, array, start_point):
    array = array.copy()
    curr_h = start_point[0]+int(array.shape[0] * 0.05)
    curr_v = start_point[1]+int(array.shape[1] * 0.05)
    for s, m in zip(steps, moves):
        match s:
            case 'R':
                array[curr_v, curr_h:curr_h+m+1] = 1
                curr_h += m
            case 'L':
                array[curr_v, curr_h-m:curr_h] = 1
                curr_h -= m
            case 'U':
                array[curr_v-m:curr_v, curr_h] = 1
                curr_v -= m
            case 'D':
                array[curr_v:curr_v+m+1, curr_h] = 1
                curr_v += m
    return cut(array)


NEIGHBORS = ((0, 1), (0, -1), (-1, 0), (1, 0))


def fill(array):
    for idx in range(0, array.shape[0]-1):
        inside = False
        on_line = False
        for jdx in range(0, array.shape[1]-1):
            if inside:
                if array[idx, jdx] == 1:
                    inside = False
                else:
                    array[idx, jdx] = 1
                    continue
            else:
                if array[idx, jdx] == 1 and array[idx, jdx+1] == 0 and not on_line:
                    inside = True
            if on_line:
                if array[idx, jdx+1] == 0:
                    on_line = False
                    if array[idx-1, jdx] and array[idx-1, jdx+1] == 1:
                        inside = True
            else:
                if array[idx, jdx] == 1 and array[idx, jdx+1] == 1:
                    on_line = True
    return array


moves, steps, colors = read_data(FILENAME)
array, start_point = prep_np(steps, moves)
dig_array = dig(steps, moves, array, start_point)
a = dig_array.sum()
plt.imsave('prefill.png', np.array(dig_array), cmap=cm.gray)

fill(dig_array)
print(int(dig_array.sum()))

plt.imsave('fill.png', np.array(dig_array), cmap=cm.gray)


def polygon_area(x, y):
    n = len(x)

    if len(y) != n:
        raise ValueError("Number of x and y coordinates must be equal.")

    # Apply the Shoelace Formula
    area = 0.5 * abs(sum(x[i] * y[(i + 1) % n] -
                     x[(i + 1) % n] * y[i] for i in range(n)))

    return area


MOVES = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}


def colors_to_moves(colors):
    moves, steps = [], []
    for c in colors:
        hex_str = c[2:-2]
        moves.append(MOVES[c[-2]])
        steps.append(int(hex_str, 16))
    return moves, steps


def get_coordinates2(moves, steps):
    current_horizontal = 0
    current_vertical = 0
    x, y = [], []
    for idx, (s, m) in enumerate(zip(steps, moves)):
        if idx == len(steps)-1:
            steps_next = steps[0]
        else:
            steps_next = steps[idx+1]
        match s:
            case 'R':
                current_horizontal += m
                if steps_next == 'U':
                    x.append(current_horizontal+1)
                    y.append(current_vertical-1)
                if steps_next == 'D':
                    x.append(current_horizontal+1)
                    y.append(current_vertical+1)
            case 'L':
                current_horizontal -= m
                x.append(current_horizontal)
                y.append(current_vertical)
                if steps_next == 'U':
                    x.append(current_horizontal-1)
                    y.append(current_vertical-1)
                if steps_next == 'D':
                    x.append(current_horizontal-1)
                    y.append(current_vertical+1)
            case 'U':
                current_vertical += m
                if steps_next == 'R':
                    x.append(current_horizontal-1)
                    y.append(current_vertical+1)
                if steps_next == 'L':
                    x.append(current_horizontal+1)
                    y.append(current_vertical+1)
            case 'D':
                current_vertical -= m
                if steps_next == 'R':
                    x.append(current_horizontal-1)
                    y.append(current_vertical-1)
                if steps_next == 'L':
                    x.append(current_horizontal+1)
                    y.append(current_vertical-1)
    return x, y


def get_coordinates(steps, moves):
    current_horizontal = 0
    current_vertical = 0
    x, y = [], []
    for idx, (s, m) in enumerate(zip(steps, moves)):
        match m:
            case 'R':
                current_horizontal += s
            case 'L':
                current_horizontal -= s
            case 'U':
                current_vertical += s
            case 'D':
                current_vertical -= s
        x.append(current_horizontal)
        y.append(current_vertical)
    return x, y


moves, steps = colors_to_moves(colors)
x, y = get_coordinates(steps, moves)
area = polygon_area(x, y)

print(f"The area of the polygon is: {int(area + sum(steps)//2+1)}")
