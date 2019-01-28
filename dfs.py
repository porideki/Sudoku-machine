import time

def dfs(problem):

    start = time.time()

    found = {problem.get_start_state()}
    stack = [[problem.get_start_state()]]
    while stack:

        path = stack.pop()
        u = path[-1]  # path の最後のノード
        for v in problem.next_states(u):

            if (time.time() - start) > 120:
                print("TIMEOUT\n")
                return path + [v]

            if problem.is_goal(v):
                print(v)
                return path + [v]
            elif v not in found:
                found.add(v)
                stack.append(path + [v])
        
