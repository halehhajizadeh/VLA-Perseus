#!/bin/sh

# SBATCH --export=ALL                          # Export all environment variables to job
# SBATCH --chdir=/lustre/aoc/observers/nm-12934/VLA_Perseus # Working directory
# SBATCH --time=8-0:0:0                        # Request 8days
# SBATCH --mem=256G                            # Memory for the whole job
# SBATCH --nodes=3                            # Request 1 node
# SBATCH --ntasks-per-node=16                   # Request 8 cores


CASAPATH=/home/casa/packages/RHEL7/release # Use a specific version of CASA
# CASAPATH=/opt/local/bin/

xvfb-run -d ${CASAPATH}/current/bin/mpicasa ${CASAPATH}/current/bin/casa --nogui -c /lustre/aoc/observers/nm-12934/VLA-Perseus/scripts/10_make_images_concat_spw.py >>file.txt 2>&1