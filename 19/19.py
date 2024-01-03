import re
import numpy as np
import copy

RULES_FILE = '19_rules.txt'
PART_FILE = '19_parts.txt'


class Part:
    def __init__(self, x, m, a, s):
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)

    def rating(self):
        return self.x + self.m + self.a + self.s

    def __repr__(self):
        return f'Part(x={self.x}, m={self.m}, a={self.a}, s={self.s})'


class Rule:
    def __init__(self, part_name, rule, number, res):
        self.part_name = part_name
        self.rule = rule
        self.number = int(number)
        self.res = res

    def filter_follows_rule(self, xmas):
        xmas = copy.deepcopy(xmas)
        if self.rule == '>':
            xmas[self.part_name] = xmas[self.part_name][np.where(
                xmas[self.part_name] > self.number)]
        else:
            xmas[self.part_name] = xmas[self.part_name][np.where(
                xmas[self.part_name] < self.number)]
        return xmas

    def filter_does_not_follow_rule(self, xmas):
        xmas = copy.deepcopy(xmas)
        if self.rule == '>':
            xmas[self.part_name] = xmas[self.part_name][np.where(
                xmas[self.part_name] <= self.number)]
        else:
            xmas[self.part_name] = xmas[self.part_name][np.where(
                xmas[self.part_name] >= self.number)]
        return xmas

    def __call__(self, part):
        if self.rule == '>':
            return getattr(part, self.part_name) > self.number
        else:
            return getattr(part, self.part_name) < self.number

    def __str__(self):
        return f'{self.part_name}{self.rule}{self.number} -> {self.res}'

    def __repr__(self):
        return str(self)


class Workflow:
    def __init__(self, rules, default):
        self.rules = rules
        self.default = default

    def __call__(self, part):
        for rule in self.rules:
            if rule(part):
                return rule.res
        return self.default

    def __str__(self) -> str:
        string = ''
        for rule in self.rules:
            string += str(rule) + '\n'
        return f'{string}default:{self.default}'

    def __repr__(self):
        return str(self)


def read_parts(filename):
    parts = []

    with open(filename, 'r') as f:
        for line in f:
            matches = re.findall(r'(\w+)=(\d+)', line.strip())
            result_dict = dict(matches)
            parts.append(Part(**result_dict))
    return parts


def read_workflows(filename):
    workflows = dict()
    pattern = re.compile(r'([^{<>,]+)([<>,])(\d+):([^{},]+)')
    with open(filename, 'r') as f:
        for line in f:
            matches = pattern.findall(line.strip())
            before_brace_match = re.match(r'([^{\n]+){', line)
            before_brace = before_brace_match.group(
                1) if before_brace_match else ""

            rules = []
            for m in matches:
                rules.append(Rule(m[0], m[1], int(m[2]), m[3]))
            last_part_match = re.search(r',([^,]+)\}', line.strip())
            last_part = last_part_match.group(1) if last_part_match else ""

            workflows[before_brace] = Workflow(rules, last_part)
    return workflows


parts, workflows = read_parts(PART_FILE), read_workflows(RULES_FILE)
results = []

for p in parts:
    res = 'in'
    while res in workflows:
        res = workflows[res](p)

    if res == 'A':
        results.append(p)

# first part
print(sum([p.rating() for p in results]))

# second part


def any_empty(xmas):
    return any([len(a) == 0 for a in xmas.values()])


def report_branch_call(branch_name, xmas):
    print('-------------')
    print(branch_name)
    print('x: ', min(xmas['x']), max(xmas['x']))
    print('m: ', min(xmas['m']), max(xmas['m']))
    print('a: ', min(xmas['a']), max(xmas['a']))
    print('s: ', min(xmas['s']), max(xmas['s']))
    print('-------------')


def analyze_branch(branch, xmas, branch_name='default'):
    # report_branch_call(branch_name, xmas)
    accepted_count = 0
    xmas = copy.deepcopy(xmas)
    for rule in branch.rules:
        new_xmas = rule.filter_follows_rule(xmas)
        if rule.res == 'A':
            res = 1
            for _, v in new_xmas.items():
                res = res * len(v)
            accepted_count += res
        elif rule.res == 'R':
            pass
        elif not any_empty(new_xmas):
            accepted_count += analyze_branch(
                workflows[rule.res], new_xmas, branch_name=rule.res)
        xmas = rule.filter_does_not_follow_rule(xmas)

    if branch.default == 'A':
        res = 1
        for _, v in xmas.items():
            res = res * len(v)
        accepted_count += res
    elif branch.default == 'R':
        pass
    else:
        accepted_count += analyze_branch(
            workflows[branch.default], xmas, branch.default)
    return accepted_count


x = np.arange(1, 4001)
m = np.arange(1, 4001)
a = np.arange(1, 4001)
s = np.arange(1, 4001)

xmas = {'x': x, 'm': m, 'a': a, 's': s}

# analyze_branch(workflows['in'], xmas)
accepted = analyze_branch(workflows['in'], xmas, 'in')
print(accepted)
