path = '../data/19B-053_2019_12_15_T07_36_56.546/products/'
filename = path + '19B-053.sb37264871.eb37595549.58832.22860825231_calibrated.ms'

applycal(vis=filename,
         field='',
		 flagbackup=True,
         gaintable=[path+'19B-053.sb37264871.eb37595549.58832.22860825231_calibrated.Kcross_sbd',
                    path+'19B-053.sb37264871.eb37595549.58832.22860825231_calibrated.Df_sbd',
                    path+'19B-053.sb37264871.eb37595549.58832.22860825231_calibrated.Xf_sbd'
                    ],
         gainfield=['','',''],
         interp=['','',''],
		 applymode='calflagstrict',
         antenna='*&*',
		 spw='',
		 spwmap=[],
		 calwt=[False,False,False],
         parang=True)         

print('applycal is done!')
print('--------------------------------')
print('splitting is starting...')

split(vis=filename,
      outputvis=path+'targets.ms',
      datacolumn='corrected',
      field='3~58')

print('splitting targets is done!')