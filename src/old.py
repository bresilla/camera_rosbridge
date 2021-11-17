import roslibpy

client = roslibpy.Ros(host='10.42.0.1', port=9090)
# client.run()

print('Is ROS connected?', client.is_connected)

tops = client.get_topics()
tops.sort()

for e in tops:
    print(e)
