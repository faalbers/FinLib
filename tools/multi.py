from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

def exec(poolVariables, multiProc):
    cpuCount = cpu_count() * 4
    multiPool = Pool(cpuCount)
    return multiPool.map(multiProc, poolVariables)


