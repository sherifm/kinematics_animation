#!/bin/bash

win1=Rviz
win2='Joint State Publisher'
for i in {1..3}
do
    echo "checking for window existence... "${i}
    exist1=`wmctrl -l |grep -c "${win1}"`
    exist2=`wmctrl -l |grep -c "${win2}"`
    if  (( $exist1 == 1 )) && (( $exist2 == 1 ))
	then 
	echo "window exists!"
	break
    else
	sleep 1
    fi
done

###############
# MOVIE SIZE: #
###############
# # rgb window:
# wmctrl -r /camera/rgb/image_color -e 0,1600,0,400,250
# # depth window:
# wmctrl -r /camera/depth/image -e 0,2000,0,400,250
# # move the demo window:
# wmctrl -r skeleton_interface.py -e 0,1600,275,800,300


#########################
# EXTERNAL MONITOR SIZE #
#########################
# rgb window:
# wmctrl -r /camera/rgb/image_color -e 0,1600,0,800,600
wmctrl -r $win1 -e 0,0,0,1400,1080
# depth window:
wmctrl -r $win2 -e 0,1500,0,400,600

exit 0