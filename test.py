from IP_Cam_python import Camera

ip = input("-> Type your camera's IP: ")

initial_position = 0
cam = Camera(ip)

cam.goto_position(initial_position)
cam.set_position(initial_position)