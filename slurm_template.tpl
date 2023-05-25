#!/bin/bash -l
#SBATCH --job-name=${job_name}
# Specific course queue and max wallclock time
#SBATCH -t ${time_limit} -p ${partition} -c ${num_cores} -n ${num_tasks}

# Defaults on Barkla (but set to be safe)
## Specify the current working directory as the location for executables/files
#SBATCH -D ./
## Export the current environment to the compute node
#SBATCH --export=ALL

# load modules
## intel compiler
module load compilers/intel/2019u5 
module load mpi/intel-mpi/2019u5/bin


conda activate test

% for c in commands:
${c}
% endfor

echo Finished
