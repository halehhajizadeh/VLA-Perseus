
thresh = '4e-4'
pblim = -0.001
nit = 2000
ms_file = '../data/new/data/test/24A-376.sb45387559.eb45519359.60419.617289120375_calibrated.ms'
img_filename = '../data/new/data/test/fourthimage'
phase_center = 'J2000 03:26:24.057 +30.35.58.881'


# Run tclean with specified parameters
tclean(
    vis=ms_file,
    field="PER_FIELD_*",
    timerange="",
    spw="",
    uvrange="",
    antenna="",
    observation="",
    intent="",
    datacolumn="corrected",
    imagename=img_filename,
    imsize=[4096],
    cell="2.5arcsec",
    phasecenter=phase_center,  # Pass the phasecenter dynamically
    stokes='I',
    specmode="mfs",
    gridder="awproject",
    mosweight=True,
    savemodel='modelcolumn',
    cfcache=f'/dev/shm/4.cf',
    pblimit=pblim,
    deconvolver="mtmfs",
    pbcor=True,
    weighting="briggs",
    robust=0.5,
    niter=nit,
    gain=0.1,
    # nsigma=3,
    threshold=thresh,
    cycleniter=200,
    # psfcutoff=0.5,
    cyclefactor=1,
    parallel=True,
    # psterm=True,
    nterms=2,
    rotatepastep=5.0,
    interactive=False
)



