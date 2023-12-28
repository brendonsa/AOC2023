import numpy as np

FILENAME = "16.txt"

class Orientation:
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3   

class EnergyField:
    def __init__(self, shape):
        self.energy_field = np.zeros(shape, dtype=bool)
    
    def energize(self, laser):
        a, b  = laser.position
        if (a >= 0 and a <self.energy_field.shape[0]) and (b >= 0 and b < self.energy_field.shape[1]):
            self.energy_field[a][b] = True
            
    def reset(self):
        self.energy_field = np.zeros_like(self.energy_field)


def file_read(filename):
    data = []
    with open(filename,'r') as f:
        for line in f:
            data.append(list(line.strip()))
    return data

# Solution uses too many global fields, but IDC
CONTRAPTION_MAP = file_read(FILENAME)
ENERGY_FIELD = EnergyField((len(CONTRAPTION_MAP),len(CONTRAPTION_MAP[1])))
POS_ORIENTATIONS = dict()



class Laser:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation
        self.lasers = []
        ENERGY_FIELD.energize(self)

        if self.position in POS_ORIENTATIONS:
            if self.orientation in POS_ORIENTATIONS[self.position]:
                self.this_stopped = True
            else:
                POS_ORIENTATIONS[self.position].append(self.orientation)
                self.this_stopped = False
        else:
            POS_ORIENTATIONS[self.position] = [self.orientation]
            self.this_stopped = False
        
    @property
    def stopped(self):
        if len(self.lasers) == 0 :
            return self.this_stopped
        else:
            return all([laser.stopped for laser in self.lasers]) and self.this_stopped
        
    def down(self, symbol):
        match symbol:
            case '\\':
                self.orientation = Orientation.RIGHT
            case '/':
                self.orientation = Orientation.LEFT
            case '|':
                pass
            case '-':
                self.orientation = Orientation.LEFT
                self.lasers.append(Laser(self.position, Orientation.RIGHT))
            case '.':
                pass
    
    def up(self, symbol):
        match symbol:
            case '\\':
                self.orientation = Orientation.LEFT
            case '/':
                self.orientation = Orientation.RIGHT
            case '|':
                pass
            case '-':
                self.orientation = Orientation.LEFT
                self.lasers.append(Laser(self.position, Orientation.RIGHT))
            case '.':
                pass
    
    def left(self, symbol):
        match symbol:
            case '\\':
                self.orientation = Orientation.UP
            case '/':
                self.orientation = Orientation.DOWN
            case '|':
                self.orientation = Orientation.DOWN
                self.lasers.append(Laser(self.position, Orientation.UP))
            case '-':
                pass
            case '.':
                pass
    
    def right(self, symbol):
        match symbol:
            case '\\':
                self.orientation = Orientation.DOWN
            case '/':
                self.orientation = Orientation.UP
            case '|':
                self.orientation = Orientation.DOWN
                self.lasers.append(Laser(self.position, Orientation.UP))
            case '-':
                pass
            case '.':
                pass
    
    def change_direction(self, symbol):
        match self.orientation:
            case Orientation.UP:
                self.up(symbol)
                
            case Orientation.DOWN:
                self.down(symbol)
            
            case Orientation.LEFT:
                self.left(symbol)
                
            case Orientation.RIGHT:
                self.right(symbol)
    
    def check_repetition(self):
        if self.orientation in POS_ORIENTATIONS.get(self.position,[]):
            self.this_stopped = True
        else:
            if self.position in POS_ORIENTATIONS:
                POS_ORIENTATIONS[self.position].append(self.orientation)
            else:
                POS_ORIENTATIONS[self.position] = [self.orientation]
    
    def step(self):
        if self.this_stopped:
            for laser in self.lasers:
                laser.step()
            return
        ENERGY_FIELD.energize(self)
        a,b = self.position
        match self.orientation:
            case Orientation.RIGHT:
                self.position = (a,b+1)
            case Orientation.LEFT :
                self.position = (a,b-1)
            case Orientation.UP:
                self.position = (a-1,b)
            case Orientation.DOWN:
                self.position = (a+1,b)
        a,b = self.position
        ENERGY_FIELD.energize(self)
        if a<0 or a>= ENERGY_FIELD.energy_field.shape[0]:
            self.this_stopped = True
        elif b < 0 or b >= ENERGY_FIELD.energy_field.shape[1]:
            self.this_stopped = True
        else:
            for laser in self.lasers:
                laser.step()
            new_symbol = CONTRAPTION_MAP[a][b]
            self.change_direction(new_symbol)
            self.check_repetition()
            


laser = Laser((0,-1),Orientation.RIGHT)
while not laser.stopped:
    laser.step()

print(ENERGY_FIELD.energy_field)
print(ENERGY_FIELD.energy_field.sum())


# Second part

best_energy = 0
# Try starting from left side
for i in range(ENERGY_FIELD.energy_field.shape[0]):
    laser = Laser((i,-1),Orientation.RIGHT)
    while not laser.stopped:
        laser.step()
    sum_field = ENERGY_FIELD.energy_field.sum()
    if sum_field > best_energy:
        best_energy = sum_field
    ENERGY_FIELD.reset()
    POS_ORIENTATIONS.clear()
    
# Now right
for i in range(ENERGY_FIELD.energy_field.shape[0]):
    laser = Laser((i,ENERGY_FIELD.energy_field.shape[1]),Orientation.LEFT)
    while not laser.stopped:
        laser.step()
    sum_field = ENERGY_FIELD.energy_field.sum()
    if sum_field > best_energy:
        best_energy = sum_field
    ENERGY_FIELD.reset()
    POS_ORIENTATIONS.clear()
        

# Now UP
for i in range(ENERGY_FIELD.energy_field.shape[1]):
    laser = Laser((-1,i),Orientation.DOWN)
    while not laser.stopped:
        laser.step()
    sum_field = ENERGY_FIELD.energy_field.sum()
    if sum_field > best_energy:
        best_energy = sum_field
    ENERGY_FIELD.reset()
    POS_ORIENTATIONS.clear()        
    
# Now DOWN
for i in range(ENERGY_FIELD.energy_field.shape[1]):
    laser = Laser((ENERGY_FIELD.energy_field.shape[0],i),Orientation.UP)
    while not laser.stopped:
        laser.step()
    sum_field = ENERGY_FIELD.energy_field.sum()
    if sum_field > best_energy:
        best_energy = sum_field
    ENERGY_FIELD.reset()
    POS_ORIENTATIONS.clear()        


print(best_energy)
                 

