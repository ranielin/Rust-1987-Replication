import numpy as np

from compute_EV import *
from choice_prob import *

def objective(theta, x, P, beta, tol, X, I):
    """
    compute partial log-likelihood objective function

    inputs:
        theta, vector of parameters associated with the utility/cost
            functions
        x, length S vector of state variables
        P, S x S transition matrix
        beta, discount factor
        tol, tolerance at which to stop the EV iteration
        X, vector of observed states in data
        I, vector of observed decisions in data

    output:
        LL, partial log-likelihood evaluated at theta
    """

    # solve for EV and conditional choice probabilities at theta
    EV = compute_EV(x, P, theta, beta, tol)
    Pr = choice_prob(x, theta, beta, EV)

    # compute partial likelihood function
    LL = 0
    for x_t, i_t in zip(X, I):
       LL += np.log(Pr[x_t, i_t])

    return -LL