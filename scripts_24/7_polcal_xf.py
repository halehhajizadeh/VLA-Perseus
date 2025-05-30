import sys
sys.path.append('.')
from configs import msfilename, refant_name

polcal(
    vis=msfilename,
    caltable=msfilename+'.Xf_sbd',
    spw='',
    field='0521+166=3C138',
    solint='inf,2MHz',
    combine='scan',
    poltype='Xf',
    refant=refant_name,
    gaintable=[msfilename+'.Kcross_sbd',msfilename+'.Df_sbd'],
    gainfield=['',''],
    append=False)
