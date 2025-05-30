import sys
sys.path.append('.')
from configs import msfilename, refant_name

# This cross-hand delay can be estimated using the gaintype=’KCROSS’ mode of gaincal (in this case,
# using the strongly polarized source 3C286)


kcross_sbd = msfilename+".Kcross_sbd" 

gaincal(vis=msfilename,
    caltable=kcross_sbd,
    field='0521+166=3C138',
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
