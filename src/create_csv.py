#!/usr/bin/env python
import rospy
from math import sin, cos, pi
import numpy as np


#Kuka youbot joints
joint_names = [
   "arm_joint_1",
   "arm_joint_2",
   "arm_joint_3",
   "arm_joint_4",
   "arm_joint_5",
   "caster_joint_fl",
   "wheel_joint_fl",
   "caster_joint_fr",
   "wheel_joint_fr",
   "caster_joint_bl",
   "wheel_joint_bl",
   "caster_joint_br",
   "wheel_joint_br",
   "gripper_finger_joint_l",
   "gripper_finger_joint_r",
]

#Barret wam7 joints
#joint_names = [
#     "wam/base_yaw_joint",
#     "wam/shoulder_pitch_joint",
#     "wam/shoulder_yaw_joint",
#     "wam/elbow_pitch_joint",
#     "wam/wrist_yaw_joint",
#     "wam/wrist_pitch_joint",
#     "wam/palm_yaw_joint"
#     ]

# universal ur5 joints 
# joint_names = [
#     "shoulder_pan_joint",
#     "shoulder_lift_joint",
#     "elbow_joint",
#     "wrist_1_joint",
#     "wrist_2_joint",
#     "wrist_3_joint"
#     ]

#trep demo robot
# joint_names = [
#      "joint1",
#      "joint2"
#      ]


DT = 0.1
TF = 10.0

j1func = lambda t: 0.75*sin(t) + 2.95
j2func = lambda t: 0.3*sin(2*t) + 1.35
j3func = lambda t: 0.2*sin(2*t) - 2.59
j4func = lambda t: 0.4*sin(t)

tvec = np.arange(0,TF+DT,DT)
dat = np.zeros((len(tvec), len(joint_names)+1))
# write headers:
for i,t in enumerate(tvec):
    tmpdat = np.zeros(len(dat[i]))
    tmpdat[0] = t
    tmpdat[1] = j1func(t)
    tmpdat[2] = j2func(t)
    tmpdat[3] = j3func(t)
    tmpdat[4] = j4func(t)
    dat[i] = tmpdat

# fd = open("/home/jarvis/me495_indigows/src/kinematics_animation/data/jointstates.csv",'w')
head = 'time,' + ','.join(joint_names)
np.savetxt("jointstates.csv", dat, header=head, comments="", delimiter=',', fmt="%3.6f")

