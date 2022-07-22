#!/usr/local_rwth/bin/zsh

# ask for 10 GB memory
#SBATCH --mem-per-cpu={memory}M

# name the job
#SBATCH --job-name={job_name}

# declare the merged STDOUT/STDERR file
#SBATCH --output=logs/{job_name}_output.%J.txt

#SBATCH -A aices
#SBATCH --time 03:00:00
#SBATCH --cpus-per-task={threads}
#SBATCH --threads-per-core=1
##SBATCH --exclusive

source $HOME/.analyzer
lscpu
eval "$1 $2"





