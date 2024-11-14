#!/usr/bin/env python3

import sys, os
import msprime
import pyslim
import tskit
import numpy as np

def main():
    #if len(args) != 5:    #4 arguments
    #    return helpMsg

    #slim_tree_path = args[1]
    #slim_params_path = args[2]
    #N = int(args[3])
    #out_path = args[4]+".trees"

    #with open(slim_params_path, "r") as paramF:
    #    lines = paramF.readlines()

    slim_tree_path="/Users/Antoniopacheco/Documents/DeepBLUES-main/simulations/SLiM/results/slim_3482038883415201127.trees"
    print(slim_tree_path)
    out_path = "/Users/Antoniopacheco/Documents/DeepBLUES-main/simulations/SLiM/results/tree_out.trees"
    mu = 1.25e-8
    rho = 1.25e-8
    Ne_recap = 2000

    ts = tskit.load(slim_tree_path)
    print(ts)
    ts_recap = pyslim.recapitate(ts, recombination_rate=rho, ancestral_Ne=Ne_recap)
    print(ts_recap)
    sampN = np.random.choice(ts_recap.samples(), size=Ne_recap, replace=False)
    print(sampN)
    ts_samp = ts_recap.simplify(samples=sampN)
    print(ts_samp)

    ts_samp.dump(out_path)

    return 0

#sys.exit(main(sys.argv))
main()
