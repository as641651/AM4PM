#!/usr/local_rwth/bin/zsh

# ask for 10 GB memory
#SBATCH --mem-per-cpu=2560M

# name the job
#SBATCH --job-name=75_75_6_75_75_T4

# declare the merged STDOUT/STDERR file
#SBATCH --output=logs/75_75_6_75_75_T4_output.%J.txt

#SBATCH -A aices
#SBATCH --time 03:00:00
#SBATCH --cpus-per-task=4
#SBATCH --threads-per-core=1
##SBATCH --exclusive

source $HOME/.analyzer
lscpu
eval "$1 $2"





