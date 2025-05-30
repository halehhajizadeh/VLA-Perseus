import sys
sys.path.append('.')
from configs import msfilename, path

applycal(vis=msfilename,
         field='',
		 flagbackup=True,
         gaintable=[msfilename+'.Kcross_sbd',
                    msfilename+'.Df_sbd',
                    msfilename+'.Xf_sbd'
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
