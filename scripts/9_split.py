import sys
sys.path.append('.')
from configs import msfilename, path
import os

if os.path.exists(path+"/targets.ms"):
    os.remove(path+"/targets.ms") 

print('splitting is starting...')

split(vis=msfilename,
      outputvis=path+'/targets.ms',
      datacolumn='corrected',
      field='PER_FIELD_*, J0336+3218'
      )
print('splitting targets is done!')



statwt(vis=path+'/targets.ms',datacolumn='data',minsamp=8)