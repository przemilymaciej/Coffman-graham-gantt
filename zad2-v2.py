import matplotlib.pyplot as plt


def get_input():
    inputted = []

    while True:
        try:
            line = input()
        except EOFError:
            break
        inputted.append(line)

    nodes = inputted[0].replace("'", "").replace(" ", "").split(",")
    edges = eval("[" + inputted[1] + "]")
    num_machines = int(inputted[2])

    return nodes, edges, num_machines


def coffman_graham(nodes, edges, num_machines):
    stack = []
    visited = set()

    tasks = {node: [] for node in nodes}
    for edge in edges:
        tasks[edge[1]].append(edge[0])

    # Funkcja pomocnicza do rekurencyjnego znajdowania uszeregowania zadań
    def find_order_util(node, visited, stack):
        visited.add(node)
        for dependent in tasks[node]:
            if dependent not in visited:
                find_order_util(dependent, visited, stack)
        stack.append(node)

    # iteracja po wierzcholkach, ktore nie maja w. wychodzacych
    for node in nodes:
        if node not in visited:
            find_order_util(node, visited, stack)

    # inicjalizacja czasów rozpoczęcia zadań dla każdej maszyny
    start_times = {node: 0 for node in nodes}

    # wyliczanie czasów rozpoczęcia zadań dla każdej maszyny
    for node in stack:
        max_start_time = 0
        for dependent in tasks[node]:
            if start_times[dependent] > max_start_time:
                max_start_time = start_times[dependent]
        start_times[node] = max_start_time + 1

    sorted_tasks = sorted(start_times.items())

    cmax = max(start_times.values())

    result = {task[0]: start_time - 1 for task, start_time in sorted_tasks}

    return result, cmax


def plot_gantt_chart(task_order, num_machines, cmax):
    fig, ax = plt.subplots()

    machine_colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray']

    for i, (task, start_time) in enumerate(task_order.items()):
        machine = i % num_machines
        color = machine_colors[machine]
        ax.broken_barh([(start_time, 1)], (machine, 1), facecolors=color, edgecolor='black')
        ax.text(start_time + 0.5, machine + 0.5, task, ha='center', va='center')

    ax.set_ylim(0, num_machines)
    ax.set_xlim(0, max(task_order.values()) + 2)
    ax.set_xlabel('Czas')
    ax.set_ylabel('Maszyny')

    ax.annotate(f'Cmax: {cmax}', xy=(1, -0.05), xytext=(-10, -10), xycoords='axes fraction', textcoords='offset points', ha='right', va='top')

    ax.set_yticks(range(num_machines))
    ax.set_yticklabels(range(1, num_machines+1))
    ax.set_title('Wykres Gantta')

    plt.show()



def main():
    nodes, edges, num_machines = get_input()

    result, cmax = coffman_graham(nodes, edges, num_machines)

    print(result)

    plot_gantt_chart(result, num_machines, cmax)


main()