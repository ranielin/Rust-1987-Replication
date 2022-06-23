import numpy as np

from compute_EV import u

def choice_prob(x, theta, beta, EV):
    """
    compute dynamic logit choice probabilities conditional on 
    state variables

    inputs:
        x, length S vector of state variables
        theta, vector of parameters associated with the utility/cost
            functions
        beta, discount factor
        EV, length S vector of expected values
    
    output:
        Pr, S x 2 array whose entries [i, j] are the probabilities
            of choosing actions j = 0, 1 conditional on state i
    """
    
    # utility and value from continuing (without the error term)
    u_0 = u(x, 0, theta)
    v_0 = u_0 + beta * EV
        
    # utility and value from replacing (without the error term)
    u_1 = u(x, 1, theta)
    v_1 = u_1 + beta * EV[0]

    # subract max(EV) from exponents to avoid overflow issues
    Pr_0 = np.exp(v_0 - max(EV)) / (np.exp(v_0 - max(EV)) + np.exp(v_1 - max(EV)))
    Pr_1 = 1 - Pr_0

    Pr = np.transpose(np.array((Pr_0, Pr_1)))
    return Pr