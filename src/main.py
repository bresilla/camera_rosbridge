from __future__ import print_function
import roslibpy

client = roslibpy.Ros(host='10.191.58.38', port=9090)
client.run()

x = 0.0
y = 0.0
theta = 0.0
lv = 0.0
av = 0.0

def callback(msg):
    global x
    x = int(msg["x"])
    global y
    global theta
    global lv
    global av
    print(msg)

listener = roslibpy.Topic(client, '/turtle1/pose', 'turtlesim/msg/Pose')
listener.subscribe(callback)

try:
    while True:
        pass
except KeyboardInterrupt:
    client.terminate()
