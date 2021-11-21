import base64
import logging
import time
import os
from PIL import Image

import cv2
import numpy as np
import roslibpy

# Configure logging
fmt = '%(asctime)s %(levelname)8s: %(message)s'
logging.basicConfig(format=fmt, level=logging.INFO)
log = logging.getLogger(__name__)

# client = roslibpy.Ros(host='127.0.0.1', port=9090)
client = roslibpy.Ros(host='10.42.0.1', port=9090)

def readb64(data):
nparr = np.frombuffer(base64.b64decode(data), np.uint8)
return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

i = 0
height = 0
width = 0

blank_image = np.zeros((480,640,3), dtype = np.uint8)
opencvImage = cv2.cvtColor(blank_image, cv2.COLOR_RGB2BGR)
# cv2.imshow("WindowNameHere", opencvImage)

def cam_info(info):
global height
global width
height = info['height']
width = info['width']
# print(info)
# print(height)
# print(width)

def receive_image(msg):
global i
global opencvImage
log.info('Received image seq=%d', msg['header']['seq'])
decoded_data = base64.b64decode(msg['data'])
np_data = np.frombuffer(decoded_data,np.uint8)
image = np.fromstring(np_data, np.uint8).reshape( height, width, 3 )
opencvImage = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

i = i + 1
filename = "images/image_" + str(i) + ".jpg"
gr_im = Image.fromarray(image).save(filename)
# cv2.imshow("WindowNameHere", opencvImage)
# print(opencvImage)




subscriber2 = roslibpy.Topic(client, '/camera_rear_node/image_raw', 'sensor_msgs/CameraInfo')
subscriber2.subscribe(cam_info)

# subscriber = roslibpy.Topic(client, '/camera/color/image_raw', 'sensor_msgs/Image')
subscriber = roslibpy.Topic(client, '/camera_rear_node/image_raw', 'sensor_msgs/Image')
subscriber.subscribe(receive_image)

client.run_forever()
cv2.waitKey(0)
cv2.destroyAllWindows()
