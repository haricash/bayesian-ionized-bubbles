import numpy as np

def quasar_zetafunc(M):
    """
    Input the array where we want to calculate the
    quasar reionization map. It will put it in the
    cell with highest density of dark matter.
    """
    zeta = 100

    M = M == M.max()
    M = np.int32(M)
    M = zeta * M