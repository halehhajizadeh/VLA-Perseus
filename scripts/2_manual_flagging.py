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
    field='0521+166=3C138',
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
 #-------------------------------------------------------------------
elif threedigits=='59-933':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )  

 #-------------------------------------------------------------------
elif threedigits=='684':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12,13'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='14, 15'
    )  

#-------------------------------------------------------------------
elif threedigits=='543':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='0, 7, 9, 10, 11, 12, 13, 14'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='5,46,47'
    )

 #-------------------------------------------------------------------
elif threedigits=='447':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,13'
    )
    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='22,27,28,29,30,37'
    )

#-------------------------------------------------------------------
elif threedigits=='362':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )

#-------------------------------------------------------------------
elif threedigits=='102':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12'
    )
    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='2:7~9;25;59;60,3:6~10;19;20;26,5:14~18;41;51;52,6:49~51',
    )

#-------------------------------------------------------------------
elif threedigits=='263':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7'
    )
  
    flagdata(
        vis=msfilename, 
        mode='manual',
        scan='45,46,53,35,37,59'
        )
    

#-------------------------------------------------------------------
elif threedigits=='208':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11'
    )
    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='27,28,48,53,46,45,44,52,54,37,47,59,35,36,51,58,43'
    )

#-------------------------------------------------------------------
elif threedigits=='587':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    scan='9,43,56,44,45,46,53,58,59,54,37,52,35'
    )

    #-------------------------------------------------------------------
elif threedigits=='482':

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='7,9,10,11,12,13,14'
    )

    flagdata(
    vis=msfilename, 
    mode='manual',
    spw='15:3;4;7;12;14;16;21;42;56;44;25;46;36;28;40;60;59'
    )