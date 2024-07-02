import sys
sys.path.append('.')
import time
import os
import numpy as np


def find_calibrated_files(base_directory):
    calibrated_files = []

    # Traverse through all directories and subdirectories
    for root, dirs, files in os.walk(base_directory):
        for directory in dirs:
            if directory.startswith('19B-053'):
                products_path = os.path.join(root, directory, 'products')
                if os.path.exists(products_path):
                    for file in os.listdir(products_path):
                        if file.startswith('19B-053') and file.endswith('_calibrated_working.ms'):
                            calibrated_files.append(os.path.join(products_path, file))
    return calibrated_files

# Specify the base directory
base_directory = '../data/19B-053_2020_01_21_T08_37_05.970/'

# Get the list of calibrated files
ms_file = find_calibrated_files(base_directory)

for i in range (54):

        tclean(vis=ms_file,
        field='PER_FIELD_'+str(i),       
        imagename='./selfcal/PER_FIELD_'+str(i)+'_r1',
        stokes='I',
        specmode='mfs',
        deconvolver='mtmfs',
        imsize=[4096],
        cell= '2.5arcsec',
        weighting='briggs',
        robust=0.5,
        niter=700,
        gridder='standard',
        savemodel='modelcolumn',
        usepointing=False,
        rotatepastep=5.0,
        nterms=2,
        pbcor=True,
        nsigma=5,
        wbawp=True,
        conjbeams=True,
        pblimit=-0.01,
        )

        gaincal(vis=ms_file, field='PER_FIELD_'+str(i), caltable='./selfcal/pcal_1_f'+str(i),solint='int',calmode='p',gaintype='G')
        applycal(vis=ms_file, field='PER_FIELD_'+str(i), gaintable='./selfcal/pcal_1_f'+str(i))


        tclean(vis=ms_file,
        field='PER_FIELD_'+str(i),       
        imagename='./selfcal/PER_FIELD_'+str(i)+'_r2',
        stokes='I',
        specmode='mfs',
        deconvolver='mtmfs',
        imsize=[4096],
        cell= '2.5arcsec',
        weighting='briggs',
        robust=0.5,
        niter=1200,
        gridder='standard',
        savemodel='modelcolumn',
        usepointing=False,
        rotatepastep=5.0,
        nterms=2,
        pbcor=True,
        nsigma=5,
        wbawp=True,
        conjbeams=True,
        pblimit=-0.01,
        )

        gaincal(vis=ms_file, field='PER_FIELD_'+str(i), caltable='./selfcal/pcal_r2_f'+str(i),solint='int',calmode='p',gaintype='G')
        bandpass(vis=ms_file, caltable='./selfcal/bpcal_r1_f'+str(i), gaintable='./selfcal/pcal_r2_f'+str(i),field='PER_FIELD_'+str(i),bandtype='B',solint='int')
        applycal(vis=ms_file, field='PER_FIELD_'+str(i), gaintable=['./selfcal/pcal_r2_f'+str(i), './selfcal/bpcal_r1_f'+str(i)])


        flagdata(vis=ms_file, datacolumn='residual', mode='tfcrop')

        tclean(vis=ms_file,
        field='PER_FIELD_'+str(i),       
        imagename='./selfcal/PER_FIELD_'+str(i)+'_r3',
        stokes='I',
        specmode='mfs',
        deconvolver='mtmfs',
        imsize=[4096],
        cell= '2.5arcsec',
        weighting='briggs',
        robust=0.5,
        niter=1700,
        gridder='standard',
        savemodel='modelcolumn',
        usepointing=False,
        rotatepastep=5.0,
        nterms=2,
        pbcor=True,
        nsigma=5,
        wbawp=True,
        conjbeams=True,
        pblimit=-0.01,
        )


####################################################################################


tclean(vis=ms_file,
field='J0336+3218',       
imagename='./selfcal/J0336+3218_r1',
stokes='I',
specmode='mfs',
deconvolver='mtmfs',
imsize=[4096],
cell= '2.5arcsec',
weighting='briggs',
robust=0.5,
niter=700,
gridder='standard',
savemodel='modelcolumn',
usepointing=False,
rotatepastep=5.0,
nterms=2,
pbcor=True,
nsigma=5,
wbawp=True,
conjbeams=True,
pblimit=-0.01,
)

gaincal(vis=ms_file, field='PER_FIELD_'+str(i), caltable='./selfcal/pcal_r1_J0336+3218',solint='int',calmode='p',gaintype='G')
applycal(vis=ms_file, field='PER_FIELD_'+str(i), gaintable='./selfcal/pcal_r1_J0336+3218')


tclean(vis=ms_file,
field='J0336+3218',       
imagename='./selfcal/J0336+3218_r2',
stokes='I',
specmode='mfs',
deconvolver='mtmfs',
imsize=[4096],
cell= '2.5arcsec',
weighting='briggs',
robust=0.5,
niter=1200,
gridder='standard',
savemodel='modelcolumn',
usepointing=False,
rotatepastep=5.0,
nterms=2,
pbcor=True,
nsigma=5,
wbawp=True,
conjbeams=True,
pblimit=-0.01,
)

gaincal(vis=ms_file, field='J0336+3218', caltable='./selfcal/pcal_r2_J0336+3218',solint='int',calmode='p',gaintype='G')
bandpass(vis=ms_file, caltable='./selfcal/bpcal_r1_f'+str(i), gaintable='./selfcal/pcal_r2_J0336+3218',field='J0336+3218',bandtype='B',solint='int')
applycal(vis=ms_file, field='J0336+3218', gaintable=['./selfcal/pcal_r2_J0336+3218', './selfcal/bpcal_r1_J0336+3218'])


flagdata(vis=ms_file, datacolumn='residual', mode='tfcrop')

tclean(vis=ms_file,
field='J0336+3218',       
imagename='./selfcal/J0336+3218_r3',
stokes='I',
specmode='mfs',
deconvolver='mtmfs',
imsize=[4096],
cell= '2.5arcsec',
weighting='briggs',
robust=0.5,
niter=1700,
gridder='standard',
savemodel='modelcolumn',
usepointing=False,
rotatepastep=5.0,
nterms=2,
pbcor=True,
nsigma=5,
wbawp=True,
conjbeams=True,
pblimit=-0.01,
)