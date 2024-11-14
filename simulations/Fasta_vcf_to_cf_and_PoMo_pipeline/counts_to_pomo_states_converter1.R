# This script reads a count file and creates a PoMo alignment in the "NaturalNumbers" type that can be uploaded into RevBayes.

# setting the working directory
setwd("../SLiM/results/")

# install.packages("Rcpp")  
library("Rcpp")

# uploading the function counts_to_pomo_states_converter
sourceCpp("../../Fasta_vcf_to_cf_and_PoMo_pipeline/weighted_sampled_method.cpp")

name <- "sequences_bal_1"
count_file <- paste0(name, ".cf")     # count file
n_alleles  <- 4                        # the four nucleotide bases A, C, G and T
N          <- 10                        # virtual population size

alignment <- counts_to_pomo_states_converter(count_file,n_alleles,N)

# writing the PoMo alignment
writeLines(alignment,paste0(name, ".txt"))
