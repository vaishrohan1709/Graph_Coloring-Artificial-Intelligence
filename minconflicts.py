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

    #initializing minimum conflicts class variables
    def __init__(self, graph):
        self.graph = graph
        self.states = list(self.graph.keys())
        self.colors = list(self.graph.values())[0]['Colors']
        self.assignment = None
        self.number_conflicts = 0
        self.variables_conflict = []
        self.steps = 0

    #function to select a color which is least conflicting with neighbors
    def min_conflicts_color(self, state, cur_assignment, impossible_color):

        colors = list(self.graph[state]['Colors'][:])
        colors.remove(impossible_color)
        connected_states = self.graph[state]['Nodes']
        colors_sequence = {c: 0 for c in colors}
        '''further logic gives a dictionary with color as key and number of occurences in neighbors
        as the value'''

        for color in colors:
            for neighbor in connected_states:
                if color == cur_assignment[neighbor]:
                    colors_sequence[color] = colors_sequence[color] + 1
        lcv = []

        #sorting the dictionary by value to get the order of minimum conflicts color
        lcv_sequence = OrderedDict(
            sorted(colors_sequence.items(), key=itemgetter(1)))
        lcv = [x for x in lcv_sequence.keys()]

        #return the color with least conflicts
        return lcv[0]

    #function to update number of conflicts and the conflicting states for a particular trial
    def conflicts_info(self, assignment):
        for state in assignment:
            for neighbor in self.graph[state]['Nodes']:
                if assignment[neighbor] == assignment[state]:
                    if neighbor not in self.variables_conflict:
                        self.variables_conflict.append(neighbor)
                    if state not in self.variables_conflict:
                        self.variables_conflict.append(state)
                    self.number_conflicts += 1

    #function to select a random state amongst the conflicting states
    def random_state_select(self, variables_conflict):
        return random.choice(variables_conflict)

    #function to support random restarts by providing random color assignments to each state
    def random_state(self):
        random_state = {}
        for s in self.states:
            random_state[s] = random.choice(self.colors)
        return random_state

    #function to get minconflicts solution
    def minconflicts_solution(self, starting_time):

        #random restart
        for random_restart in range(100):

            #getting a random initial assignment
            cur_assignment = self.random_state()

            #conflict reduction trials
            for trial in range(10000):
                self.steps += 1
                self.number_conflicts = 0
                self.variables_conflict = []
                self.conflicts_info(cur_assignment)

                #to support time limit of 60 sec
                if (time.time() - starting_time) < 60:

                    #if conflicts are 0, return the current assignment as solution
                    if self.number_conflicts == 0:
                        self.assignment = cur_assignment
                        return self.assignment
                    else:

                        #selecting next state to assign and giving it minimum conflicting color
                        next_state = self.random_state_select(
                            self.variables_conflict)
                        next_state_color = self.min_conflicts_color(
                            next_state, cur_assignment,
                            cur_assignment[next_state])
                        cur_assignment[next_state] = next_state_color
                else:

                    # to support time limit of 60 sec
                    self.assignment = None
                    print('overtime')
                    return None
        return None


#function to parse the input file as a graph with state as key and Neighbor Nodes and Colors are values
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


#function to write solution to file
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
    input_file = str(sys.argv[1])
    output_file = str(sys.argv[2])
    graph = input_parse(input_file)

    #generating graph
    minconflict = minconflicts(graph)

    #noting the starting time
    starting_time = time.time()
    answer = minconflict.minconflicts_solution(starting_time)
    write_output(output_file, answer)
