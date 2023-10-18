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
    spw='1,7,9,11,12,13,14'
    )

    flagdata(
    vis=msfilename,
    field= '3~58',
    mode='manual',
    spw='12:30~60'
    )

#----------------------------------------------------------------  
elif threedigits=='933':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )

#----------------------------------------------------------------
elif threedigits=='627':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )

#----------------------------------------------------------------

elif threedigits=='198':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,14'
    )
    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='35,36'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    filed='0521+166=3C138',
    channel='11,14,20~30;36~42,'
    )
 #-------------------------------------------------------------------
elif threedigits=='861':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )   

 #-------------------------------------------------------------------
elif threedigits=='076':
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12,14'
    )  

 #-------------------------------------------------------------------
elif threedigits=='228':
    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='48'
    )
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )  
    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='8'
    )

 #-------------------------------------------------------------------
elif threedigits=='672':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12,13'
    )  
    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='27,30'
    )  
