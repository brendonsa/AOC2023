from enum import Enum
import numpy as np

FILENAME = '10.txt'

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    
    
def north(symbol):
    match symbol:
        case '|':
            return Direction.NORTH
        case 'F':
            return Direction.EAST
        case '7':
            return Direction.WEST

def south(symbol):
    match symbol:
        case '|':
            return Direction.SOUTH
        case 'J':
            return Direction.WEST
        case 'L':
            return Direction.EAST

def east(symbol):
    match symbol:
        case '-':
            return Direction.EAST
        case 'J':
            return Direction.NORTH
        case '7':
            return Direction.SOUTH

def west(symbol):
    match symbol:
        case '-':
            return Direction.WEST
        case 'F':
            return Direction.SOUTH
        case 'L':
            return Direction.NORTH
    


class Pipes:
    def __init__(self, filename:str):
        self.facing = None
        self.map = self.parse_map(filename)
        self.starting_point = np.argwhere(self.map=='S')[0]
        self.init_facing()
        self.loop = self.find_loop()
        
    def parse_map(self, filename:str):
        lines = []
        with open(filename,'r') as f:
            for idx,line in enumerate(f):
                lines.append(np.array(list(line.strip())))
        return np.vstack(lines)
    
    def init_facing(self):
        line_idx, symbol_idx = self.starting_point
        if line_idx > 0:
            if self.map[line_idx-1,symbol_idx] in ['|','7','F']:
                self.facing =  Direction.NORTH
                return
        if line_idx < self.map.shape[0]-1:
            if self.map[line_idx+1,symbol_idx] in ['|','J','L']:
                self.facing =  Direction.SOUTH
                return
        if symbol_idx > 0:
            if self.map[line_idx,symbol_idx-1] in ['-','L','F']:
                self.facing =  Direction.WEST
                return
            
        self.facing = Direction.EAST
        return
        # Three checks is enough
        
    def step(self, curr):
        match self.facing:
            case Direction.NORTH:
                new_location = (curr[0]-1, curr[1])
                self.facing = north(self.map[new_location])
                return new_location
            case Direction.SOUTH:
                new_location = (curr[0]+1, curr[1])
                self.facing = south(self.map[new_location])
                return new_location
            case Direction.EAST:
                new_location = (curr[0], curr[1]+1)
                self.facing = east(self.map[new_location])
                return new_location
            case Direction.WEST:
                new_location = (curr[0], curr[1]-1)
                self.facing = west(self.map[new_location])
                return new_location
        
                
        
    
    def find_loop(self):
        start = tuple(self.starting_point)
        loop = [start]
        curr = tuple(self.starting_point)
        first = True
        while (curr!=start) or first:
            first = False
            curr = self.step(curr)
            if (curr!=start):
                loop.append(curr)
                
        return loop
            
        
    
pipes = Pipes(FILENAME)
print(len(pipes.loop)//2)

# Second part

for i in range(pipes.map.shape[0]):
    for j in range(pipes.map.shape[1]):
        if (i,j) not in pipes.loop:
            pipes.map[i,j] = '.'
            
            
            
to_bitmap = {
    '-': np.array([[0,0,0],[1,1,1],[0,0,0]]),
    '.': np.array([[0,0,0],[0,0,0],[0,0,0]]),
    '|': np.array([[0,1,0],[0,1,0],[0,1,0]]),
    '7': np.array([[0,0,0],[1,1,0],[0,1,0]]),
    'L': np.array([[0,1,0],[0,1,1],[0,0,0]]),
    'J': np.array([[0,1,0],[1,1,0],[0,0,0]]),
    'F': np.array([[0,0,0],[0,1,1],[0,1,0]]),
    'S': np.array([[0,1,0],[1,1,1],[0,1,0]]),
}

new_map = np.zeros((pipes.map.shape[0]*3,pipes.map.shape[1]*3), dtype=int) # Draw a map by mapping the pipes to 3x3
new_map_fill = np.zeros((pipes.map.shape[0]*3,pipes.map.shape[1]*3), dtype=int) # Draw a map by filling 3x3 where pipe is
for i in range(pipes.map.shape[0]):
    for j in range(pipes.map.shape[1]):
        new_map[i*3:(i+1)*3,j*3:(j+1)*3] = to_bitmap[pipes.map[i,j]]
        if pipes.map[i,j] in ['-','|','7','L','J','F','S']:
            new_map_fill[i*3:(i+1)*3,j*3:(j+1)*3] = np.array([[1,1,1],[1,1,1],[1,1,1]])

# For checking the pipelines
from matplotlib import image as mpimg
mpimg.imsave('output_image.png', new_map, cmap='gray')

INITIAL_POINT = (0,0)

point_list = [INITIAL_POINT]

while len(point_list)!=0:
    point = point_list.pop()
    new_map[point] = 1
    if point[0] > 0:
        new_point = (point[0]-1,point[1])
        if new_map[new_point] == 0:
            point_list.append(new_point)
    if point[0] < new_map.shape[0]-1:
        new_point = (point[0]+1,point[1])
        if new_map[new_point] == 0:
            point_list.append(new_point)
    if point[1] > 0:
        new_point = (point[0],point[1]-1)
        if new_map[new_point] == 0:
            point_list.append(new_point)
    if point[1] < new_map.shape[1]-1:
        new_point = (point[0],point[1]+1)
        if new_map[new_point] == 0:
            point_list.append(new_point)

mpimg.imsave('output_image2.png', new_map, cmap='gray')
final_map = new_map | new_map_fill
final_map = final_map.astype(bool)

mpimg.imsave('output_image3.png', final_map, cmap='gray')
print((~final_map).sum()//9)
    
        
    



        
# Praplėsti lygiagrečias juostas, jei jungias galai sujungt, jei nesijungia dėt . po to paimt pirmą išorinį ir sužymėt nuo jo visus įmanomus išorinius.
    