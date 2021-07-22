#!/bin/bash 
touch QCTOOL_SORT.sh
chmod 755 QCTOOL_SORT.sh
cat > QCTOOL_SORT.sh <<- EOF
#!/bin/bash -l
#SBATCH --job-name=QCTOOL_TASK_$4
#SBATCH --mem-per-cpu=64000
#SBATCH --time=120:00:00
#SBATCH --account=mignot
module load qctool/v2.0.1
qctool_v2.0.1 \\
-filetype gen \\
-sort \\
-g $1 \\
-s $2 \\
-og $3_SORTED.bgen \\
-os $3_SORTED.sample \\
EOF
sbatch QCTOOL_SORT.sh
