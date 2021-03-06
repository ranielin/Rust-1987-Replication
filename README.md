# Rust (1987) Replication

Replication of the single-agent dynamic programming problem of optimal bus engine replacement in [Rust (1987)](https://www.econometricsociety.org/publications/econometrica/1987/09/01/optimal-replacement-gmc-bus-engines-empirical-model-harold). The code provided replicates the point estimates of the model parameters for the simple linear cost function specification (first four rows of the "Groups 1, 2, 3, 4" column of Table IX) in Rust (1987).

This replication estimates the model using Rust's Nested Fixed Point Algorithm (NFXP), a full-solution method that is computationally burdensome: the DP problem must be solved for each value of model parameters that is searched over. For alternative estimation methods and/or extensions of the single-agent Rust model to models of dynamic games, the following resources may be helpful:
* [Aguirregabiria and Mira (2010)](http://aguirregabiria.net/wpapers/survey_annalsje.pdf) for a comprehensive overview of several estimation methods for dynamic discrete choice models
* [Arcidiacono and Ellickson (2011)](https://www.annualreviews.org/doi/abs/10.1146/annurev-economics-111809-125038) for a practical guide to conditional choice probability (CCP) estimation methods
* [Aguirregabiria, Collard-Wexler, and Ryan (2021)](https://arxiv.org/abs/2109.01725) for multiple-agent dynamic game models

A walkthrough of this replication can be found [here](https://ranielin.github.io/files/rust.html).

### Data

Data on bus engine replacement schedules and mileage is obtained from the ["companion web page"](http://individual.utoronto.ca/vaguirre/wpapers/program_code_survey_joe_2008.html) to Aguirregabiria and Mira (2010). Data from bus groups 1 through 4 are combined, which correspond to data files "g870.asc", "rt50.asc", "t8h203.asc", and "a530875.asc", respectively.

Following Rust (1987), the mileage state variable ![equation](https://latex.codecogs.com/svg.image?x_t) is discretized into bins of ![equation](https://latex.codecogs.com/svg.image?5000) mi., i.e., ![equation](https://latex.codecogs.com/svg.image?x_t&space;=&space;0) if the mileage accumulated is between ![equation](https://latex.codecogs.com/svg.image?0) and ![equation](https://latex.codecogs.com/svg.image?5000), ![equation](https://latex.codecogs.com/svg.image?x_t&space;=&space;1) if the mileage accumulated is between ![equation](https://latex.codecogs.com/svg.image?5000) and ![equation](https://latex.codecogs.com/svg.image?10000), and so on. The mileage accumulated is the current mileage minus the mileage at the last engine replacement and the decision variable ![equation](https://latex.codecogs.com/svg.image?i_t) is simply a binary indicator that equals ![equation](https://latex.codecogs.com/svg.image?1) if the engine is replaced in time ![equation](https://latex.codecogs.com/svg.image?t) and ![equation](https://latex.codecogs.com/svg.image?0) otherwise.

### Estimation of Transition Matrix

The state transition density ![equation](https://latex.codecogs.com/svg.image?p(x_{t&plus;1}&space;|&space;x_t,&space;i_t,&space;\theta_3)) is characterized by two parameters:
- ![equation](https://latex.codecogs.com/svg.image?\theta_3_0), the probability that ![equation](https://latex.codecogs.com/svg.image?x_{t&plus;1}&space;-&space;x_{t}) is equal to zero given ![equation](https://latex.codecogs.com/svg.image?i_t&space;=&space;0)
- ![equation](https://latex.codecogs.com/svg.image?\theta_3_1), the probability that ![equation](https://latex.codecogs.com/svg.image?x_{t&plus;1}&space;-&space;x_{t}) is equal to one given ![equation](https://latex.codecogs.com/svg.image?i_t&space;=&space;0)

These paremeters are empirically estimated directly from the data as ![equation](https://latex.codecogs.com/svg.image?\text{freq}(x_{t&plus;1}&space;-&space;x_t&space;=&space;j&space;|&space;i_t&space;=&space;0,&space;x_{t&plus;1}&space;-&space;0&space;=&space;j&space;|&space;i_t&space;=&space;1)) for ![equation](https://latex.codecogs.com/svg.image?j&space;=&space;0,&space;1).

The transition matrix ![equation](https://latex.codecogs.com/svg.image?P) is an ![equation](https://latex.codecogs.com/svg.image?S&space;\times&space;S) matrix whose ![equation](https://latex.codecogs.com/svg.image?[j,&space;k])'th entries denote the estimated probabilities of transitioning from state ![equation](https://latex.codecogs.com/svg.image?j) to state ![equation](https://latex.codecogs.com/svg.image?k), conditional on the decision ![equation](https://latex.codecogs.com/svg.image?i&space;=&space;0), where ![equation](https://latex.codecogs.com/svg.image?S&space;=&space;90) denotes the size of the state space.

### Expected Value Function Contraction

For given values of the utility function parameters ![equation](https://latex.codecogs.com/svg.image?\theta) and discount rate ![equation](https://latex.codecogs.com/svg.image?\beta), the iterative contraction mapping

![equation](https://latex.codecogs.com/svg.image?EV^{new}&space;=&space;P&space;[\log&space;(\sum_{j&space;=&space;0,&space;1}&space;\exp(\bar&space;u(\cdot,&space;j;&space;\theta)&space;&plus;&space;\beta&space;EV^{old}))]) 

is applied with initial guess ![equation](https://latex.codecogs.com/svg.image?EV=0), where
- ![equation](https://latex.codecogs.com/svg.image?EV) is a length ![equation](https://latex.codecogs.com/svg.image?S) vector denoting the expected value function of choice ![equation](https://latex.codecogs.com/svg.image?i&space;=&space;0) at each state ![equation](https://latex.codecogs.com/svg.image?x=0,\dots,S-1)
- ![equation](https://latex.codecogs.com/svg.image?\bar&space;u(\cdot,&space;j;&space;\theta)) is a length ![equation](https://latex.codecogs.com/svg.image?S) vector denoting the current-period utility (minus the structural error) of making choice ![equation](https://latex.codecogs.com/svg.image?j) at each state ![equation](https://latex.codecogs.com/svg.image?x=0,\dots,S-1)
- ![equation](https://latex.codecogs.com/svg.image?P) is an ![equation](https://latex.codecogs.com/svg.image?S&space;\times&space;S) transition matrix.

The iteration proceeds until ![equation](https://latex.codecogs.com/svg.image?\left\|&space;EV^{new}&space;-&space;EV^{old}\right\|&space;<&space;10^{-6}). Note that at any state, the expected value function evaluated for the choice ![equation](https://latex.codecogs.com/svg.image?i&space;=&space;1) is equal to the expected value function evaluated for the choice ![equation](https://latex.codecogs.com/svg.image?i&space;=&space;0) at state ![equation](https://latex.codecogs.com/svg.image?x&space;=&space;0), so the expected value function can be represented as an ![equation](https://latex.codecogs.com/svg.image?S&space;\times&space;1) vector rather than an ![equation](https://latex.codecogs.com/svg.image?S&space;\times&space;2) matrix.

As shown in Rust (1987), this sequence of expected values converges to the expected value function ![equation](https://latex.codecogs.com/svg.image?\mathbb{E}_{x',&space;\epsilon'&space;|&space;x,&space;i}[V(x',&space;\epsilon';&space;\theta)]), where ![equation](https://latex.codecogs.com/svg.image?V(\cdot)) is the value function (i.e., the maximum utility flow obtained from the optimal decision sequence as a function of the state variable and structural error).

### Dynamic Logit Choice Probabilities

Under the standard distributional assumption that the error terms ![equation](https://latex.codecogs.com/svg.image?\epsilon_t) are distributed i.i.d. Type I extreme value, choice probabilities conditional on the state variables are of the the dynamic logit form ![equation](https://latex.codecogs.com/svg.image?P(i&space;|&space;x;&space;\theta)&space;=&space;\frac{\exp(\bar&space;u(x,&space;i;&space;\theta)&space;&plus;&space;\beta&space;EV(x,&space;i))}{\sum_{j&space;=&space;0,&space;1}&space;\exp(\bar&space;u(x,&space;j;&space;\theta)&space;&plus;&space;\beta&space;EV(x,&space;j))}).

### Partial Maximum Likelihood Estimation

The likelihood objective function to maximize is 
![equation](https://latex.codecogs.com/svg.image?l(\theta)&space;=&space;\sum_{t}&space;P(i_t&space;|&space;x_t;&space;\theta)&space;&plus;&space;\sum_{t}&space;P(x_t&space;|&space;x_{t&space;-&space;1},&space;i_{t&space;-&space;1};&space;\theta_3)), where the summation is taken over all independent observations. The second component of this log-likelihood function is maximized when the parameters ![equation](https://latex.codecogs.com/svg.image?\theta_3) are estimated in the construction of the transition matrix ![equation](https://latex.codecogs.com/svg.image?P). Taking the estimates ![equation](https://latex.codecogs.com/svg.image?\hat&space;\theta_3) as given, the remaining parameters in ![equation](https://latex.codecogs.com/svg.image?\theta) are then estimated by maximizing the first component of this log-likelihood function (i.e., the partial likelihood).

These partial maximum likelihood estimates are consistent for ![equation](https://latex.codecogs.com/svg.image?\theta) but not efficient. As explained in Rust (1987), a consistent estimate for ![equation](https://latex.codecogs.com/svg.image?\theta) can be obtained by re-estimating the full likelihood function jointly with respect to all the parameters using the original partial likelihood estimates as starting values, although there does not appear to be much difference between these estimates and the original estimates.