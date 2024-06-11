#!/bin/sh

#SBATCH --export=ALL                          # Export all environment variables to job
#SBATCH --chdir=/lustre/aoc/observers/nm-12934/VLA_Perseus/scripts # Working directory
#SBATCH --time=8-0:0:0                        # Request 8 days
#SBATCH --mem=256G                            # Memory for the whole job
#SBATCH --nodes=1                          # Request 1 node
#SBATCH --ntasks-per-node=16                   # Request 8 cores (adjust if necessary)


CASAPATH=/home/casa/packages/RHEL7/release/current/bin/ # Use a specific version of CASA


xvfb-run -d ${CASAPATH}mpicasa --oversubscribe -n 16 ${CASAPATH}casa --nogui -c /lustre/aoc/observers/nm-12934/VLA-Perseus/scripts/10_make_images_concat_spw.py >>file.txt 2>&1
