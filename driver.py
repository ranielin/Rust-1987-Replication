import pandas as pd
import numpy as np

from transition import *
from compute_EV import *

# np.random.seed(123)

# load data
X = np.array(pd.read_csv("./data/estimation/bus_dat.csv"))[:, 0]
I = np.array(pd.read_csv("./data/estimation/bus_dat.csv"))[:, 1]
delta = np.array(pd.read_csv("./data/estimation/bus_dat.csv"))[:, 2]

S = 90 # number of states
A = 2 # number of actions
x = np.arange(S, dtype = np.float64) # state space vector

# get transition matrix
P = transition(S, delta)

# test compute EV
# tol = 1e-6
# theta = np.array((3.6, 10))
# beta = 0.9999
# EV = compute_EV(tol, theta, beta, P, x)