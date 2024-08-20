from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

def exec(poolVariables, multiProc, cpuCount=None):
    if cpuCount == None:
        cpuCount = cpu_count()
    multiPool = Pool(cpuCount)
    return multiPool.map(multiProc, poolVariables)


