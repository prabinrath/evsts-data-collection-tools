from pypylon import pylon
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rospy
# import cv2

class BaslerCameraNode(object):
    def __init__(self):
        # conecting to the first available camera
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        # Grabing Continusely (video) with minimal delay
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        self.converter = pylon.ImageFormatConverter()
        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        self.br = CvBridge()
        # Node cycle rate (in Hz).
        self.loop_rate = rospy.Rate(30)
        # Publishers
        self.pub = rospy.Publisher('basler_camera/image_raw', Image, queue_size=10)

    def start(self):
        while not rospy.is_shutdown() and self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            # rospy.loginfo('publishing image')
            if grabResult.GrabSucceeded():
                image = self.converter.Convert(grabResult)
                img = image.GetArray()
                # self.pub.publish(self.br.cv2_to_imgmsg(img))
                self.pub.publish(self.br.cv2_to_imgmsg(img))
            grabResult.Release()
            self.loop_rate.sleep()

        # Releasing the resource    
        self.camera.StopGrabbing()
            
if __name__ == '__main__':
    rospy.init_node("basler_camera_node", anonymous=True)
    my_node = BaslerCameraNode()
    my_node.start()
