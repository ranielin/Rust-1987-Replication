import numpy as np

def compute_EV(tol, theta, beta, P, x):
    """
    compute expected value (EV) function for given values of
    model parameters by solving for the fixed point of the
    contraction mapping problem

    inputs:
        tol, tolerance at which to stop the iteration
        theta, vector of parameters associated with the utility/cost
            function
        beta, discount factor
        P, S x S transition matrix
        x, state space vector

    output:
        EV, length S vector encoding the expected value function for each
            state in x at the given parameters theta
    """

    theta_1_1 = theta[0] # linear cost parameter
    RC = theta[1] # replacement cost

    def B(EV):
        """
        Bellman operator to iterate on
        cost function: c(x, theta_1_1) = -0.001 * theta_1_1 * x
        utility functions: u(x, 0, theta_1_1) = c(x, theta_1_1),
        u(x, 1, theta_1_1) = c(x[0], theta_1_1) - RC

        inputs:
            EV, length S vector encoding the expected value function

        output:
            B, length S vector encoding the value B(EV)
        """
        
        # utility and value from continuing (without the error term)
        u_0 = u(theta_1_1, RC, x, 0)
        v_0 = u_0 + beta * EV
        
        # utility and value from replacing (without the error term)
        u_1 = u(theta_1_1, RC, x[0], 1)
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

def u(theta_1_1, RC, x, i):
    """
    compute current-period utility, less the structural error

    inputs:
        theta_1_1, linear cost function parameter
        RC, replacement cost
        x, state variable
        i, decision variable
    
    output:
        u, utility from choosing action i in state x
    """

    if i == 0:
        return -0.001 * theta_1_1 * x 
    elif i == 1:
        return -0.001 * theta_1_1 * x - RC 