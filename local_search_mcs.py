#!/usr/bin/python3
import random
import numpy as np

from copy import deepcopy
from matplotlib import pyplot as plt
from collections import Counter
from graph import Graph

#stari calc_solution trebace
def calc_solution_value(graph):

#   stari deo-- radi ali nije potreban
    #[1,2,4,7,1,3,6,7,7,2,4] boje svakog cvora
    #[(1,2),(2,2),(3,1),(4,2),(6,1),(7,3)] broj pojavljivanja svake boje
    #[(7,3),(4,2),(2,2),(1,2),(6,1),(3,1)] sortiramo po boju pojavljivanja tj.drugom parametru
    # 3*1 + 2*2 + 2*3 + 2*4 + 1*5 + 1*6  funkcija cilja=suma(broj_pojavljuvanja*indeks_unizu)

    tmp = list(map(lambda el: (el,1),graph.coloring_vector))
    tmp = list(set([(el[0], Counter(tmp)[el]) for el in tmp]))
    tmp = sorted(tmp, key = lambda el: el[1],reverse=True)

    total_sum = 0
    for index,tupp in enumerate(tmp):
        total_sum += (index+1)*tupp[1]

    return total_sum

def free_colors(zauzete, ind, n):
    slobodne = []
    for i in range(1,n+1):
        if i not in zauzete[ind]:
            slobodne.append(i)
    return slobodne

def calc_solution_value(solution, graph):
    n = graph.num_of_vertices
    x_boje = [0 for _ in range(n)]
    zauzete = [[] for _ in range(n)]

    for i in range(len(solution)):
        ind = solution.index(i)
        if i == 0:
            x_boje[ind] = 1
            for j in range(n):
                if graph.get_edges(ind,j) == 1:
                    zauzete[j].append(1)
        else:
            slobodne = free_colors(zauzete,ind,n)
            x_boje[ind] = min(slobodne)
            for j in range(n):
                if graph.get_edges(ind,j) == 1:
                    zauzete[j].append(x_boje[ind])

    # print(x_boje)
    # print(sum(x_boje))
    return sum(x_boje)

def initialize(num_resources):
    #generisemo permutacije
    solution = list(np.random.permutation(num_resources))
    return solution

def make_small_change(solution):
    poz1 = random.randrange(0, len(solution))
    poz2 = random.randrange(0, len(solution))
    pom = solution[poz1]
    solution[poz1] = solution[poz2]
    solution[poz2] = pom

    return solution
def draw_graph(xs, ys):
    # iscrtavnanje grafika
    plt.title('Solution value through the iterations: ')
    plt.xlabel('Iters')
    plt.ylabel('Target function')
    plt.plot(xs, ys, color='blue')
    plt.show()

def local_search(graph, max_iters):
    #initialize solution
    solution = initialize(graph.num_of_vertices)
    curr_value = calc_solution_value(solution, graph)

    # za iscrtavanje grafika
    xs = []
    ys = []

    for i in range(max_iters):
        #malo promenimo resenje
        new_solution = make_small_change(solution)
        new_value = calc_solution_value(new_solution,graph)
        if new_value < curr_value:
            solution = deepcopy(new_solution)
            curr_value = new_value
        else:
            #nastavi sa starim resenjem
            pass

        xs.append(i)
        ys.append(curr_value)

    draw_graph(xs,ys)

    return solution,curr_value

if __name__=='__main__':

    g = Graph(30)
    g.random_graph()
    # g.save_graph_to_file("random_graph.txt")
    g.load_graph_from_file("random_graph.txt")
    # print(g)

    solution, curr_value = local_search(g,10000)
    print(solution)
    print(curr_value)