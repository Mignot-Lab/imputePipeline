#!/bin/bash
mkdir -p phasedHaps
command="./bin/shapeit --input-bed bedFiles/"$1"_CHR\$SLURM_ARRAY_TASK_ID.bed bedFiles/"$1"_CHR\$SLURM_ARRAY_TASK_ID.bim bedFiles/"$1"_CHR\$SLURM_ARRAY_TASK_ID.fam \
-M /labs/mignot/IMPUTE_REFERENCE_PHASE3/genetic_map_chr\$SLURM_ARRAY_TASK_ID\_combined_b37.txt \
-O phasedHaps/"$1"_CHR\$SLURM_ARRAY_TASK_ID \
-T 8"
touch shapeit_array.sh
chmod 755 shapeit_array.sh
if [[ $3 -eq 0 ]]; then
cat > shapeit_array.sh <<- EOF
#!/bin/bash -l
#SBATCH --job-name=shapeit_array
#SBATCH --mem-per-cpu=10000
#SBATCH --time=120:00:00
#SBATCH --array=$2
#SBATCH --cpus-per-task=4
#SBATCH --account=mignot
$command
EOF
else
cat > shapeit_array.sh <<- EOF
#!/bin/bash -l
#SBATCH --job-name=shapeit_array
#SBATCH --mem-per-cpu=10000
#SBATCH --time=120:00:00
#SBATCH --array=$2
#SBATCH --depend=afterok:"$3"
#SBATCH --cpus-per-task=4
#SBATCH --account=mignot
$command
EOF
fi
sbatch shapeit_array.sh
