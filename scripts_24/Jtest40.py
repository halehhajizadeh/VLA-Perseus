import os

# === Parameters ===
ms_file = '24A-376.sb45388185.eb45417364.60412.697942569444_calibrated.ms'
phasecenter = 'J2000 03:40:00.063 +32.23.58.799'
thresh = '9e-5'         # or whatever value you prefer
nit = 5000              # or your desired number of iterations
base_imgname = 'field'  # prefix for image name
imsize = [4096]
cell = '2.5arcsec'

# === Loop over each field ===
for i in range(55):
    field_str = str(i)
    img_filename = f'{base_imgname}_{field_str}'

    # Delete old files if they exist
    for suffix in ['.image', '.model', '.psf', '.residual', '.pb', '.mask', '.sumwt', '.weight', '.image.pbcor']:
        fname = f'{img_filename}{suffix}'
        if os.path.exists(fname):
            os.remove(fname)

    print(f'Running tclean for field {field_str} -> {img_filename}')
    tclean(
        vis=ms_file,
        field=field_str,
        timerange="",
        spw="",
        uvrange="",
        antenna="",
        observation="",
        intent="",
        datacolumn="corrected",
        imagename=img_filename,
        imsize=imsize,
        cell=cell,
        phasecenter=phasecenter,
        stokes='I',
        specmode="mfs",
        gridder="standard",
        mosweight=True,
        deconvolver="hogbom",
        pbcor=True,
        weighting="briggs",
        robust=0.5,
        niter=nit,
        gain=0.1,
        threshold=thresh,
        interactive=False
    )
