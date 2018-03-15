import sys
import argparse
import math
import time
from collections import OrderedDict
from operator import itemgetter
from itertools import *
from heapq import heappush, heappop
from copy import deepcopy
import random


class minconflicts:

    def __init__(self,graph):
        self.graph = graph
        self.states = list(self.graph.keys())
        self.colors= list(self.graph.values())[0]['Colors']
        self.assignment = None
        #self.time = 0
        self.number_conflicts=0
        self.variables_conflict=[]

    def min_conflicts_color(self,state,cur_assignment,impossible_color):

        colors=list(self.graph[state]['Colors'][:])
        colors.remove(impossible_color)
        connected_states=self.graph[state]['Nodes']
        colors_sequence = {c: 0 for c in colors}
        for color in colors:
            for neighbor in connected_states:
                if color== cur_assignment[neighbor]:
                    colors_sequence[color]=colors_sequence[color] +1
        lcv=[]
        lcv_sequence = OrderedDict(sorted(colors_sequence.items(), key=itemgetter(1)))
        lcv=[x for x in lcv_sequence.keys()]
        return lcv[0]

    def conflicts_info(self,assignment):
        for state in assignment:
            for neighbor in self.graph[state]['Nodes']:
                if assignment[neighbor]==assignment[state]:
                    if neighbor not in self.variables_conflict:
                        self.variables_conflict.append(neighbor)
                    if state not in self.variables_conflict:
                        self.variables_conflict.append(state)
                    self.number_conflicts+=1

    def random_state_select(self,variables_conflict):
        return random.choice(variables_conflict)

    def random_state(self):
        random_state={}
        for s in self.states:
            random_state[s]=random.choice(self.colors)
        return random_state

    def minconflicts_solution(self,starting_time):
        for random_restart in range(100):
            cur_assignment=self.random_state()
            #print ('curr ass:', cur_assignment)
            for trial in range(10000):
                self.number_conflicts = 0
                self.variables_conflict = []
                self.conflicts_info(cur_assignment)
                if (time.time()-starting_time)<0.3:
                    if self.number_conflicts==0:
                        self.assignment=cur_assignment
                        print ('trial', trial)
                        return self.assignment
                    else:
                        next_state=self.random_state_select(self.variables_conflict)
                        next_state_color=self.min_conflicts_color(next_state,cur_assignment,cur_assignment[next_state])
                        cur_assignment[next_state]=next_state_color
                else:
                    self.assignment=None
                    print ('overtime')
                    return None
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

def verify_solution(solution, graph):
    if solution == None:
        return False
    for node in solution:
        for dependent_node in graph[node]['Nodes']:
            if solution[node] == solution[dependent_node]:
                return False
    return True

if __name__ == '__main__':
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])
    graph=input_parse(input_file)
    minconflict=minconflicts(graph)
    starting_time = time.time()
    answer=minconflict.minconflicts_solution(starting_time)
    print(answer)
    if verify_solution(answer,graph):
        print ('correct')
    else:
        print ('incorrect')