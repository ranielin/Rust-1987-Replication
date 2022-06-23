import pandas as pd
import numpy as np
import scipy.optimize

from transition import *
from objective import *

# load data
X = np.array(pd.read_csv("./data/estimation/bus_dat.csv"))[:, 0]
I = np.array(pd.read_csv("./data/estimation/bus_dat.csv"))[:, 1]
delta = np.array(pd.read_csv("./data/estimation/bus_dat.csv"))[:, 2]

S = 90 # number of states
x = np.arange(S, dtype = np.float64) # state space vector

# estimate transition probabilities theta_3 to build transition matrix
P = transition(S, delta)

# maximize partial log-likelihood
tol = 1e-6
beta = 0.9999
theta_1_start = np.array((2.6275, 9.7558))
bounds = ((0, np.inf),) * theta_1_start.shape[0]

p_ll = scipy.optimize.minimize(objective, theta_1_start, args = (
    x, P, beta, tol, X, I
    ), method = 'L-BFGS-B', bounds = bounds, options = {
        'maxiter': 1000})

# write parameter estimates to .csv
theta = np.insert(p_ll.x, [2, 2], [P[0, 0], P[0, 1]])
theta_df = pd.DataFrame(theta)
theta_df.insert(0, "var", [
    "theta_1_1", "RC", "theta_3_0", "theta_3_1"])
theta_df.rename({0:'est'}, axis = 1, inplace = True)
theta_df.to_csv("./output/theta_est.csv", sep = ",", index = False)