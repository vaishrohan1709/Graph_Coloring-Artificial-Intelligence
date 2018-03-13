import sys
import argparse
import math
import time
from itertools import *
from heapq import heappush, heappop


class DFSB:
    def __init__(self,graph):
        self.graph=graph
        self.states=list(self.graph.keys())
        self.assignment=None
        self.time=0
        self.over_time=False
        self.num_assigned=0

    def dfsb_solution(self):
        self.starting_time=time.time()
        self.assignment=self.recursive_dfsb({})
        return self.assignment

    def recursive_dfsb(self,cur_assignment):
        if self.num_assigned==len(list(self.graph.keys())):
            return cur_assignment
        self.time=time.time()- self.starting_time
        if self.time < 60:
            state= self.states[self.num_assigned]
            permitted_colors=self.graph[state]['Colors'][:]
            for color in permitted_colors:
                if self.isSafe(cur_assignment,state,color):
                    temp_cur_assignment={**cur_assignment, **{state:color}}
                    self.num_assigned=self.num_assigned+1
                    temp_assignment=self.recursive_dfsb(temp_cur_assignment)
                    if temp_assignment:
                        return temp_assignment
                    if self.over_time:
                        return None
            return None

        else:
            self.over_time= True
            return None

    def isSafe(self,cur_assignment,state,color):
        for connected_state in self.graph[state]['Nodes']:
            if connected_state in cur_assignment:
                if color==cur_assignment[connected_state]:
                    return False
        return True


class DFSBPlus:

    def __init__(self,graph):
        self.graph = graph
        self.states = list(self.graph.keys())
        self.assignment = None
        self.time = 0
        self.over_time = False
        self.num_assigned = 0

    def dfsb_plus_solution(self):
        self.starting_time = time.time()
        self.assignment = self.recursive_dfsb({})
        return self.assignment

    def recursive_dfsb_plus(self,cur_assignment):
        if self.num_assigned==len(list(self.graph.keys())):
            return cur_assignment
        self.time = time.time() - self.starting_time
        
        if self.time < 60:
            state = self.states[self.num_assigned]
            permitted_colors = self.graph[state]['Colors'][:]
            for color in permitted_colors:
                if self.isSafe(cur_assignment, state, color):
                    temp_cur_assignment = {**cur_assignment, **{state: color}}
                    self.num_assigned = self.num_assigned + 1
                    temp_assignment = self.recursive_dfsb(temp_cur_assignment)
                    if temp_assignment:
                        return temp_assignment
                    if self.over_time:
                        return None
            return None

        else:
            self.over_time = True
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
    mode=0
    if (str(sys.argv[3]) == '1'):
        mode = 0
        print("DFSB")
    elif (str(sys.argv[3]) == '2'):
        mode=1
        print("DFSB++")
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])
    graph=input_parse(input_file)

    if mode==0:
        dfsb=DFSB(graph)
        answer=dfsb.dfsb_solution()
        print(answer)
    if mode==1:




