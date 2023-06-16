import plotly.figure_factory as ff

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


def plot_gantt_chart(result, num_machines, cmax):
    df = []

    for task, start_time in result.items():
        machine = start_time % num_machines + 1
        df.append(dict(Task=f'Machine {machine}', Start=int(start_time), Finish=int(start_time) + 1, Resource=task))

    fig = ff.create_gantt(df, index_col='Resource', show_colorbar=False, title='Gantt chart')
    fig.update_layout(xaxis_type='linear', xaxis_title='Time', yaxis_title='Machine Number')

    fig.add_annotation(x=max(result.values()) / 2, y=2*num_machines + 1.2, text=f'Cmax: {cmax}', showarrow=False)

    fig.show()


def main():
    nodes, edges, num_machines = get_input()

    result, cmax = coffman_graham(nodes, edges, num_machines)

    print(result)

    plot_gantt_chart(result, num_machines, cmax)


main()