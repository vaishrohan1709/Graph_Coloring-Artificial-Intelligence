import sys
import argparse
import math
import time
from collections import OrderedDict
from operator import itemgetter
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
        self.assignment = self.recursive_dfsb_plus({})
        return self.assignment

    def recursive_dfsb_plus(self,cur_assignment):
        if self.num_assigned==len(list(self.graph.keys())):
            return cur_assignment
        self.time = time.time() - self.starting_time

        state=self.most_constrained_variable(cur_assignment)
        print (state)

        lcv_colors_seq= self.least_constraining_value(state,cur_assignment)
        print (lcv_colors_seq)

        '''if self.time < 60:
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
            return None'''
    def get_arcs(self,cur_assignment):
        assigned_states = cur_assignment.keys()
        #arcs={}
        arcs=[]
        for state, value in self.graph.items():
            for head in value['Nodes']:
                arcs.append((state,head))
                #arcs[head].append((state,head))
        return arcs


    def arc_consistency(self, cur_assignment):
        assigned_states = cur_assignment.keys()
        arcs=self.get_arcs(cur_assignment)
        removed_colors = []
        while arcs:
            tail, head=arcs.pop(0)
            colors_h= self.graph[head]['Colors']
            colors_t=self.graph[tail]['Colors']
            flag=0
            for color in colors_t:
                if len(colors_h- {color})<0:
                    self.graph[tail]['Colors'].remove(color)
                    removed_colors.append(color)
                    flag=1
                if len(colors_t)==0:
                    return False
            if flag==1:
                arcs.append(self.get_tail_arcs(arcs,tail))
        return True

    def get_tail_arcs(self,arcs,tail):
        temp_arcs=[]
        for t,h in arcs:
            if h==tail:
                temp_arcs.append((t,h))
        return temp_arcs





    def forward_check(self,state,color,cur_assignment):
        assigned_states = cur_assignment.keys()
        unassigned_states = []
        for state in self.graph.keys():
            if state not in assigned_states:
                unassigned_states.append(state)
        connected_states=self.graph[state]['Nodes']
        for neighbor in connected_states:
            if neighbor in unassigned_states:
                if color in self.graph[neighbor]['Colors']:
                    self.graph[neighbor]['Colors'].remove(color)
                    if len(self.graph[neighbor]['Colors'])==0:
                        return False
        return True

    def least_constraining_value(self,state,cur_assignment):
        colors=self.graph[state]['Colors'][:]
        assigned_states = cur_assignment.keys()
        connected_states=self.graph[state]['Nodes']
        unassigned_states=[]
        for state in self.graph.keys():
            if state not in assigned_states:
                unassigned_states.append(state)
        colors_sequence = {c: 0 for c in colors}
        for color in colors:
            for neighbor in connected_states:
                if neighbor in unassigned_states:
                    if color in self.graph[neighbor]['Colors']:
                        colors_sequence[color]=colors_sequence[color] +1
        lcv=[]
        lcv_sequence = OrderedDict(sorted(colors_sequence.items(), key=itemgetter(1)))
        lcv=[x for x in lcv_sequence.keys()]
        return lcv




    def most_constrained_variable(self,cur_assignment):
        assigned_states=cur_assignment.keys()
        unassigned_states=[]
        for state in self.graph.keys():
            if state not in assigned_states:
                unassigned_states.append(state)
        print (unassigned_states)
        mcv=sys.maxsize
        mcv_state=None
        for state in self.graph.keys():
            if state in unassigned_states:
                if len(self.graph[state]['Colors'])<=mcv:
                    if len(self.graph[state]['Colors'])==mcv:
                        if len(self.graph[state]['Nodes'])>len(self.graph[mcv_state]['Nodes']):
                            mcv_state=state
                    elif len(self.graph[state]['Colors'])<mcv:
                        mcv_state = state
                    mcv = len(self.graph[state]['Colors'])
        return mcv_state

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
    if (str(sys.argv[3]) == '0'):
        mode = 0
        print("DFSB")
    elif (str(sys.argv[3]) == '1'):
        mode=1
        print("DFSB++")
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])
    graph=input_parse(input_file)
    print (graph)
    if mode==0:
        dfsb=DFSB(graph)
        answer=dfsb.dfsb_solution()
        print(answer)
    if mode==1:
        print ('hey')
        dfsb = DFSBPlus(graph)
        dfsb.dfsb_plus_solution()
        #print(answer)




