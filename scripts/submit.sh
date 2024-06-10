#!/bin/sh

#SBATCH --export=ALL
#SBATCH --chdir=/lustre/aoc/observers/nm-12934/VLA_Perseus/scripts
#SBATCH --time=8-0:0:0
#SBATCH --mem=256G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8

CASAPATH=/home/casa/packages/RHEL7/release/current/bin/


# Run CASA with xvfb for virtual frame buffer support
xvfb-run -d ${CASAPATH}/mpicasa -n 8 $ntasks ${CASAPATH}/casa --nogui --nologger /lustre/aoc/observers/nm-12934/VLA-Perseus/scripts/10_make_images_concat_spw.py >> file.txt 2>&1
