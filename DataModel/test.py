import random



def recursive_search(depGraph, temp_list, perm_list, current_package):
    if current_package not in depGraph.keys():
        perm_list.append(current_package)
        return
    elif current_package in perm_list:
        return
    else:
        temp_list.append(current_package)
        for package in depGraph[current_package]:
            if package not in perm_list:
                recursive_search(depGraph, temp_list, perm_list, package)
        perm_list.append(current_package)
        return



def depGraphSolver(depGraph : dict):
    temp_list = []
    perm_list = []
    while(len(list(set(depGraph.keys()) - set(perm_list)))>0):
        current_package = random.choice(list(depGraph.keys()))
        print(f"{current_package = }")
        recursive_search(depGraph, temp_list, perm_list, current_package)
    return current_package, perm_list


if __name__ == "__main__":
    """
        ->b ->d
       /
    a
      \
    h->  -> c -> f
    """
    depGraph = {"a": ['b', 'c'], "b": ['d'], 'c': ['f'], 'h': ['c']}
    print(depGraphSolver(depGraph))
