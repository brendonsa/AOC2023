import numpy as np
from numba import njit
from multiprocessing import Pool


@njit
def traverse(maps, seed):
    current_val = seed
    for m in maps:
        # find if value is in range of any given maps
        for x in range(0, m.shape[1], 2):
            if current_val >= m[0, x] and current_val <= m[0, x+1]:
                current_val = m[1, x] + np.fabs(m[0, x] - current_val)
                break
    return current_val


@njit
def calc(maps, locs, start, end):
    print(f"calulating seeds {start} - {end}")
    for y in np.arange(start, end):
        vals = traverse(maps, y)
        if vals < locs:  # update the minimum
            locs = vals
    print("min loc ", locs)
    return locs


seeds = np.loadtxt('5_seeds.txt').astype(int)
sts = np.loadtxt('5_seed_to_soil.txt').astype(int)
stf = np.loadtxt('5_soil_to_fertilizer').astype(int)
ftw = np.loadtxt('5_fertilizer_to_water.txt').astype(int)
wtl = np.loadtxt('5_water_to_light.txt').astype(int)

ltt = np.loadtxt('5_light_to_temperature.txt').astype(int)
tth = np.loadtxt('5_temperature_to_humidity.txt').astype(int)
htl = np.loadtxt('5_humidity_to_location.txt').astype(int)
seeds_range = []
for i in range(len(seeds)//2):
    seeds_range.append([seeds[i*2], seeds[i*2+1]])
seeds_range = np.array(seeds_range).astype(int)

maps = [sts, stf, ftw, wtl, ltt, tth, htl]


def parse_maps(maps):
    maps_new = []
    for ranges in maps:
        arr = None
        for line in ranges:
            if arr is None:
                arr = np.array([[line[1], line[1] + line[2] - 1],
                               [line[0], line[0] + line[2] - 1]])
            else:
                arr = np.append(arr, np.array(
                    [[line[1], line[1] + line[2] - 1], [line[0], line[0] + line[2] - 1]]), axis=1)
        maps_new.append(arr)
    return maps_new


new_maps = parse_maps(maps)
locs = new_maps[-1].max()
pool = Pool(processes=10)
for i in range(0, len(seeds), 2):
    res = pool.apply_async(calc, args=(
        new_maps, locs, seeds[i], (seeds[i] + seeds[i+1])))
pool.close()
pool.join()
