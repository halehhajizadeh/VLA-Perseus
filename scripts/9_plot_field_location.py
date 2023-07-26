import sys
sys.path.append('.')
import matplotlib.pyplot as plt
import numpy as np
import os

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

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

for ms_folder in mslist:
    #This file is a text file with each line being the name of your field, the RA as 'hh:mm:ss.sss' and Dec as 'dd.mm.ss.ssss' of the center of the source separated by tabs, I have an example if you need it. The data is from listobs
    f='./phasecenter/'+str(ms_folder.split('/')[-1])+'_radecs.txt'
    l=open(f)
    data=l.readlines()

    ID=[]
    ra_raw=[]
    dec_raw=[]

    for d in data:
        dat_split=d.split()
        ID.append(dat_split[0])
        ra_raw.append(dat_split[1])
        dec_raw.append(dat_split[2].split('\n')[0])
    print(ID)
    print(ra_raw)
    print(dec_raw)
    ra_deg=[]
    for r in ra_raw:
        ra_split=r.split(':')
        ra_h=ra_split[0]
        ra_m=ra_split[1]
        ra_s=ra_split[2]
        if float(ra_h) > 0:
            ra=(float(ra_h)+float(ra_m)/60+float(ra_s)/3600)*15
        else:
            ra=(float(ra_h)-float(ra_m)/60-float(ra_s)/3600)*15
        ra_deg.append(ra)
        
    dec_deg=[]
    for c in dec_raw:
        dec_split=c.split('.', 2)
        dec_d=dec_split[0]
        dec_m=dec_split[1]
        dec_s=dec_split[2]
        if float(dec_d) > 0:
            dec=float(dec_d)+float(dec_m)/60+float(dec_s)/3600
        else:
            dec=float(dec_d)-float(dec_m)/60-float(dec_s)/3600
        dec_deg.append(dec)


    plt.rc('text',usetex=True)
    plt.rc('font',family='serif')

    plt.figure(1)

    plt.subplot(111)

    fig, ax = plt.subplots()

    ax.plot(ra_deg, dec_deg, 'b.')
    ax.set_xlabel(r'RA (deg)',fontsize=15)
    ax.set_ylabel(r'DEC (deg)',fontsize=15)
    ax.tick_params(axis='x',labelsize=14)
    ax.tick_params(axis='y',labelsize=14)
    ax.set_title(str(ms_folder))

    for i, txt in enumerate(ID):
        ax.annxotate(txt, (ra_deg[i], dec_deg[i]))

    fig.savefig('./phasecenter/'+str(ms_folder.split('/')[-1])+'.png')

