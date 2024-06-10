#!/bin/sh

#SBATCH --export=ALL
#SBATCH --chdir=/lustre/aoc/observers/nm-12934/VLA_Perseus/scripts
#SBATCH --time=8-0:0:0
#SBATCH --mem=256G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16

CASAPATH=/home/casa/packages/RHEL7/release/current/bin/
# CASAPATH=/opt/local/bin/

# Get the number of available cores on the node
available_cores=$(sinfo -N -l | grep -m 1 "idle" | awk '{print $4}')

if [ "$available_cores" -lt 16 ]; then
    echo "Not enough slots available, reducing the number of tasks to $available_cores"
    ntasks=$available_cores
else
    ntasks=16
fi

# Run CASA with xvfb for virtual frame buffer support
xvfb-run -d ${CASAPATH}/mpicasa -n $ntasks ${CASAPATH}/casa --nogui --nologger --log2term /lustre/aoc/observers/nm-12934/VLA-Perseus/scripts/10_make_images_concat_spw.py >> file.txt 2>&1
