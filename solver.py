import networkx as nx
from parse import *
from utils import *
import sys
import numpy as np


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    k = len(G.nodes) // 2    
    stress_budget = s / k
    
    mapping = dict(zip([i for i in range(k)], [[] for i in range(k)]))
    room_assignments = [[] for i in range(k)]
    all_stress = dict(zip([i for i in range(k)], [0 for i in range(k)]))
    curr_room = 0
    # call helper function to find room assignment for node i
    while len(G.nodes) != 2 :
        try:
            try:
                node = np.random.choice(G.nodes)


                match= get_max_happiness(G, node)            

                stress_add_node = all_stress[curr_room]
                stress_add_match = all_stress[curr_room]
                if len(room_assignments[curr_room]) == 0:
                    all_stress[curr_room] += (G[node][match]['stress'])
                else:
                    for j in room_assignments[curr_room]:
                        try:
                            stress_add_node +=  G[node][j]['stress']

                            stress_add_match += G[match][j]['stress']
                        except KeyError as e:
                            continue
                if stress_add_node > stress_budget:
                    #put both into new room node
                    room_assignments[curr_room + 1] = [node, match]
                    all_stress[curr_room + 1] += stress_add_node
                elif stress_add_node + stress_add_match < stress_budget:
                    # add both to room
                    room_assignments[curr_room] += [node, match]
                    all_stress[curr_room] += stress_add_node
                    all_stress[curr_room] += stress_add_match
                elif stress_add_node < stress_budget or stress_add_match < stress_budget:
                    # choose max(happiness)
                    # one goes to curr 
                    # other goes into next room?
                    node_happy = potential_room_happiness(G,node,all_stress[curr_room],room_assignments[curr_room])
                    match_happy = potential_room_happiness(G,match,all_stress[curr_room],room_assignments[curr_room])
                    if node_happy >= match_happy:
                        room_assignments[curr_room].append(node)
                        all_stress[curr_room] += stress_add_node
                        room_assignments[curr_room + 1].append(match)    
                        all_stress[curr_room + 1] += stress_add_match

                    else:
                        room_assignments[curr_room].append(match)
                        all_stress[curr_room] += stress_add_match
                        room_assignments[curr_room + 1].append(node)         
                        all_stress[curr_room + 1] += stress_add_node


                for k, v in all_stress.items():
                    if v > stress_budget:
                        #mapping[curr_room] = room_assignments[curr_room]
                        curr_room += 1
                G.remove_node(node)
                G.remove_node(match)
                #plot_graph(G)
                if len(G.nodes) == 2:
                    for i in range(len(room_assignments)):  
                        if len(room_assignments[i]) == 0:
                            room_assignments[i] += list(G.nodes)
                            break

                elif len(G.nodes) == 1:
                    for i in range(len(room_assignments)):

                        if len(room_assignments[i]) == 0:

                            room_assignments[i] += list(G.nodes)
                            break


                mapping = dict(zip([i for i in range(len(room_assignments))], room_assignments))
            except IndexError:
                for i in range(len(room_assignments)):
                    if len(room_assignments[i]) == 0:
                        curr_room = i
                        continue
                    else:
                        pass
        except KeyError:
            continue
    return convert_dictionary(mapping), k

def get_max_happiness(G1, node):
    ret_node = -1
    curr_max = 0
    for j in range(len(G1.nodes)):
        if j == node:
            continue
        else:
            try:
                if G1[node][j]['happiness'] > curr_max:
                    ret_node = j
                    curr_max = G1[node][j]['happiness']
            except KeyError:
                continue
    return ret_node


def potential_room_happiness(G, node, s_room, room):
    potential_happiness = s_room
    for j in room:
        try:
            if j == node: continue
            potential_happiness += G[node][j]['happiness']
        except KeyError:
            continue

    return potential_happiness


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'out/test.out')

# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
