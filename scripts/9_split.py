import sys
sys.path.append('.')
from configs import msfilename, path
import os
import shutil

directory_path = path + "/targets.ms"

if os.path.exists(directory_path):
    os.remove(directory_path)
    shutil.rmtree(directory_path)

if os.path.exists(directory_path):
    os.remove(directory_path+".flagversions")
    shutil.rmtree(directory_path+".flagversions")

print('splitting is starting...')

split(vis=msfilename,
      outputvis=path+'/targets.ms',
      datacolumn='corrected',
      field='PER_FIELD_*, J0336+3218'
      )
print('splitting targets is done!')



statwt(vis=path+'/targets.ms',datacolumn='data',minsamp=8)