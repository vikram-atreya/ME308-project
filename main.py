import random
from pulp import *

class Container:
    def __init__(self, weight, l_port, d_port, refrig, toxic):
        self.weight = weight
        self.l_port = l_port
        self.d_port = d_port
        self.refrig = refrig
        self.toxic = toxic

class Ship:
    def __init__(self, length, breadth, width, bays, stacks, tiers, ref_bays, x_cg_tol, y_cg_tol):
        self.length = length
        self.breadth = breadth
        self.width = width
        self.bays = bays
        self.stacks = stacks
        self.tiers = tiers
        self.ref_bays = ref_bays #will be a list of ref bay numbers
        self.x_cg_tol = x_cg_tol
        self.y_cg_tol = y_cg_tol

bays = 1
stacks = 1000
tiers = 1000

stow = [[[0 for k in range(bays)] for j in range(stacks)] for i in range(tiers)]

n_port = 10
n_cont = 0
conts = []

'''
for i in range(n_cont):
    l_port = random.randint(1,n_port-1)
    d_port = random.randint(2,n_port)
    refrig = random.randint(0,1)
    toxic  = random.randint(0,1)
    test_cont = Container(l_port, d_port, refrig, toxic)
    conts.append(test_cont)
'''


T = []
for i in range(n_port):
    temp_list = []
    for j in range(n_port):
        if j>i:
            t_no = random.randint(0,5)
            n_cont += t_no
            temp_list.append(t_no)
        else:
            temp_list.append(0)
    T.append(temp_list)

print(T)

prob = LpProblem("Stowage",LpMinimize)

#prob += lpSum([[T[i][j] for i in n_port] for j in n_port]) <= stacks*tiers
x = {}
y = {}
for i in range(n_port):
    for j in range(n_cont):
        for s in range(stacks):
            for t in range(tiers):
                lowerBound = 0
                upperBound = 1
                if i == n_port-1:
                    upperBound = 0
                x[i,j] = pulp.LpVariable('x' + str(i) + '_' + str(j) + '_' + str(s) + '_' + str(t), lowerBound, upperBound, pulp.LpBinary)
                y[i,j] = pulp.LpVariable('y' + str(i) + '_' + str(j) + '_' + str(s) + '_' + str(t), lowerBound, upperBound, pulp.LpBinary)

prob += pulp.LpSum([ y[i,j,s,t] for i in range(2,n_port-1) for j in range(i,n_cont) for s in range(stacks) for t in range(tiers)])

for i in range(n_port-1):
    for j in range(i,n_cont):
        for s in range(stacks):
           for t in range(tiers):
               prob += x[i-1,j,s,t] - x[i,j,s,t] <= y[i,j,s,t]

for i in range(n_port-1):
    for s in range(1,stacks):
        for t in range(tiers):
            prob += x[i-1,i,s-1,t] + pulp.LpSum([ y[i,j,s-1,t] for j in range(i+1,n_port)]) <=  x[i-1,i,s,t] + pulp.LpSum([ y[i,j,s,t] for j in range(i+1,n_port)])

for j in range(n_port-1):
            prob += pulp.LpSum( [x[1,j,s,t] for s in range(stacks) for t in range(tiers)]) == T[1][j]



prob.solve()

print("Status:", LpStatus[prob.status])

