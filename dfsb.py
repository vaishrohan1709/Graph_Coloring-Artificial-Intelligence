import sys
import argparse
import math
import time
from collections import OrderedDict
from operator import itemgetter
from itertools import *
from heapq import heappush, heappop
from copy import deepcopy


class DFSB:

    #initializing DFSB class variables
    def __init__(self, graph):
        self.graph = graph
        self.states = list(self.graph.keys())
        self.assignment = None
        self.steps = 0

    #function to generate assignment
    def dfsb_solution(self):
        self.starting_time = time.time()

        # starting with empty assignment and with first state
        self.assignment = self.recursive_dfsb(0, {})
        return self.assignment

    #function to support dfsb_solution function
    def recursive_dfsb(self, var_assigned, cur_assignment):

        #if all assignment are not complete
        if var_assigned != len(list(self.graph.keys())):
            self.steps += 1

            #if under time
            if (time.time() - self.starting_time) < 60:
                state = self.states[var_assigned]
                for color in self.graph[state]['Colors']:

                    #checking if neigbors are compatible with the current assignment
                    if self.isSafe(cur_assignment, state, color):

                        #taking a copy of current assignment to put the color to current state
                        temp_cur_assignment = deepcopy(cur_assignment)
                        temp_cur_assignment[state] = color

                        #recursively calling the function for further assignments
                        temp_assignment = self.recursive_dfsb(
                            var_assigned + 1, temp_cur_assignment)

                        #if last assignment is compatible, return it
                        if temp_assignment is not None:
                            return temp_assignment

                        # if over time
                        if time.time() - self.starting_time > 60:
                            return None
                return None

            # if over time
            else:
                return None

        # if all assignment are complete
        else:
            return cur_assignment

    #function to check the current assignment compatibility with the neighbors
    def isSafe(self, cur_assignment, state, color):
        for connected_state in self.graph[state]['Nodes']:
            if connected_state in cur_assignment:
                if color == cur_assignment[connected_state]:
                    return False
        return True


