path = '../data/19B-053_2019_12_15_T07_36_56.546/products/'
filename = path + '19B-053.sb37264871.eb37595549.58832.22860825231_calibrated.ms'

polcal(
    vis=filename,
    caltable=path+'19B-053.sb37264871.eb37595549.58832.22860825231_calibrated'+'.Xf_sbd',
    spw='',
    field='1',
    solint='inf,2MHz',
    combine='scan',
    poltype='Xf',
    refant='ea08',
    gaintable=[path+'19B-053.sb37264871.eb37595549.58832.22860825231_calibrated'+'.Kcross_sbd',path+'19B-053.sb37264871.eb37595549.58832.22860825231_calibrated'+'.Df_sbd'],
    gainfield=['',''],
    append=False)
