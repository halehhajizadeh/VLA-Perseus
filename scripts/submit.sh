#!/bin/sh

#SBATCH --export=ALL                          # Export all environment variables to job
#SBATCH --chdir=/lustre/aoc/observers/nm-12934/VLA_Perseus/scripts # Working directory
#SBATCH --time=8-0:0:0                        # Request 8 days
#SBATCH --mem=256G                            # Memory for the whole job
#SBATCH --nodes=5                             # Request 1 node
#SBATCH --ntasks-per-node=8                   # Request 8 cores (adjust if necessary)
#SBATCH --cpus-per-task=2                     # Use hardware threads (adjust if necessary)
#SBATCH --oversubscribe                       # Allow oversubscription

CASAPATH=/home/casa/packages/RHEL7/release/current/bin/ # Use a specific version of CASA

xvfb-run -d ${CASAPATH}mpicasa --map-by :OVERSUBSCRIBE -n 16 ${CASAPATH}casa -c --nogui /lustre/aoc/observers/nm-12934/VLA-Perseus/scripts/10_make_images_concat_spw.py >>file.txt 2>&1
