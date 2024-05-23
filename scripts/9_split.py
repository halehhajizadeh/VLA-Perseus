import sys
sys.path.append('.')
from configs import msfilename, path
import os
import shutil

directory_path = path + "/targets.ms"

if os.path.exists(directory_path) and os.path.isdir(directory_path):
    shutil.rmtree(directory_path)

flagversions_path = directory_path + ".flagversions"

if os.path.exists(flagversions_path) and os.path.isdir(flagversions_path):
    shutil.rmtree(flagversions_path)

print('splitting is starting...')

split(vis=msfilename,
      outputvis=path+'/targets.ms',
      datacolumn='corrected',
      field='PER_FIELD_*, J0336+3218'
      )
print('splitting targets is done!')



statwt(vis=path+'/targets.ms',datacolumn='corrected',minsamp=8)