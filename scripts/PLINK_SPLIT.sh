#!/bin/bash -l
#SBATCH --job-name=PLINK_SPLIT_CHR
#SBATCH --mem-per-cpu=4000
#SBATCH --time=01:00:00
#SBATCH --array=1-22
#SBATCH --account=mignot
./bin/plink --bfile test --chr $SLURM_ARRAY_TASK_ID --make-bed --out test_CHR$SLURM_ARRAY_TASK_ID
