#!/usr/bin/env python
import rospy
from math import sin, cos, pi
import numpy as np
from scipy.interpolate import interp1d
from sensor_msgs.msg import JointState


class KinematicsAnimator( object ):
    def __init__(self):
        freq = rospy.get_param("~freq", 50)
        rospy.loginfo("Publishing frequency = "+str(freq))
        fname = rospy.get_param("~file", None)
        if fname is None:
            rospy.logerr("Must provide private param '~file'")
            rospy.signal_shutdown("No CSV file provided")
        else:
            rospy.loginfo("Animation file = "+fname)
        self.rate = rospy.get_param("~rate", 1.0)
        rospy.loginfo("Time scaling = " + str(self.rate))
        # load data:
        with open(fname, 'r') as f:
            fline = f.readline()
        self.names = fline.rstrip('\r\n').split(',')
        self.names = self.names[1:]
        self.dat = np.loadtxt(fname, skiprows=1, delimiter=',')
        self._fint = interp1d(1/float(self.rate)*self.dat[:,0], self.dat[:,1:], kind='linear', axis=0)
        self.base_time = rospy.Time.now()
        # create publisher:
        self.state_pub = rospy.Publisher("joint_states", JointState, latch=True, queue_size=3)
        # create timer:
        self.pbtimer = rospy.Timer(rospy.Duration(1/float(freq)), self.timercb)
        return

    def timercb(self, time_dat):
        t = (rospy.Time.now() - self.base_time).to_sec()
        try :
            q = self._fint(t)
        except ValueError:
            q = self._fint(self._fint.x[-1])
            if (t - self._fint.x[-1]) > 2.0:
                rospy.loginfo("Resetting animation!")
                self.base_time = rospy.Time.now()
        js = JointState(name=self.names, position=q)
        js.header.stamp = rospy.Time.now()
        self.state_pub.publish(js)
        return


def main():
    rospy.init_node("animating_csv_files", log_level=rospy.INFO)
    
    try:
        animator = KinematicsAnimator()
    except rospy.ROSInterruptException:
        pass
    rospy.spin()

    

if __name__ == '__main__':
    main()
