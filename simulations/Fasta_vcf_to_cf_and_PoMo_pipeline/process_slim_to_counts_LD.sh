#!/bin/bash

#
# ./process_diploids_4sp_remastered.sh
# ./generate_counts_file_diploids_4sp_remastered.sh

# mv ../SLiM/results/example_from_fasta_vcf.cf ../SLiM/results/sequences_bal.cf

Rscript create_separate_cfs.R
Rscript counts_to_pomo_states_converter1.R
Rscript counts_to_pomo_states_converter2.R
