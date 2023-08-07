import sys
sys.path.append('.')
from configs import msfilename, refant_name

kcross_sbd = msfilename+".Kcross_sbd" 

gaincal(vis=msfilename,
    caltable=kcross_sbd,
    field='1',
    scan = '',
    spw='',
    refant=refant_name,
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
