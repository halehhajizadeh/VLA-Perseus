import sys
sys.path.append('.')
from configs import msfilename

polcal(vis=msfilename,
       caltable=msfilename+'.Df_sbd',
       field='0',
       scan = '2,3',
       spw='',
       refant='ea08',
       poltype='Df',
       solint='inf,2MHz',
       combine='scan',
       gaintable=[msfilename+'.Kcross_sbd'],
       gainfield=[''],
	append=False
       )


