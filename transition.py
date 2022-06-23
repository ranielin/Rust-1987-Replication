import numpy as np

def transition(S, delta):
    """
    construct transition matrix for the Rust model with empirical probabilities
    of the three possible state transitions (delta = 0, 1, or 2)

    inputs:
        S, number of possible states
        delta, vector of mileage increments
        
    output:
        P, S x S matrix with entries [i, j] containing the probability of 
            transitioning to state j from state i
    """

    # empirical probabilities of three state transitions
    theta_3_0 = sum(delta == 0) / delta.size
    theta_3_1 = sum(delta == 1) / delta.size
    theta_3_2 = 1 - theta_3_0 - theta_3_1

    P = np.zeros((S, S))

    # fill off-diagonals of transition matrix
    P[np.arange(0, S), np.arange(0, S)] = theta_3_0
    P[np.arange(0, S-1), np.arange(1, S)] = theta_3_1
    P[np.arange(0, S-2), np.arange(2, S)] = theta_3_2

    # adjust absorbing states to sum to 1
    P[S-1, S-1] = 1
    P[S-2, S-1] = 1 - theta_3_0

    return P