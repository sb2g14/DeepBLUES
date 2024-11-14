#!/usr/bin/env Rscript

library(vcfR) ## see: https://github.com/knausb/vcfR
library(LDheatmap) ## see: https://sfustatgen.github.io/LDheatmap/index.html
## LDheatmap is better installed from GitHub with:
## devtools::install_github("SFUStatgen/LDheatmap")
library(data.table)
library(snpStats) ## converts genotypes to LD matrix
library(ggplot2)

## for this example we select a subset of SNPs since 11k x 11k LD matrix is not
## visualisable
# snp.sel <- 2031

## set parameters
wd <- getwd()
vcf.file <- file.path(wd, "p1_2kb.vcf.gz")
ld.plot.file <- file.path(wd, "ld.plot_2kb.png")

## read VCF to R
snp <- read.vcfR(vcf.file)

## extract genotypes
gt <- snp@gt
gt <- t(gt) ## transpose

## remove FORMAT row and select first N SNPs
gt <- gt[2:nrow(gt), ]

#' Convert the matrix of genotypes to a numeric matrix in which genotypes are
#' coded as 0, 1 or 2 copies of the minor allele.
#'
#' @param x Matrix with genotypes to be converted to numeric format
#'
#' @return Matrix with numeric genotypes.
convert2numeric <- function(x) {
    gdat <- matrix(NA, nrow=nrow(x), ncol=ncol(x))
    for (m in 1:nrow(x)) {
        for (n in 1:ncol(x)) {
          a <-as.numeric(unlist(strsplit(x[m,n], "|"))[1])
          b <- as.numeric(unlist(strsplit(x[m,n], "|"))[3])
          gdat[m,n] <- a + b
        }
    }
    rownames(gdat) <- rownames(x)
    colnames(gdat) <- colnames(x)
    return(gdat)
}

## convert to numeric
gdat <- convert2numeric(gt)

## get SNP chromosome and position in data.table format (see vcfR docs:
## https://knausb.github.io/vcfR_documentation/vcf_data.html)
map <- data.table(chrom=as.numeric(snp@fix[, 1]), pos=as.numeric(snp@fix[, 2]))

## create SNP names as chrom_pos
map[, name := paste0(chrom, "_", pos)]

## assign names to the SNPs in gdat matrix
colnames(gdat) <- map[, name]

## convert to SnpMatrix object so that LDheatmap could compute LD correlations
gdat_for_ld <- as(gdat, "SnpMatrix")

## plot correlation matrix (takes a while given the size of the data)
plot <- LDheatmap(gdat_for_ld, genetic.distances=map[, pos],
                  title='LD heatmap', add.map=FALSE, color=heat.colors(20),
                  flip=TRUE)
                  
## save plot to PNG file
ggsave(ld.plot.file, plot$LDheatmapGrob)
