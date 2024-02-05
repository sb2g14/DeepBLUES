#!/usr/bin/env bash

#SBATCH --partition=long
#SBATCH --ntasks=24
#SBATCH --mem=15G
##SBATCH --cpus-per-task=20
#SBATCH --nodes=1
#SBATCH --mail-user=sb442@st-andrews.ac.uk
#SBATCH --mail-type=END,FAIL

# cd $TMPDIR
#
# cp -r /home/sbraiche/projects/uosa/Carolin_Kosiol/svitlana_braichenko/revbayes_pomos/non_reversible_run .
#
# cd non_reversible_run

mpirun rb-mpi rb_script1.Rev

#cp -r output3 /home/sbraiche/projects/uosa/Carolin_Kosiol/svitlana_braichenko/revbayes_pomos/non_reversible_run/


