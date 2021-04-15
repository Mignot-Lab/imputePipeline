# Imputation pipeline used in the mignot lab
This is slurm job dependent pipeline that takes in base plink format bed files, splits them into chromosomes ( 1 to 22) and then phases them using shapeit, after phasing each chromosome is imputed to 1000 genomes phase 3 in 1mb chunks
# New added support for custom chr range
All chromsomes `-CHR 1-22`, single chromosome `-CHR 1` or a custom range `-CHR 2,3,21`  
# Dependancies
plink/1.90
 shapeit
 impute2
# example command to impute phase3
```python scripts/imputePipe.py -F plink_binary -Ref 3 -CHR 1-22```
