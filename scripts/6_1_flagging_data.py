import sys
sys.path.append('.')
from configs import msfilename, refant_name

flagdata(vis=msfilename, 
        mode='clip',
        correlation='ABS_ALL',
        clipminmax=[0.0, 0.25],
        datacolumn='CPARAM',
        clipoutside=True,
        action='apply',
        flagbackup=False,
        savepars=False)