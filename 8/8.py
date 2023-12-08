import numpy as np
FILENAME = '8.txt'


class Node:
    def __init__(self, name, L=None, R=None):
        self.name = name
        self.L = L
        self.R = R

    def step(self, step_str):
        if step_str == 'L':
            return self.L
        elif step_str == 'R':
            return self.R
        else:
            return self

    def __repr__(self):
        return self.name


def read_data(filename):
    node_dict = dict()
    steps = None
    with open(filename) as f:
        # Create nodes without filling the L,R values
        steps = f.readline().strip()
        f.readline()
        for line in f:
            node_name, lr = line.split('=')
            node_name = node_name.replace(' ', '')
            lr = lr.replace(' ', '').replace(')', '').replace(
                '(', '').replace('\n', '')
            node_dict[node_name] = dict()
            node_dict[node_name]['node'] = Node(node_name)
            l, r = lr.split(',')
            node_dict[node_name]['L'] = l
            node_dict[node_name]['R'] = r
    for node in node_dict:
        node_dict[node]['node'].L = node_dict[node_dict[node]['L']]['node']
        node_dict[node]['node'].R = node_dict[node_dict[node]['R']]['node']
    return node_dict, steps


# First part

node_dict, steps = read_data(FILENAME)
node = node_dict['AAA']['node']
steps_taken = 0
while node != node_dict['ZZZ']['node']:
    for s in steps:
        node = node.step(s)
        steps_taken += 1
        if node == node_dict['ZZZ']['node']:
            break
print(steps_taken)

# Second part


def nodes_finished(nodes):
    nodes_end_Z = [node for node in nodes if node.name[-1] == 'Z']
    return len(nodes_end_Z) == len(nodes)


start_node_names = filter(lambda x: x[-1] == 'A', node_dict.keys())
nodes = [node_dict[n]['node'] for n in start_node_names]
end_node_names = filter(lambda x: x[-1] == 'Z', node_dict.keys())
end_nodes = [node_dict[n]['node'] for n in end_node_names]
steps_all = []
for n in nodes:
    steps_taken = 0
    while n not in end_nodes:
        for s in steps:
            n = n.step(s)
            steps_taken += 1
            if n in end_nodes:
                break
    steps_all.append(steps_taken)

print(steps_all)


print(np.lcm.reduce(steps_all))

steps_all = []
for n in end_nodes:
    steps_taken = 0
    first = True
    while n not in end_nodes or first:
        first = False
        for s in steps:
            n = n.step(s)
            steps_taken += 1
            if n in end_nodes:
                break
    steps_all.append(steps_taken)

print(steps_all)

print(np.lcm.reduce(steps_all))
