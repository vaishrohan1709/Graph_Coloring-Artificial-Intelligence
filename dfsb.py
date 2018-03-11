import sys
import argparse
import math
import time
from itertools import *
from heapq import heappush, heappop


class DFSB:
    def __init__(self,graph):
        self.graph=graph
        self.states=list(self.graphs.keys())
        self.assignment=None
        self.time=0
        self.over_time=False
        self.num_assigned=0

    def dfsb_solution(self):
        self.starting_time=time.time()
        self.assignment=self.recursive_dfsb({})
        return self.solution

    def recursive_dfsb(self,cur_assignment):
        if self.num_assigned==len(list(self.graphs.keys()))
            return cur_assignment

        self.time=time.time()- self.starting_time

        if self.time < 60:
            state= self.states[self.num_assigned]
            permitted_colors=self.graph[state]['Colors'][:]
            for connected_state in self.graph[state]['Nodes']:
                if cur_assignment[connected_state] in permitted_colors:
                    permitted_colors.remove(ur_assignment[connected_state])

            for color in permitted_colors:



        else:
            self.over_time= True
            return None









def input_parse(input_file):
    input = open(input_file).read()
    line1=input.split('\n')[0]
    number_nodes= int(line1.split()[0])
    connections = int(line1.split()[1])
    colors = int(line1.split()[2])
    graph={n: {'Nodes':[],'Colors':[]} for n in range(number_nodes)}
    for line in input.split('\n')[1:connections+1]:
        graph[int(line.split()[0])]['Nodes'].append(int(line.split()[1]))
        graph[int(line.split()[1])]['Nodes'].append(int(line.split()[0]))
    for i in range(number_nodes):
        graph[i]['Colors']=list(range(colors))
    return graph





if __name__ == '__main__':
    if (str(sys.argv[3]) == '1'):
        mode = 1
        print("DFSB")
    elif (str(sys.argv[3]) == '2'):
        mode=2
        print("DFSB++")
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])
    graph=input_parse(input_file)
    print(graph)

    '''print('Output:')
    if (algorithm == 1):
        initialize = Astar(start_state, heuristic, type)
        solution = initialize.A_star_solution()
        print(solution)

    elif (algorithm == 2):
        initialize = IDAstar(start_state, heuristic, type)
        solution = initialize.IDAstar_solution()
        print(solution)

    output = open(output_file, "w")
    output.write(solution)
    output.close()'''
