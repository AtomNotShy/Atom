import math
import heapq
import re

directions = {
    1: [+1, 0, 0],
    2: [-1, 0, 0],
    3: [0, +1, 0],
    4: [0, -1, 0],
    5: [0, 0, +1],
    6: [0, 0, -1],
    7: [+1, +1, 0],
    8: [+1, -1, 0],
    9: [-1, +1, 0],
    10: [-1, -1, 0],
    11: [+1, 0, +1],
    12: [+1, 0, -1],
    13: [-1, 0, +1],
    14: [-1, 0, -1],
    15: [0, +1, +1],
    16: [0, +1, -1],
    17: [0, -1, +1],
    18: [0, -1, -1]
}


# read basic info and build graph
def read_file(name):
    global grid_size, start, end, number_of_points, search_method, graph, parents

    with open(name, 'r') as f:
        lines = [line.split() for line in f]
    search_method = lines.pop(0).pop()
    for i in range(0, 3):
        lines[i] = list(map(int, lines[i]))

    grid_size = lines.pop(0)
    start = str(lines.pop(0))
    end = str(lines.pop(0))
    number_of_points = lines.pop(0)
    graph = dict()

    if search_method != 'BFS':
        # build weighted graph and initial parents
        for line in lines:
            line = list(map(int, line))
            graph[str((line[:3]))] = dict()
            for act in line[3:]:
                if act < 7:
                    d = 10
                else:
                    d = 14
                next_v = str(list(map(lambda x, y: x + y, line[:3], directions[act])))

                graph[str((line[:3]))][next_v] = d
    else:
        # unweighted graph and initial parents
        for line in lines:
            adj = []
            line = list(map(int, line))
            for act in line[3:]:
                next_v = str(list(map(lambda x, y: x + y, line[:3], directions[act])))
                adj.append(next_v)
                graph[str((line[:3]))] = adj
    return


def inti_distance(graph, start):
    distance = {str(start): 0}
    for k in graph.keys():
        if k != str(start):
            distance[k] = math.inf
    return distance


def heuristic(node, end):
    node = list(re.sub('\D+', ' ', node).split())
    end = list(re.sub('\D+', ' ', end).split())
    dx = abs(int(node[0]) - int(end[0]))
    dy = abs(int(node[1]) - int(end[1]))
    dz = abs(int(node[2]) - int(end[2]))
    return 10 * (dx + dy + dz)


def BFS():
    queue = [start]
    visited = set()
    visited.add(start)
    parent = {start: start}
    while queue:
        ver = queue.pop(0)
        nodes = graph[ver]
        for node in nodes:
            if node not in visited:
                queue.append(node)
                visited.add(node)
                parent[node] = ver
    return parent


def UCS():
    pqueue = []
    heapq.heappush(pqueue, (0, start))
    visited = set()
    visited.add(start)
    distance = inti_distance(graph, start)
    parents = {start: start}
    while pqueue:
        pair = heapq.heappop(pqueue)
        dist = pair[0]
        vertex = str(pair[1])
        visited.add(vertex)
        nodes = graph[vertex].keys()
        for node in nodes:
            if node not in visited:
                if (dist + graph[vertex][node]) <= distance[node]:
                    heapq.heappush(pqueue, (dist + graph[vertex][node], node))
                    parents[node] = vertex
                    distance[node] = dist + graph[vertex][node]
    return parents, distance


def AStar():
    pqueue = []
    parent = {start: start}
    heapq.heappush(pqueue, (0, start))
    visited = set()
    visited.add(start)
    distance = inti_distance(graph, start)
    distance_g = inti_distance(graph, start)
    while pqueue:
        pair = heapq.heappop(pqueue)
        dist = pair[0]
        vertex = str(pair[1])
        visited.add(vertex)
        nodes = graph[vertex].keys()
        for node in nodes:
            if node not in visited:
                distance_g[node] = graph[vertex][node] + distance_g[vertex]
                if (dist + graph[vertex][node]) < distance[node]:
                    heapq.heappush(pqueue, (dist + graph[vertex][node] + heuristic(node, end), node))
                    parent[node] = vertex
                    distance[node] = dist + graph[vertex][node]
    return parent, distance_g[end]


def find_path(parents_list, key):
    res = []
    while parents_list[key] != start:
        res.append(key)
        key = parents_list[key]
    res.append(key)
    res.append(start)
    res.reverse()
    return res


def find_a_path(parents_list, key):
    f_dist = 0
    res = []
    while parents_list[key] != start:
        res.append(key)
        key = parents_list[key]
        f_dist = f_dist + graph[key][res[-1]]
    f_dist = f_dist + graph[key][start]
    res.append(key)
    res.append(start)
    res.reverse()
    return res, f_dist


def bfs_write(path):
    cost = [0]
    cost.extend([1] * (len(path) - 1))
    with open('output.txt', 'w') as f:
        f.writelines(str(len(path) - 1) + '\n')
        f.writelines(str(len(path)) + '\n')
        n = 0
        for line in path:
            line = re.sub('\D+', ' ', line).lstrip()
            f.writelines(line + str(cost[n]) + '\n')
            n += 1
    return


def ucs_write(graph, distance, path):
    with open('output.txt', 'w') as f:
        if type(distance) == int:
            f.writelines(str(distance) + '\n')
            f.writelines(str(len(path)) + '\n')
        else:
            f.writelines(str(distance[end]) + '\n')
            f.writelines(str(len(path)) + '\n')

        for n in range(len(path)):
            if n != 0:
                cost = graph[path[n - 1]][path[n]]
                line = re.sub('\D+', ' ', path[n]).lstrip()
                f.writelines(line + '' + str(cost) + '\n')
            else:
                line = re.sub('\D+', ' ', path[n]).lstrip()
                f.writelines(line + '' + str(0) + '\n')
    return


def write_fail():
    with open('output.txt', 'w') as f:
        f.write('FAIL')
        exit(0)
    return


def excute():
    if end not in graph:
        write_fail()
    else:
        if search_method == 'BFS':
            parents_list = BFS()
            path = find_path(parents_list, end)
            bfs_write(path)
        elif search_method == 'UCS':
            parents_list, distance = UCS()
            path, dis = find_a_path(parents_list, end)
            ucs_write(graph, distance, path)
        elif search_method == 'A*':
            parents_list, dist = AStar()
            path, dis = find_a_path(parents_list, end)
            ucs_write(graph, dis, path)
    return


if __name__ == '__main__':
    import time
    s = time.time()
    read_file('input7.txt')
    excute()
    e = time.time()
    print('time:', e - s, 's')
