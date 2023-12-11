from scipy.spatial.distance import cityblock
import numpy as np
from itertools import combinations


FILENAME_TEST = '11_test.txt'
FILENAME_TEST_EXPANSION = '11_test_expansion.txt'
FILENAME = '11.txt'

def read_file(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(np.array(list(line.strip().replace('.','0').replace('#','1'))).astype(int))
    return np.vstack(lines)

def expand_lines(star_map):
    new_lines = []
    for line in star_map:
        if line.any():
            new_lines.append(line)
        else:
            new_lines.append(line)
            new_lines.append(line)
    return np.vstack(new_lines)


def expand(star_map):
    expanded = expand_lines(star_map)
    expanded = expand_lines(expanded.T)
    expanded = expanded.T
    return expanded


def calculate_distances(expanded_map):
    locations = np.argwhere(expanded_map==1)
    locations_index = np.arange(len(locations))
    locations_distance = {loc:10000000000 for loc in locations_index}
    for comb in combinations(locations_index,2):
        a,b = comb
        distance = cityblock(locations[a],locations[b])
        if locations_distance[a]> distance:
            locations_distance[a] = distance
        if locations_distance[b]> distance:
            locations_distance[b] = distance
    print(locations_distance)
            
def calculate_distances(expanded_map):
    locations = np.argwhere(expanded_map==1)
    locations_index = np.arange(len(locations))
    locations_distance = dict()
    for comb in combinations(locations_index,2):
        a,b = comb
        distance = cityblock(locations[a],locations[b])
        locations_distance[(a,b)]=distance
    return(locations_distance)

            

test_file = read_file(FILENAME_TEST)


test_expansion = read_file(FILENAME_TEST_EXPANSION)
expanded = expand(test_file)
# Test if expansion is working
print((test_expansion == expanded).all())

distances = calculate_distances(expanded)
distances_sum = 0
for k,v in distances.items():
    distances_sum += v
print(distances_sum)
# First part
input_map = read_file(FILENAME)
expanded = expand(input_map)
distances = calculate_distances(expanded)
distances_sum = 0
for k,v in distances.items():
    distances_sum += v
print(distances_sum)

# Second part

def calculate_distances_multiplier(non_expanded_map, multiplier=1):
    locations = np.argwhere(non_expanded_map==1)
    locations_index = np.arange(len(locations))
    locations_distance = dict()
    for comb in combinations(locations_index,2):
        a,b = locations[comb[0]], locations[comb[1]]
        dis_height = np.abs(a[0]-b[0])
        dis_width = np.abs(a[1]-b[1])
        if a[0] < b[0]:
            start_h = a[0]
        else:
            start_h = b[0]
        if a[1] < b[1]:
            start_w = a[1]
        else:
            start_w = b[1]
        for h in range(start_h, start_h+dis_height):
            if not non_expanded_map[h,:].any():
                dis_height= dis_height -1 + multiplier
        for w in range(start_w, start_w+dis_width):
            if not non_expanded_map[:,w].any():
                dis_width= dis_width -1 + multiplier
        distance = dis_height + dis_width
        locations_distance[comb]=distance
    return(locations_distance)

distances = calculate_distances_multiplier(input_map,1000000)
distances_sum = 0
for k,v in distances.items():
    distances_sum += v
print(distances_sum)


