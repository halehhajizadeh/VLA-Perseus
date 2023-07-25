import os

def find_txt(directory):
    files = [file for file in os.listdir(directory) if (file.lower().endswith('.txt'))]
    print(files)
    return files

files_name = find_txt('./phasecenter/')

with open('./phasecenter/phasecenter_results.txt', 'w') as result_file:
    for file in files_name:
        ms_folder = file.replace("_radecs.txt", "")
        print (ms_folder)

        with open('./phasecenter/'+file, 'r') as txt_file:
            ra = []
            dec= []
            lines = txt_file.readlines()
            target_line= lines[29]
            items = target_line.split()

            ra = items[1]
            dec = items[2]
        result_file.write(str(ms_folder) + '\t' + 'J2000 '+ str(ra) +' '+str(dec) + '\n')



