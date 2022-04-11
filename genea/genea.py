import copy

import matplotlib.pyplot as plt

import ga2
import cost_function

results = []


def start(config):
    # Problem Definition
    cost_fun = cost_function.main
    # Run GA
    res = (ga2.run(config, cost_fun))
    results.append(copy.deepcopy(res))
    save_to_file(res, config.file_path)


color_it = 0


# Results and Plot'''
'''
def show_graph(res_i, config):

    for i in range(int(res_i)):
        start(config)
        config.seed += 5

    colors = ['r', 'b', 'g']

    #try:
    #    int(res_i)
    #except ValueError:
    #    return "Argument must be an integer equal to or greater than 0 and less than current number of solutions"

    #if int(res_i) > len(results) - 1:
    #    return "Entered number of solution is out of bounds for current solutions"

    a1 = []
    z = 0
    cit = results[0].converged_it
    for i in range(150):
        if i > cit > 0:
            a1.append(results[0].best_cost[z])
        else:
            a1.append(results[0].best_cost[i])
            z = i

    a2 = []
    z = -1
    cit = results[1].converged_it
    for i in range(150):
        if i > cit > 0:
            a2.append(results[1].best_cost[z])
        else:
            a2.append(results[1].best_cost[i])
            z = i

    a3 = []
    z = -1
    cit = results[2].converged_it
    for i in range(150):
        if i > cit > 0:
            a3.append(results[2].best_cost[z])
        else:
            a3.append(results[2].best_cost[i])
            z = i

    plt.semilogy(a1, colors[0], label="1")
    plt.semilogy(a2, colors[1], label="2")
    plt.semilogy(a3, colors[2], label="3")

    plt.xlim(0, 150)

    plt.xlabel('Generations')
    plt.ylabel('Cost')
    plt.title('Genetic Algorithm')
    plt.legend()
    plt.grid(True)
    plt.savefig("res_" + res_i, format='png', dpi=1200)
    plt.show()
    return

'''
def clear_graph():
    results.clear()


def save_to_file(out, file_path):
    name = out.name
    if len(file_path) > 2:
        file_path = file_path + '/' + name + '.txt'
    else:
        file_path = name + '.txt'

    file = open(file_path, 'w')
    file.write("Best solution: " + str(out.best_sol.cost) + "\n")
    file.write("Best and average solutions from each generation: \n")
    if out.converged_it <= 0:
        it = 150
    else:
        it = out.converged_it
    for i in range(it):
        if i == 0:
            file.write('{0:20}{1:20}{2:20}\n'.format('Gen', 'Best', 'Avg'))
            file.write(f"--------------------------------------------------------------\n")
        file.write('{:-5} {:-20} {:-20}\n'.format(i, round(out.best_cost[i], 3), round(out.avg_cost[i], 3)))

    file.close()
