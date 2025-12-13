# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VLA-Perseus is a radio astronomy data processing pipeline for VLA (Very Large Array) observations of the Perseus molecular cloud. The project focuses on polarization calibration and imaging of radio continuum data, with subsequent analysis of line-of-sight magnetic fields using Faraday rotation.

## Architecture

### Main Pipeline (`scripts/`)

The numbered scripts form a sequential processing pipeline that must be run in order within CASA (Common Astronomy Software Applications):

1. **Data Initialization** (`1_initialize_data.py`) - Extracts tar archives, copies MS files to products directory, restores flag versions, applies calibration tables, runs rflag/tfcrop flagging, and splits calibrated data
2. **Manual Flagging** (`2_manual_flagging.py`) - Interactive flagging
3. **Calibrator Parameters** (`3_calibrator_parameters.py`) - Sets up calibrator source parameters
4. **Flux Calibration** (`4_setjy.py`) - Sets flux density scale
5. **Gain Calibration** (`5_gaincal.py`) - Cross-hand delay calibration (KCROSS)
6. **Polarization Calibration** (`6_polcal_df.py`, `7_polcal_xf.py`) - D-term and X-Y phase calibration
7. **Apply Calibration** (`8_applycal_final.py`) - Applies all calibration tables
8. **Split Targets** (`9_split.py`) - Extracts target fields to `targets.ms`
9. **Imaging** (`10_make_images*.py`) - tclean imaging with mosaic gridder for Stokes I/Q/U
10. **Post-processing** (`11_smooth.py`, `12_exportfits.py`) - Image smoothing and FITS export
11. **Analysis** (`16_source_detection.py`, `17-flux-extract.py`, `18_merge_table.py`) - Source detection and flux extraction

### Configuration (`scripts/configs.py`)

Central configuration file containing observation-specific parameters:
- `path` - Data directory path
- `msfilename` - Measurement set filename
- `refant_name` - Reference antenna (e.g., 'ea23', 'ea24')
- `phase_center` - Mosaic phase center in J2000 coordinates
- `thresh` - Clean threshold
- `nit` - Number of clean iterations
- `pblim` - Primary beam limit

Switch between observations by uncommenting the appropriate configuration block.

### MC-BLOS Submodule (`MC-BLOS/`)

Separate analysis package for calculating line-of-sight magnetic field strengths from Faraday rotation. Run via `MC-BLOS/MolecularClouds/Run.py` which executes scripts 01-07 sequentially.

## Running Scripts

Scripts must be run within CASA environment:

```bash
# From scripts directory
casa --nologger -c 1_initialize_data.py
casa --nologger -c 5_gaincal.py
casa --nologger -c 10_make_images.py
```

For non-CASA scripts (source detection, analysis):
```bash
python 16_source_detection.py
```

## Key Dependencies

- CASA 6.x (provides `tclean`, `gaincal`, `polcal`, `flagdata`, `split`, `imsmooth`, `exportfits`)
- Python packages: astropy, numpy, pandas, scipy, matplotlib, rm-tools, reproject

## Data Organization

```
../data/
├── [observation_id]/
│   └── products/
│       ├── *.ms (measurement sets)
│       └── *.tbl (calibration tables)
└── concat/
    └── [phase_center]/
        ├── targets.ms
        └── Images/img5000/
            ├── tclean/
            ├── smo/
            └── fits/
```

## Important Patterns

- Spectral windows (spw) 2-6, 8-10, 15-17 are typically used (avoiding RFI-contaminated channels)
- Channel ranges split into 8-channel blocks: `00~07`, `08~15`, ..., `56~63`
- Stokes parameters processed: I (total intensity), Q, U (linear polarization)
- Imaging uses mosaic gridder with Briggs weighting (robust=0.5)
- Images smoothed to common resolution (typically 60 arcsec) before polarization analysis
