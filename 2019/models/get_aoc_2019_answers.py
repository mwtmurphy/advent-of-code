'''Prints answers for Advent of Code 2019'''

#import modules
from aoc import data, errors, models
import itertools
import networkx as nx
import numpy as np
from os import path

#functions
def get_day_1_answers():
    '''Prints answers for day 1'''
    with open(path.join(DATA_DIR, "raw/day_1.txt"), "r") as infile:
        masses = np.array(infile.readlines(), dtype=int)
    
    ans_1 = sum([models.get_simple_fuel(mass) for mass in masses])
    ans_2 = sum([models.get_complex_fuel(mass) for mass in masses])
    
    print("** Day 1 **")
    print(f"Fuel counter-upper for problem 1.1 = {ans_1}")
    print(f"Fuel counter-upper for problem 1.2 = {ans_2}", end="\n\n")

def get_day_2_answers():
    '''Prints answers for day 2'''
    with open(path.join(DATA_DIR, "raw/day_2.txt"), "r") as infile:
        intcode = np.array(infile.read().split(","), dtype=int)
        
    ans_1 = models.get_program_state(intcode.copy(), 12, 2)
    ans_2 = list(models.get_program_code(intcode.copy(), 19690720))[0]

    print("** Day 2 **")
    print(f"Program state for problem 2.1 = {ans_1}")
    print(f"Program code for problem 2.2 = {ans_2}", end="\n\n")
    
def get_day_3_answers():
    '''Prints answers for day 3'''
    with open(path.join(DATA_DIR, "raw/day_3.txt"), "r") as infile:
        wires = [wire.split(",") for wire in infile.readlines()]
        
    w1_coords = models.get_wire_coords(wires[0])
    w2_coords = models.get_wire_coords(wires[1])
    cross_coords = list(set(w1_coords) & set(w2_coords))

    man_dist = [abs(x) + abs(y) for x, y in cross_coords]
    ttl_steps = [w1_coords.index(coord) + w2_coords.index(coord) for coord in cross_coords]

    ans_1 = sorted(man_dist)[1]
    ans_2 = sorted(ttl_steps)[1]

    print("** Day 3 **")
    print(f"Minimum Manhattan distance for problem 3.1 = {ans_1}")
    print(f"Minimum total steps for problem 3.2 = {ans_2}", end="\n\n")

def get_day_4_answers():
    '''Prints answers for day 4'''
    simple_pwords = models.get_simple_pwords(256310, 732736)
    complex_pwords = models.get_complex_pwords(256310, 732736)

    ans_1 = len(simple_pwords)
    ans_2 = len(complex_pwords)

    print("** Day 4 **")
    print(f"Number of simple passwords for problem 4.1 = {ans_1}")
    print(f"Number of complex passwords for problem 4.2 = {ans_2}", end="\n\n")

def get_day_5_answers():
    '''Prints answers for day 5'''
    with open(path.join(DATA_DIR, "raw/day_5.txt"), "r") as infile:
        intcode = np.array(infile.read().split(","), dtype=int)

    diag_codes = models.get_diagnostic_codes(intcode.copy(), 1)
    ans_1 = diag_codes[-1]
    diag_codes = models.get_diagnostic_codes(intcode.copy(), 5)
    ans_2 = diag_codes[-1]

    print("** Day 5 **")
    print(f"Diagnostic code for problem 5.1 = {ans_1}")
    print(f"Diagnostic code  for problem 5.2 = {ans_2}", end="\n\n")

def get_day_6_answers():
    '''Prints answers for day 6'''
    with open(path.join(DATA_DIR, "raw/day_6.txt")) as infile:
        edges = [orbit.strip().split(")") for orbit in infile.readlines()]
    
    nodes = set(itertools.chain(*edges))
        
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    ans_1 = sum([len(nx.ancestors(graph, node)) for node in nodes])

    ugraph = graph.to_undirected()
    ans_2 = len(nx.shortest_path(ugraph, source="YOU", target="SAN"))-3

    print("** Day 6 **")
    print(f"Total direct and indirect orbits for problem 6.1 = {ans_1}")
    print(f"Shortest path to Santa for problem 6.2 = {ans_2}", end="\n\n")

def get_day_7_answers():
    '''Prints answers for day 7'''
    with open(path.join(DATA_DIR, "raw/day_7.txt")) as infile:
        intcode = np.array(infile.read().split(","), dtype=int)

    phases = list(itertools.permutations(range(5)))
    out_thrusts = []

    for seq in phases:
        in_sig = 0
        intcode_copy = intcode.copy()
        
        for in_code in seq:
            amp_output = models.get_amp_output(intcode_copy, [in_code, in_sig])
            in_sig = amp_output[0]
            
        out_thrusts.append(amp_output[0])

    ans_1 = max(out_thrusts)

    phases = list(itertools.permutations(range(5, 10)))
    out_thrusts = []

    for seq in phases:
        in_sig = 0
        com_ix = 0
        code_99 = False
        
        state = {}
        for i in range(5, 10):
            state[i] = {"ix": 0, "ic": intcode.copy()}
        
        while not code_99:
            for in_code in seq:
                amp_output, state[in_code]["ix"], code_99 = models.get_amp_loop_output(
                    state[in_code]["ic"], state[in_code]["ix"], [in_code, in_sig], com_ix
                )
                
                if amp_output:
                    in_sig = amp_output[0]
                else:
                    break
                
            if not com_ix:
                com_ix = 1
            
        out_thrusts.append(in_sig)

    ans_2 = max(out_thrusts)

    print("** Day 7 **")
    print(f"Highest signal that can be sent for problem 7.1: {ans_1}")
    print(f"Highest signal that can be sent for problem 7.2: {ans_2}", end="\n\n")

def get_day_8_answers():
    '''Refers to notebook for answers'''
    print("** Day 8 **")
    print("Refer to day_8_problem.ipynb in notebooks due to required graphing solution", end="\n\n")

def get_day_9_answers():
    '''Prints day 9 answers'''
    with open(path.join(DATA_DIR, "raw/day_9.txt")) as infile:
        bc = [int(val) for val in infile.read().split(",")]
    
    ans_1 = models.get_diagnostic_codes(bc, 1)[0]
    ans_2 = models.get_diagnostic_codes(bc, 2)[0]

    print("** Day 9 **")
    print(f"Test BOOST keycode for problem 9.1: {ans_1}")
    print(f"Sensor BOOST keycode for problem 9.2: {ans_2}", end="\n\n")


if __name__=="__main__":
    if data.load_env_vars():
        DATA_DIR = data.get_env_vars("DATA_DIR")
        get_day_1_answers()
        get_day_2_answers()
        get_day_3_answers()
        get_day_4_answers()
        get_day_5_answers()
        get_day_6_answers()
        get_day_7_answers()
        get_day_8_answers()
        get_day_9_answers()

    else:
        print("[*] Path to data directory should be stated in the '.env' under 'DATA_DIR'")
