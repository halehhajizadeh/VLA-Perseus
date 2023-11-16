#to run this script, you need to put your data in a directory named 'data' and put the script inside another directory named 'scripts'
#
import os
import sys
import tarfile
import shutil

# working_directory = sys.argv[1]
working_directory = '../data'
# working_directory = '../data/03:36:00.000000_+30.30.00.00001'

def find_ms_folder(directory, startswith='19B-053', endswith=''):
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


def unzip(path: str, endswith: str = ".tar") -> None:
    """
    Unzips the tar file including products

    path (str): The path of ms file which we want to find the tar file
    endswith (str): The ending of the tar file
    """
    for file in os.listdir(path):
        if file.endswith(endswith):
            tarfile_path = os.path.join(path, file)
            with tarfile.open(tarfile_path) as tar:
                tar.extractall(path=path) # specify which folder to extract to



def copy(directory='.', startswith='19B-053', endswith='.ms'):
    """
    Copy the ms file to the products directory

    directory (str): The directory which contains the ms file
    startswith (str): The starting of the ms file
    endswith (str): The ending of the ms file

    returns:
    copy of the ms file to the products directory
    """
    file = find_ms_folder(directory, startswith, endswith)
    print(file)
    splitted_path = file[0].split('/')
    destination = splitted_path[0]+'/'+splitted_path[1]+'/'+splitted_path[2]+'/products/'+splitted_path[3]
    return shutil.copytree(file[0], destination)


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
folders_list = find_ms_folder(working_directory, "19B-053")

print('List of the folders:')
print(folders_list)

#-----------------------------------------------------------------------------------------
ms_file_name = input('Which file do you want to continue with?\n')

# #------------------------------------------------------------------------------------------
# #unzipping the products folder
# unzip(path=ms_file_name, endswith=".tar")
# print('Unzipping the tar file is done!')   

# #unzippng the tables 
# unzip(ms_file_name + '/products', ".caltables.tgz")
# print('Unzipping tables is done!')

# #copy the ms file and its flagversion to products folder    
# copy(directory=ms_file_name,startswith='19B-053',endswith='.ms')
# print('ms file copied to products')
# copy(directory=ms_file_name,startswith='19B-053',endswith='.ms.flagversions')
# print('flagversions copied to products')

# #------------------------------------------------------------------------------------------
# #Change working directory to products
# os.chdir(ms_file_name+ '/products/')
# print(os.getcwd())
# os.makedirs('plots')

# filename = find_ms_folder('.', '19', '.ms')
# filename = filename[0]


#----------------------------------------------------------------------------------------
filename = '/lustre/aoc/observers/nm-12934/VLA-Perseus/data/19B-053_2020_01_11_T03_36_56.543/19B-053.sb37658530.eb37691790.58859.0565694213.ms/'


#print the flaglist to restore
flags_list = flagmanager(vis=filename)
print(flags_list)

flag_version = input('which flagversion do you want to restore?\n')


flagmanager(vis=filename , mode='restore', versionname=flag_version)

flag_dict = flagdata(vis=filename, mode='summary')

count = 0
for i in range(55):
    percantage = flag_dict['field']['PER_FIELD_' + str(i)]['flagged']/ flag_dict['field']['PER_FIELD_' + str(i)]['total']*100     
    # print('PER_FIELD_' + str(i) + ': ' + str(percantage)) 
    if percantage > 60:
        count = count + 1
print('Number of percantages more than 60%: ' + str(count))

yesno = input('Do you want to restore again?\n')

if yesno == 'yes':
    flag_version2 = input('Which flag version do you want to restore again?\n')
    flagmanager(vis=filename , mode='restore', versionname=flag_version2)

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
      spw='1~18')

print('splitting to calibrated file is done!')
#--------------------------------------------------------------------------------------
