import numpy as np

def compute_EV(x, P, theta, beta, tol):
    """
    solve the single-agent DP problem, computing the expected value (EV)
    function for given values of model parameters by finding the fixed point
    of the Bellman operator contraction

    inputs:
        x, state space vector
        P, S x S transition matrix
        theta, vector of parameters associated with the utility/cost
            functions
        beta, discount factor
        tol, tolerance at which to stop the iteration


    output:
        EV, length S vector encoding the expected value function for each
            state in x at the given parameters theta
    """

    def B(EV):
        """
        Bellman operator to iterate on

        inputs:
            EV, length S vector encoding the expected value function

        output:
            B, length S vector encoding the value B(EV)
        """
        
        # utility and value from continuing (without the error term)
        u_0 = u(x, 0, theta)
        v_0 = u_0 + beta * EV
        
        # utility and value from replacing (without the error term)
        u_1 = u(x[0], 1, theta)
        v_1 = u_1 + beta * EV[0]

        # subtract and re-add EV to avoid overflow issues
        G = np.exp(v_0 - EV) + np.exp(v_1 - EV) # social surplus function
        B = P @ (np.log(G) + EV) # Bellman operator

        return B

    EV_old = EV = np.zeros(P.shape[0]) # initial EV guess
    error = 1

    while error > tol:
        EV_old = EV
        EV = B(EV_old)
        error = np.max(np.abs(EV - EV_old))

    return EV

def u(x, i, theta):
    """
    compute current-period utility, less the structural error

    inputs:
        x, state variable
        i, decision variable
        theta, vector of parameters associated with the utility/cost
            functions
    
    output:
        u, utility from choosing action i in state x
    """

    theta_1_1 = theta[0] # linear cost parameter
    RC = theta[1] # replacement cost

    if i == 0:
        return -0.001 * theta_1_1 * x 
    elif i == 1:
        return -0.001 * theta_1_1 * x - RC 