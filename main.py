import time


class Node:
    def __init__(self, key, parent, mov):
        self.key = key
        self.children = []
        self.parent = parent
        self.move = mov


def search_node(node, target):
    if node is None:
        return None
    queue = [node]
    while queue:
        current_node = queue.pop(0)
        if current_node.key == target:
            return current_node
        for node in current_node.children:
            queue.append(node)
    return Node


def get_neighbours(parent, visited, visited_goal):
    row, col, new_state = None, None, []
    #hľadanie pozície prázdneho miesta(0)
    for i in range(len(parent.key)):
        for j in range(len(parent.key[i])):
            if parent.key[i][j] == 0:
                row, col = i, j

    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for move in moves:
        # vypočítanie novej pozície prázdneho políčka(0) a kontrola či je tento posun v hraniciach poľa
        new_row, new_col = row + move[0], col + move[1]
        if 0 <= new_row < len(parent.key) and 0 <= new_col < len(parent.key[0]):
            new_state = [n[:] for n in parent.key]
            new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
            if new_state not in visited:
                #filtrovanie stavov, ktoré sme už niekedy navštívili a značky posunu
                if visited_goal is True:
                    if move == (0, 1):
                        parent.children.append(Node(new_state, parent, "LEFT"))
                    elif move == (0, -1):
                        parent.children.append(Node(new_state, parent, "RIGHT"))
                    elif move == (1, 0):
                        parent.children.append(Node(new_state, parent, "UP"))
                    elif move == (-1, 0):
                        parent.children.append(Node(new_state, parent, "DOWN"))
                else:
                    if move == (0, 1):
                        parent.children.append(Node(new_state, parent, "RIGHT"))
                    elif move == (0, -1):
                        parent.children.append(Node(new_state, parent, "LEFT"))
                    elif move == (1, 0):
                        parent.children.append(Node(new_state, parent, "DOWN"))
                    elif move == (-1, 0):
                        parent.children.append(Node(new_state, parent, "UP"))


def bidirectional_search(start, goal):
    visited_start = []
    visited_goal = []
    path = []
    queue_toVisit_start = [start]
    queue_toVisit_goal = [goal]

    while queue_toVisit_goal and queue_toVisit_start:
        current_start_node = queue_toVisit_start.pop(0)
        current_goal_node = queue_toVisit_goal.pop(0)
        # zisťovanie či sme už našli spoločný stav
        if current_start_node.key in visited_goal:
            #nájdenie spoločného stavu v koncovom strome
            node = search_node(goal, current_start_node.key)
            #skonštruovanie cesty
            while current_start_node is not None:
                path.append(current_start_node)
                current_start_node = current_start_node.parent
            path.reverse()


            while node is not None:
                path.append(node)
                node = node.parent
            #výpis počtu stavov
            print("From start: ", len(visited_start))
            print("From goal: ", len(visited_goal))
            return path

        if current_goal_node.key in visited_start:
            node = search_node(start, current_goal_node.key)


            while node is not None:
                path.append(node)
                node = node.parent
            path.reverse()

            while current_goal_node is not None:
                path.append(current_goal_node)
                current_goal_node = current_goal_node.parent
            print("From start: ", len(visited_start))
            print("From goal: ", len(visited_goal))
            return path
        #nájdenie susedov v strome začínajúcom v počiatočnom stave
        get_neighbours(current_start_node, visited_start, False)
        for node in current_start_node.children:
            visited_start.append(node.key)
            queue_toVisit_start.append(node)
        # nájdenie susedov v strome začínajúcom v koncovom stave
        get_neighbours(current_goal_node, visited_goal, True)
        for node in current_goal_node.children:
            visited_goal.append(node.key)
            queue_toVisit_goal.append(node)
    #ak nie je možné nájsť riešenie program výkoná túto časť
    print("Unsolvable")
    print("From start: ", len(visited_start))
    print("From goal: ", len(visited_goal))

#zadanie puzzle
start_state = [[1, 2, 0], [5, 3, 4]]
goal_state = [[1, 2, 3], [4, 5, 0]]
start_root = Node(start_state, None, None)
goal_root = Node(goal_state, None, None)

start = time.time()

path = bidirectional_search(start_root, goal_root)

end = time.time()

print((end - start) * 1000, 'ms')

if path is not None:
    print(len(path) - 1)
    for i in path:
        for j in i.key:
            print(j)
        print(i.move)

