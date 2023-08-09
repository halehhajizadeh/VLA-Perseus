import sys
sys.path.append('.')
from configs import msfilename, threedigits

if threedigits=='546':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='0:19~32'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    spw='3:0~5'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    spw='0:0~8'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    spw='12'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    spw='15:12~15'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    field = '0',
    spw='9,11,7'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    field = '0',
    spw='15:7~8;14~27'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    field = '0',
    spw='17:14~15;33~35'
    )

    flagdata( 
    vis=msfilename, 
    mode='manual', 
    field = '3~58',
    spw='0'
    )
#----------------------------------------------------------------
if threedigits=='755':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='1,7,9,11,12,13,14'
    )

  

