from collections import deque

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': []
}

start_node = 'A'   # Where the search begins
goal_node  = 'G'   # What we are looking for

# (i) BREADTH FIRST SEARCH (BFS)

def bfs(graph, start, goal):
    """
    Breadth First Search.
    Returns the path from start to goal, or None if not found.
    """
    queue = deque()
    queue.append((start, [start]))

    visited = set()          # Track visited nodes to avoid revisiting
    visited.add(start)

    print("── BFS Exploration Order ──")

    while queue:
        current, path = queue.popleft()   # Take from the FRONT of queue
        print(f"   Visiting: {current}  |  Path so far: {' → '.join(path)}")

        # Goal check
        if current == goal:
            return path

        # Add unvisited neighbours to the back of the queue
        for neighbour in graph[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))

    return None   # Goal not found

# (ii) DEPTH FIRST SEARCH (DFS)

def dfs(graph, start, goal):
    """
    Depth First Search.
    Returns the path from start to goal, or None if not found.
    """
    # Stack holds (current_node, path_so_far)
    stack = []
    stack.append((start, [start]))

    visited = set()          # Track visited nodes to avoid revisiting
    visited.add(start)

    print("── DFS Exploration Order ──")

    while stack:
        current, path = stack.pop()       # Take from the TOP of stack
        print(f"   Visiting: {current}  |  Path so far: {' → '.join(path)}")

        # Goal check
        if current == goal:
            return path

        # Add unvisited neighbours to the top of the stack
        for neighbour in reversed(graph[current]):   # reversed keeps left-to-right order
            if neighbour not in visited:
                visited.add(neighbour)
                stack.append((neighbour, path + [neighbour]))

    return None   # Goal not found

# RUN BOTH SEARCHES

print("=" * 55)
print("       Search & Optimization – BFS vs DFS")
print("=" * 55)
print(f"  Graph : {graph}")
print(f"  Start : {start_node}")
print(f"  Goal  : {goal_node}")
print("=" * 55)
print()

print("[ BREADTH FIRST SEARCH (BFS) ]")
print("Strategy: Explore level by level using a QUEUE\n")
bfs_path = bfs(graph, start_node, goal_node)
print()
if bfs_path:
    print(f"✅ BFS Goal '{goal_node}' found!")
    print(f"   Path: {' → '.join(bfs_path)}")
    print(f"   Steps: {len(bfs_path) - 1}")
else:
    print(f"❌ BFS: Goal '{goal_node}' not reachable.")

print()
print("-" * 55)
print()

# DFS
print("[ DEPTH FIRST SEARCH (DFS) ]")
print("Strategy: Explore deep first using a STACK\n")
dfs_path = dfs(graph, start_node, goal_node)
print()
if dfs_path:
    print(f"✅ DFS Goal '{goal_node}' found!")
    print(f"   Path: {' → '.join(dfs_path)}")
    print(f"   Steps: {len(dfs_path) - 1}")
else:
    print(f"❌ DFS: Goal '{goal_node}' not reachable.")

print()
print("=" * 55)
print("COMPARISON SUMMARY")
print("=" * 55)
print(f"  {'Algorithm':<10} {'Path':<30} {'Steps'}")
print(f"  {'-'*48}")
if bfs_path:
    print(f"  {'BFS':<10} {' → '.join(bfs_path):<30} {len(bfs_path)-1}")
if dfs_path:
    print(f"  {'DFS':<10} {' → '.join(dfs_path):<30} {len(dfs_path)-1}")
print()
print("Key Differences:")
print("  BFS → Uses a QUEUE, explores level by level, finds SHORTEST path")
print("  DFS → Uses a STACK, explores deep first, faster in some cases")
print("=" * 55)
