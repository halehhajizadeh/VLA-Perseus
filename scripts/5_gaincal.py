import sys
sys.path.append('.')
from configs import msfilename

kcross_sbd = msfilename+".Kcross_sbd" 

gaincal(vis=msfilename,
    caltable=kcross_sbd,
    field='0',
    scan = '2,3',
    spw='',
    refant='ea08',
    gaintype="KCROSS",
    solint="inf",
    combine="scan",
    calmode="ap",
    append=False,
    gaintable=[''],
    gainfield=[''],
    interp=[''],
    spwmap=[[]],
    parang=True)
