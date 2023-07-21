import os
import tarfile
import shutil

working_directory = '../data_new'

def find_ms_folder(directory, startswith='19B-053', endswith=''):
    """
    Finds names of ms files in a directroy.

    directory (str): The directory to search
    startswith (str): The beginning of the file to searchs
    endswith (str): The end of the file to search

    Returns:
    str : An array including the name of the ms files found.
    """
    folders_list = []
    for file in os.listdir(directory):
        if file.startswith(startswith):
            if file.endswith(endswith):
                folders_list.append(os.path.join(directory, file))                
    return(folders_list)




mslist = find_ms_folder (working_directory, startswith='19B-053', endswith='')
print(mslist)



for msfolder in mslist:
    msfilename = find_ms_folder(msfolder, '19', '.ms')
    msfilename = msfilename[0]
    print(msfilename)

    tclean(vis=msfilename,
        field="3~58",
        spw="16:5~55",
        timerange="",
        uvrange="",
        antenna="",
        observation="",
        intent="",
        datacolumn="corrected",
        imagename=working_directory+"/Images/"+str(msfilename),
        imsize=[4096],
        cell="2.5arcsec",
        # phasecenter=phase_center,
        stokes="I",
        projection="SIN",
        specmode="mfs",
        gridder="mosaic",
        mosweight=True,
        cfcache="",
        pblimit=0.06,
        normtype="flatnoise",
        deconvolver="hogbom",
        restoration=True,
        restoringbeam=[],
        pbcor=True,
        outlierfile="",
        weighting="briggs",
        robust=0.5,
        npixels=2,
        uvtaper=[],
        niter=10,
        gain=0.1,
        threshold=1e-4,
        nsigma=0.0,
        cycleniter=-1,
        cyclefactor=1.0,
        restart=True,
        calcres=True,
        calcpsf=True,
        parallel=True,
        interactive=False)



    exportfits(working_directory+"/Images/"+str(msfilename)+".image", working_directory+"/Images/"+str(msfilename)+".image.fits")
