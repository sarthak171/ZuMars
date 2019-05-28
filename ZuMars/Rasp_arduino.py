import serial
import pygame
import time


ser = serial.Serial('/dev/ttyACMO',9600)
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
end = True
joystick.init()
pygame.init()

while True:
	time.sleep(1)
	pygame.event.get()
	turn = int(joystick.get_axis(2)*1000)
	if(turn>0):
		turn = 1
	elif(turn<0):
		turn = 2
	else:
		turn = 0
	forward = int(joystick.get_axis(1)*1000)
	if(forward>0):
		forward = 2000
	elif(forward<0):
		forward = 0
	ser.write(str(int(turn))+'t')

	print(ser.readline())
	turn = 1000
	forward = 1000
	



