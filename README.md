# Rust (1987) Replication

Replication of the single-agent dynamic programming problem of optimal bus engine replacement in [Rust (1987)](https://www.econometricsociety.org/publications/econometrica/1987/09/01/optimal-replacement-gmc-bus-engines-empirical-model-harold). The code provided replicates the point estimates of the model parameters for the simple linear cost function specification (first four rows of the "Groups 1, 2, 3, 4" column of Table IX) in Rust (1987).

This replication estimates the model using Rust's Nested Fixed Point Algorithm (NFXP), a full-solution method that is computationally burdensome: the DP problem must be solved for each value of model parameters that is searched over. For alternative estimation methods and/or extensions of the single-agent Rust model to models of dynamic games, the following resources may be helpful:
* [Aguirregabiria and Mira (2010)](http://aguirregabiria.net/wpapers/survey_annalsje.pdf) for a comprehensive overview of several estimation methods for dynamic discrete choice models
* [Arcidiacono and Ellickson (2011)](https://www.annualreviews.org/doi/abs/10.1146/annurev-economics-111809-125038) for a practical guide to conditional choice probability (CCP) estimation methods
* [Aguirregabiria, Collard-Wexler, and Ryan (2021)](https://arxiv.org/abs/2109.01725) for multiple-agent dynamic game models

### Data

Data on bus engine replacement schedules and mileage is obtained from the ["companion web page"](http://individual.utoronto.ca/vaguirre/wpapers/program_code_survey_joe_2008.html) to Aguirregabiria and Mira (2010). Data from bus groups 1 through 4 are combined, which correspond to data files "g870.asc", "rt50.asc", "t8h203.asc", and "a530875.asc", respectively.

Following Rust (1987), the mileage state variable is discretized into bins of 5000 mi., i.e., 0 if the mileage accumulated is between 0 and 5000, 1 if the mileage accumulated is between 5000 and 10000, and so on. The mileage accumulated is the current mileage minus the mileage at the last engine replacement and the decision variable is simply a binary indicator that equals 1 if the engine is replaced in time t and 0 otherwise.

### Estimation of Transition Matrix

The state transition density is characterized by two parameters. The first parameter is the probability that the mileage state variable increment is equal to zero (given the decision variable is zero), and the second parameter is the probability that the mileage state variable increment is equal to zero (given the decision variable is zero).

These paremeters are empirically estimated directly from the data using the frequency of mileage increments conditional on no engine replacement. The transition matrix is an S by S matrix whose (j, k)'th entries denote the estimated probabilities of transitioning from state j to state k, conditional on the decision variable being equal to zero, where S = 90 denotes the size of the state space.

### Expected Value Contraction

For given values of the utility function parameter and discount rate, the iterative contraction mapping in Rust (1987) is applied with a tolerance level of 10e-6 and EV = 0 used as the initial guess, where EV denotes a length S vector of expected values (conditional on the decision variable being equal to zero) that the iteration is applied to. At any state, the expected value function when the decision variable is equal to one is the same as the expected value function when the decision variable is equal to zero and the state variable is equal to zero, so the expected value function can be represented as a length S vector rather than an S by 2 matrix.

As shown in Rust (1987), this sequence of expected values converges to the expected value function, which is the expectation of the value function (i.e., the maximum utility flow obtained from the optimal decision sequence as a function of the state variable and structural error), where the expectation is taken over all values of the state and error term variables conditional on the values of the state and error variable that the EV function is evaluated at.

### Dynamic Logit Choice Probabilities

Under the standard assumption that the error terms are distributed i.i.d. Type I extreme value, choice probabilities conditional on the state variables are of the the standard dynamic logit form. The probability of choice i, conditional on state x, is a function of decision i's current-period flow utility (less the structural error term) and the EV function evaluated at x and i, divided by that term plus the identical term but with choice j replacing choice i.

### Partial Maximum Likelihood Estimation

The likelihood objective function to maximize consists of both choice probabilities (conditional on the state variables) and transition probabilities (conditional on last period's state and decision), summed over all independent observations. The second component of the log-likelihood function is maximized when the transition parameters are estimated in the construction of the transition matrix. Taking these estimates as given, the remaining parameters are then estimated by maximizing the first component of the log-likelihood function (i.e., the partial likelihood).

The partial maximum likelihood estimates are consistent but not efficient. In Rust (1987), an efficient estimate is obtained by re-estimating the full likelihood function jointly with respect to all the parameters using the original partial likelihood estimates as starting values, although there is not a larrge difference between these estimates and the original estimates.