#!/bin/sh

# SBATCH --export=ALL                          # Export all environment variables to job
# SBATCH --chdir=/lustre/aoc/observers/nm-12934/VLA_Perseus # Working directory
# SBATCH --time=8-0:0:0                        # Request 8days
# SBATCH --mem=128G                            # Memory for the whole job
# SBATCH --nodes=1                             # Request 1 node
# SBATCH --ntasks-per-node=8                   # Request 8 cores

CASAPATH=/opt/local/bin/casa/ # Use a specific version of CASA
# xvfb-run -d mpicasa ${CASAPATH}/bin/casa --nogui -c /lustre/aoc/observers/nm-12934/VLA-Perseus/scripts/10_make_images.py >>file.txt 2>&1
xvfb-run -d ${CASAPATH}/mpicasa --oversubscribe ${CASAPATH}/casa --nogui -c /lustre/aoc/observers/nm-12934/VLA-Perseus/scripts/10_make_images.py >>file.txt 2>&1