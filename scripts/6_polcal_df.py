import sys
sys.path.append('.')
from configs import msfilename, refant_name

polcal(vis=msfilename,
       caltable=msfilename+'.Df_sbd',
       field='0',
       scan = '2,3',
       spw='',
       refant=refant_name,
       poltype='Df',
       solint='inf,2MHz',
       combine='scan',
       gaintable=[msfilename+'.Kcross_sbd'],
       gainfield=[''],
	append=False
       )


