import rospy
from math import isnan
from math import pi
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
land = rospy.ServiceProxy('land', Trigger)
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)

r = rospy.Rate(5)

navigate(x=0, y=0, z=1.5, speed=0.5, frame_id='body', auto_arm=True)
rospy.sleep(3)
z = 1.5
while(True):
    navigate(x=0, y=0, z=1.5-z, speed=0.5, frame_id='body')
    z = 1.5
    if isnan(get_telemetry(frame_id='aruco_15').z):
        rospy.sleep(0.2)
        pass

    z = get_telemetry(frame_id='aruco_15').z
    while(z >= 0.5):
	set_position(x=0, y=-0.15, z=z, yaw=pi*0.5, frame_id='aruco_15')
        z = z - 0.03
        if (z <= 0.5):
            break
        if isnan(get_telemetry(frame_id='aruco_15').z) == True:
            break
        r.sleep()

    if isnan(get_telemetry(frame_id='aruco_9').z):
        pass

    while(z <= 0.5):
        set_position(x=0, y=0, z=z, yaw=pi*0.5, frame_id='aruco_9')
        z = z - 0.03
        if (z <= 0.15):
            break
        if (isnan(get_telemetry(frame_id='aruco_9').z) == True):
            break
        r.sleep()

    if z <= 0.15:
        navigate(x=0, y=0, z=-1, speed=2, frame_id='body')
        rospy.sleep(0.5)
        arming(False)
        break
