library(data.table)

setwd("../SLiM/results/")
path <- getwd()

file.name <- "sequences_bal.cf"
VCF <- fread(file.name)


data1 <- VCF[VCF$POS <= nrow(VCF)/2]
data2 <- VCF[VCF$POS > nrow(VCF)/2]

file.out1 <- "sequences_bal_1.cf"
counts.file1 <-  file.path(path, file.out1)

writeLines(paste0("COUNTSFILE NPOP ", ncol(data1)-2, " NSITES ", nrow(data1)), counts.file1)
fwrite(data1, counts.file1, col.names = TRUE, append=TRUE, quote=FALSE, sep=" ")

file.out2 <- "sequences_bal_2.cf"
counts.file2 <-  file.path(path, file.out2)

writeLines(paste0("COUNTSFILE NPOP ", ncol(data2)-2, " NSITES ", nrow(data2)), counts.file2)
fwrite(data2, counts.file2, col.names = TRUE, append=TRUE, quote=FALSE, sep=" ")
