# Imputation pipeline used in the mignot lab
This is slurm job dependent pipeline that takes in base plink format bed files, splits them into chromosomes ( 1 to 22) and then phases them using shapeit, after phasing each chromosome is imputed to 1000 genomes phase 3 in 1mb chunks
# Dependancies
plink/1.90
 shapeit
 impute2
# example command
```python imputePipe.py -F plink_binary```
