#!/bin/bash

cd ../SLiM/results/vcf/
vcf_files=(p1.vcf.gz p2.vcf.gz p3.vcf.gz p4.vcf.gz)
python3 /Users/sb442/Documents/work/DataConversion/cflib/scripts/FastaVCFToCounts.py ../anc.fa.gz "${vcf_files[@]}" ../example_from_fasta_vcf.cf --merge --ploidy 2
