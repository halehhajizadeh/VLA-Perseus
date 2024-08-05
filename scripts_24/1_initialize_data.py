#to run this script, you need to put your data in a directory named 'data' and put the script inside another directory named 'scripts'
#
import os
import sys
import tarfile
import shutil

# working_directory = sys.argv[1]
working_directory = '../data'

def find_ms_folder(directory, startswith='24A-376', endswith=''):
    """
    Finds names of ms files in a directroy.

    directory (str): The directory to search
    startswith (str): The beginning of the file to search
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




def find_tables(table_kind: str, directory="."):
    """
    finds tables.

    table_kind (str): name of the table
    directory (str): the directory which we will search for tables

    Returns:
    str: the full path and name of the table
    """
    for file in os.listdir(directory):
        if file.endswith(table_kind + ".tbl"):
            return(os.path.join(directory, file))


def table_list():
    """
    Makes a list of tables in order 

    Returns:
    str: the list of tables
    """
    table_lists = []
    table_lists.extend(
        [find_tables('gc'), 
        find_tables('opac'),
        find_tables('rq'),
        find_tables('finaldelay'), 
        find_tables('finalBPcal'), 
        find_tables('averagephasegain'), 
        find_tables('finalampgaincal'), 
        find_tables('finalphasegaincal')]
        )
    return table_lists    

#-----------------------------------------------------------------------------------------
folders_list = find_ms_folder(working_directory, "24A-376")

print('List of the folders:')
print(folders_list)

#-----------------------------------------------------------------------------------------
ms_file_name = input('Which file do you want to continue with?\n')

#------------------------------------------------------------------------------------------
os.chdir(ms_file_name)

filename = find_ms_folder('.', '24A-376', '.ms')
filename = filename[0]



flag_dict = flagdata(vis=filename, mode='summary')


#Restore statwt
print("Restoring statwt is starting...")
flagmanager(vis=filename , mode='restore', versionname='statwt_1')
print("Restoring statwt is done!")

#applycal with parang = False
print("applycal with parang=false is starting...")
applycal(vis=filename ,
         antenna='*&*',
         gaintable=table_list(),
         gainfield=['', '', '', '', '', '', '', ''], 
         interp=['', '', '', '', 'linear,linearflag', '', '', ''], 
         spwmap=[[], [], [], [], [],
         [], [], []], 
         calwt=[False, False, False, False, False, False, False, False], 
         parang=False, 
         applymode='calflagstrict', 
         flagbackup=False)

print('Applycal is done!')         


#Falgging data
flagdata(vis=filename,
         mode='rflag', 
         correlation='ABS_RR,LL', 
         intent='*CALIBRATE*',
         datacolumn='corrected', 
         ntime='scan', 
         combinescans=False,
         extendflags=False, 
         winsize=3, 
         timedevscale=4.0, 
         freqdevscale=4.0,
         action='apply', 
         flagbackup=True, 
         savepars=True)

flagdata(vis=filename,
         mode='rflag', 
         correlation='RL, LR', 
         intent='*CALIBRATE*',
         datacolumn='corrected', 
         ntime='scan', 
         combinescans=False,
         extendflags=False, 
         winsize=3, 
         timedevscale=4.0, 
         freqdevscale=4.0,
         action='apply', 
         flagbackup=True, 
         savepars=True)


flagdata(vis= filename,
         mode='rflag', 
         correlation='ABS_RR,LL', 
         intent='*TARGET*',
         datacolumn='corrected',
         ntime='scan', 
         combinescans=False,
         extendflags=False, 
         winsize=3, 
         timedevscale=4.0, 
         freqdevscale=4.0,
         action='apply', 
         flagbackup=True, 
         savepars=True)

     
flagdata(vis= filename,
         mode='rflag', 
         correlation='RL, LR', 
         field = '',
         datacolumn='corrected',
         ntime='scan', 
         combinescans=False,
         extendflags=False, 
         winsize=3, 
         timedevscale=4.0, 
         freqdevscale=4.0,
         action='apply', 
         flagbackup=True, 
         savepars=True)


flagdata(vis= filename,
         mode='tfcrop', 
         correlation='RR, LL', 
         field = '',
         datacolumn='corrected',
         ntime='scan', 
         combinescans=False,
         extendflags=False, 
         winsize=3, 
         timedevscale=4.0, 
         freqdevscale=4.0,
         action='apply', 
         flagbackup=True, 
         savepars=True)


flagdata(vis= filename,
         mode='tfcrop', 
         correlation='RL, LR', 
         field = '',
         datacolumn='corrected',
         ntime='scan', 
         combinescans=False,
         extendflags=False, 
         winsize=3, 
         timedevscale=4.0, 
         freqdevscale=4.0,
         action='apply', 
         flagbackup=True, 
         savepars=True)



statwt(vis=filename, 
       minsamp=8,
       datacolumn='corrected')


calibrated_file = filename.split('.ms')
calibrated_file = calibrated_file[0] + '_calibrated.ms'

split(vis=filename, 
      outputvis=calibrated_file,
      datacolumn='corrected', 
      spw='1,2,4,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22')

print('splitting to calibrated file is done!')
#--------------------------------------------------------------------------------------
