path = '../data/19B-053_2019_12_15_T07_36_56.546/products/'
filename = path + '19B-053.sb37264871.eb37595549.58832.22860825231_calibrated.ms'

polcal(vis=filename,
       caltable=path+'19B-053.sb37264871.eb37595549.58832.22860825231_calibrated'+'.Df_sbd',
       field='0',
       scan = '2,3',
       spw='',
       refant='ea08',
       poltype='Df',
       solint='inf,2MHz',
       combine='scan',
       gaintable=[path+'19B-053.sb37264871.eb37595549.58832.22860825231_calibrated'+'.Kcross_sbd'],
       gainfield=[''],
	append=False
       )


