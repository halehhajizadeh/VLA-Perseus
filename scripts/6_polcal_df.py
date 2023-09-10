import sys
sys.path.append('.')
from configs import msfilename, refant_name

#if we have an instrumental polarization calibrator that we know is unpolarized, we run polcal with poltype=’Df

polcal(vis=msfilename,
       caltable=msfilename+'.Df_sbd',
       field='0542+498=3C147',
       scan = '',
       spw='',
       refant=refant_name,
       poltype='Df',
       solint='inf,2MHz',
       combine='scan',
       gaintable=[msfilename+'.Kcross_sbd'],
       gainfield=[''],
	append=False
       )


