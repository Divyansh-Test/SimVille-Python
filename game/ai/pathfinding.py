import heapq


def heuristic(a, b):
    return abs(abs(a[0] - b[0]) + abs(a[1] - b[1]))


def pathfinding(grid, start, goal):
    start=tuple(start)
    goal=tuple(goal)
    way = {}
    openset = []    
    heapq.heappush(openset, (0, start))
    
    row = len(grid)
    col = len(grid[0])
    g_score = {start: 0}
    direction = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while openset:
        _, current = heapq.heappop(openset)
        

        if current == goal:
            path = []
            
            while current in way:
                
                path.append(current)
                current = way[current]

            
            return path

        for dx, dy in direction:
            neighbour = (current[0] + dx, current[1] + dy)
            if not (0 <= neighbour[0] < row and 0 <= neighbour[1] < col):
                
                continue
            if grid[neighbour[0]][neighbour[1]] != 0:
                continue

            tentative_g = g_score[current] + 1
            if neighbour not in g_score or tentative_g < g_score[neighbour]:
                # print("here in teh if state.")
                way[neighbour] = current
                # print("This is",neighbour,current)
                g_score[neighbour] = tentative_g
                f_score = tentative_g + heuristic(neighbour, goal)
                heapq.heappush(openset, (f_score, neighbour))

    return None



if  __name__=="__main__":
     grid=[[0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0]]
     start=(0,0)
     goal=(9,9)
     path=pathfinding(grid,start,goal)
     print(path)