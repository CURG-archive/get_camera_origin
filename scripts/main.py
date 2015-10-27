#!/usr/bin/env python
import rospy
import numpy as np
import tf_conversions
import tf
from get_camera_origin.srv import *


def handle(request):
    rospy.loginfo("received get camera origin request")
    
    world_transform = get_world_transform()
    camera_origin = None
    rospy.loginfo("world transform: " + str(world_transform))

    p = geometry_msgs.msg.Pose()
    if world_transform != None:
        camera_origin = np.linalg.inv(world_transform)[0:3, 3]*1000
        p.orientation.w = 1
        p.position.x = camera_origin[0]
        p.position.y = camera_origin[1]
        p.position.z = camera_origin[2]

    rospy.loginfo("camera_pose: " + str(camera_origin))
    
    return p


def get_world_transform():
    transform_listener = tf.TransformListener()
    try:
        transform_listener.waitForTransform("/camera_rgb_optical_frame", "/world", rospy.Time(0), rospy.Duration(10))
    except:
        rospy.logwarn("Failed to get world transform for: ")
        return None
    world_transform = tf_conversions.toMatrix(tf_conversions.fromTf(
            transform_listener.lookupTransform(
            "/camera_rgb_optical_frame", '/world', rospy.Time(0))))
    return world_transform


def get_camera_origin_server():
    rospy.init_node('get_camera_origin')
    rospy.loginfo("about to init node")
    s = rospy.Service('get_camera_origin', GetCameraOrigin, handle)
    rospy.loginfo("Get Camera Origin Node inited..")
    rospy.spin()

if __name__ == "__main__":
    print "In Main"
    rospy.loginfo("In Main")
    get_camera_origin_server()
