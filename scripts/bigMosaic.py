import os
import tarfile
import shutil

working_directory = '../data_new/'
# working_directory = '../data/'

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

def extract_specific_file(tar_filename, file_to_extract, extract_to_path):
    with tarfile.open(tar_filename, 'r') as tar:
        for member in tar.getmembers():
            if member.name == file_to_extract:
                tar.extract(member, extract_to_path)
                break

def phase_center(ms_folder_name):
    with open('./phasecenter/phasecenter_results.txt', 'r') as txt_file:
        lines = txt_file.readlines()
        for line in lines:
            items = line.split()
            if items[0] == ms_folder_name:
                phase_center_value = str(items[1]) +' '+ str(items[2])  +' '+ str(items[3])  
    return phase_center_value      

mslist = find_ms_folder (working_directory, startswith='19B-053', endswith='')
print(mslist)



for msfolder in mslist:
    

    msfile = find_ms_folder(msfolder, '19', '.ms')
    msfile = msfile[0]
    print(msfile)
    msfilename = msfile.split('/')

    phase_center_value =phase_center(msfolder.split('/')[-1])
    print('phase center is = ' + phase_center_value)

    tclean(vis=msfile,
        field="3~57",
        spw="16:5~55",
        timerange="",
        uvrange="",
        antenna="",
        observation="",
        intent="",
        datacolumn="corrected",
        imagename=working_directory+"/Images/"+str(msfilename[-2]),
        imsize=[4096],
        cell="2.5arcsec",
        phasecenter=phase_center_value,
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
        parallel=False,
        interactive=False)



    exportfits(working_directory+"/Images/"+str(msfilename[-2])+".image", working_directory+"/Images/"+str(msfilename[-2])+".image.fits")