class DFSBPlus:

    #initializing the class variables for DFSBPlus
    def __init__(self, graph):
        self.graph = graph
        self.states = list(self.graph.keys())
        self.assignment = None
        self.steps = 0

    #function to generate assigment
    def dfsb_plus_solution(self):
        self.starting_time = time.time()

        #starting with empty assignment and with first state
        self.assignment = self.recursive_dfsb_plus(0, {})
        return self.assignment

    #function to support dfsb_plus_solution
    def recursive_dfsb_plus(self, var_assigned, cur_assignment):

        # if all assignment are not complete
        if var_assigned != len(list(self.graph.keys())):
            self.steps += 1

            #if under time
            if time.time() - self.starting_time < 60:

                #selecting the most constrained state as our next assignment
                state = self.most_constrained_variable(cur_assignment)

                #generating the color sequence in the order of least contraining values
                lcv_colors_seq = self.least_constraining_value(
                    state, cur_assignment)
                for color in lcv_colors_seq:

                    #taking a backup of current graph
                    backup = deepcopy(self.graph)
                    self.graph[state]['Colors'] = [color]
                    self.steps += 1

                    #checking for AC3 consistency with the current assignment and pruning domains
                    if self.arc_consistency(cur_assignment, state):
                        temp_cur_assignment = deepcopy(cur_assignment)
                        temp_cur_assignment[state] = color

                        #recursively calling the function for further assignments
                        temp_assignment = self.recursive_dfsb_plus(
                            var_assigned + 1, temp_cur_assignment)

                        #if assignment is compatible, return it
                        if temp_assignment is not None:
                            return temp_assignment

                    #if assignment is not compatible, restore graph to previous state
                    self.graph = backup

                    #if over time
                    if time.time() - self.starting_time > 60:
                        print('overtime')
                        return None

                return None

            # if over time
            else:
                print('overtime')
                return None

        #if all assignments are done, return it
        else:
            return cur_assignment

    #function to generate arcs between all the unassignment states and storing them in a list
    def get_arcs(self, cur_assignment):
        assigned_states = cur_assignment.keys()
        arcs = []
        for state, value in self.graph.items():
            for head in value['Nodes']:
                if state not in assigned_states:
                    arcs.append((state, head))
        return arcs

    #function to check arc consistency and pruning domains, returns false if it fails
    def arc_consistency(self, cur_assignment, state):
        assigned_states = list(cur_assignment.keys())
        assigned_states.append(state)

        #getting all arcs
        arcs = self.get_arcs(cur_assignment)

        #until arcs queue is not empty
        while arcs:
            '''prunes tail's domain on the basis of head's domain. If a color is removed from tail's domain, 
            all the arcs coming into the tail are added back to the end of the queue'''

            tail, head = arcs.pop(0)
            colors_h = self.graph[head]['Colors']
            colors_t = self.graph[tail]['Colors']
            colors_t_copy = colors_t
            for color in colors_t:
                if color in colors_h:
                    if len(colors_h) == 1:
                        colors_t.remove(color)
            if len(colors_t) != 0:
                if colors_t_copy != colors_t:
                    self.graph[tail]['Colors'] = [colors_t]
                    arcs.append(self.get_tail_arcs(arcs, tail))
            else:
                return False
        return True

    #fuction to generate arcs from a particular tail
    def get_tail_arcs(self, arcs, tail):
        temp_arcs = []
        for (t, h) in arcs:
            if h == tail:
                temp_arcs.append((t, h))
        return temp_arcs

    #function to get the order of least constraining colors
    def least_constraining_value(self, state, cur_assignment):
        colors = self.graph[state]['Colors'][:]
        assigned_states = cur_assignment.keys()
        connected_states = self.graph[state]['Nodes']
        unassigned_states = []

        #removing all the assigned states
        for state in self.graph.keys():
            if state not in assigned_states:
                unassigned_states.append(state)
        colors_sequence = {c: 0 for c in colors}

        #maintaining a dictionary with color as key and number of occurences in neighbors as value
        for color in colors:
            for neighbor in connected_states:
                if neighbor in unassigned_states:
                    if color in self.graph[neighbor]['Colors']:
                        colors_sequence[color] = colors_sequence[color] + 1
        lcv = []

        #sorting the dictionary by values in the descendig order
        lcv_sequence = OrderedDict(
            sorted(colors_sequence.items(), key=itemgetter(1)))
        lcv = [x for x in lcv_sequence.keys()]
        return lcv

    #function to get the most contrained state
    def most_constrained_variable(self, cur_assignment):
        assigned_states = cur_assignment.keys()
        unassigned_states = []

        #removing all the assigned states
        for state in self.graph.keys():
            if state not in assigned_states:
                unassigned_states.append(state)
        '''this logic gives us that state which has the least numbers of colors in domain,
        if there is a tie, then select the state with most neighbors, if still tie, return 
        the first one'''

        mcv = sys.maxsize
        mcv_state = None
        for state in self.graph.keys():
            if state in unassigned_states:
                if len(self.graph[state]['Colors']) <= mcv:
                    if len(self.graph[state]['Colors']) == mcv:
                        if len(self.graph[state]['Nodes']) > len(
                                self.graph[mcv_state]['Nodes']):
                            mcv_state = state
                    elif len(self.graph[state]['Colors']) < mcv:
                        mcv_state = state
                    mcv = len(self.graph[state]['Colors'])
        return mcv_state


#function to parse input file as graph
def input_parse(input_file):
    input = open(input_file).read()
    line1 = input.split('\n')[0]
    number_nodes = int(line1.split()[0])
    connections = int(line1.split()[1])
    colors = int(line1.split()[2])
    graph = {n: {'Nodes': [], 'Colors': []} for n in range(number_nodes)}
    for line in input.split('\n')[1:connections + 1]:
        graph[int(line.split()[0])]['Nodes'].append(int(line.split()[1]))
        graph[int(line.split()[1])]['Nodes'].append(int(line.split()[0]))
    for i in range(number_nodes):
        graph[i]['Colors'] = list(range(colors))
    return graph


#function to write output to file
def write_output(output_file, answer):
    solution = ''
    output = open(output_file, "w")
    if (answer is None):
        output.write('No answer')
    else:
        for state in sorted(answer.keys()):
            solution = solution + str(answer[state]) + '\n'
        solution.strip(' \t\n\r')
        output.write(solution)
    output.close()


if __name__ == '__main__':
    mode = 0
    if (str(sys.argv[3]) == '0'):
        mode = 0
        print("DFSB")
    elif (str(sys.argv[3]) == '1'):
        mode = 1
        print("DFSB++")
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])
    graph = input_parse(input_file)

    #if mode is 0, use DFSB
    if mode == 0:
        dfsb = DFSB(graph)
        answer = dfsb.dfsb_solution()
        write_output(output_file, answer)

    # if mode is 0, use DFSB++
    if mode == 1:
        dfsb = DFSBPlus(graph)
        answer = dfsb.dfsb_plus_solution()
        write_output(output_file, answer)
