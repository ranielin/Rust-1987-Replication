import pandas as pd
import numpy as np

from transition import *

np.random.seed(123)

# load data
X = np.array(pd.read_csv("./data/estimation/bus_dat.csv"))[:, 0]
I = np.array(pd.read_csv("./data/estimation/bus_dat.csv"))[:, 1]
delta = np.array(pd.read_csv("./data/estimation/bus_dat.csv"))[:, 2]

S = 90 # number of states
A = 2 # number of actions

P = transition(delta, S) # get transition matrix

# np.savetxt("P.csv", P, delimiter = ",")