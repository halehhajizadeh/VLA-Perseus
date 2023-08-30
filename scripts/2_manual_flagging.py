import sys
sys.path.append('.')
from configs import msfilename, threedigits

if threedigits=='546':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='0:0~8;19~32'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    spw='3:0~5'
    )


    flagdata( 
    vis=msfilename, 
    mode='manual', 
    spw='7,9,11,12'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    field = '0',
    spw='15:7~8;12~27'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    field = '0',
    spw='17:14~15;33~35'
    )
#----------------------------------------------------------------
elif threedigits=='775':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='1,12,13,14'
    )

    flagdata(
    vis=msfilename,
    field= '3~58',
    mode='manual',
    spw='12:30~60'
    )
  

