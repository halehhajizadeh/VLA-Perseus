import sys
sys.path.append('.')
from configs import msfilename, path


print('splitting is starting...')

split(vis=msfilename,
      outputvis=path+'/targets.ms',
      datacolumn='corrected',
      field='J0336+3218,PER_FIELD_*')
print('splitting targets is done!')



statwt(vis=path+'/targets.ms',datacolumn='data',minsamp=8)