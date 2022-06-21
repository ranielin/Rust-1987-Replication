# organize and clean bus engine data obtained from
# Aguirregabiria and Mira's "Companion Web Page to
# Dynamic discrete choice structural models: A survey"

library(tidyverse)

# load data corresponding to bus groups 1 through 4 in Rust (1987)
df1 <- matrix(unlist(read.table("./data/raw/g870.asc")), nrow = 36, byrow = FALSE)
df2 <- matrix(unlist(read.table("./data/raw/rt50.asc")), nrow = 60, byrow = FALSE)
df3 <- matrix(unlist(read.table("./data/raw/t8h203.asc")), nrow = 81, byrow = FALSE)
df4 <- matrix(unlist(read.table("./data/raw/a530875.asc")), nrow = 128, byrow = FALSE)

clean_dat <- function(df){
  
  # odometer values at replacement
  od_rep_1 <- df[6, ]
  od_rep_2 <- df[9, ]
  
  # total mileage
  df <- df[12:nrow(df), ]
  
  # indicators for when mileage is above the odometer values at replacement
  rep_1 <- t(apply(df, 1, function(x) x >= od_rep_1) * as.vector(od_rep_1 > 0))
  rep_2 <- t(apply(df, 1, function(x) x >= od_rep_2) * as.vector(od_rep_2 > 0))
  
  # state variable: mileage since replacement, discretized increments of 5000 mi.
  x <- df - t(t(rep_1) * t(rep_2 == 0) * od_rep_1) -
    t(t(rep_2) * t(rep_1 == 0) * od_rep_2)
  x <- ceiling(x / 5000)
    
  # decision variable: engine replacement, i.e., mileage is above rep_1 or rep_2
  # in the current period but not in the prior period
  i <- ifelse(rbind(0, rep_1[2:nrow(rep_1), ] - rep_1[1:nrow(rep_1) - 1, ]) + 
    rbind(0, rep_2[2:nrow(rep_2), ] - rep_2[1:nrow(rep_2) - 1, ]) > 0, 1, 0)
  
  # delta: mileage increment from prior period, accounting for engine replacement
  delta <- rbind(0, x[2:nrow(x), ] - x[1:nrow(x) - 1, ] + x[1:nrow(x) - 1, ] * i[2:nrow(x), ]) 
  
  # return data frame with columns x (state), i (decision), and delta (increment)
  return(tibble(x = matrix(x, ncol = 1), i = matrix(i, ncol = 1), delta = matrix(delta, ncol = 1)))
}

df1 <- clean_dat(df1)
df2 <- clean_dat(df2)
df3 <- clean_dat(df3)
df4 <- clean_dat(df4)

bus_dat <- rbind(df1, df2, df3, df4)
write_csv(bus_dat, "./data/estimation/bus_dat.csv")
