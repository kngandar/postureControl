import serial

ser = serial.Serial('COM3',9600)

try:
	print('Press CTRL+C to quit')
	while True:
		frontR = ser.readline()
		frontL = ser.readline()
		backR = ser.readline()
		backL = ser.readline()
		print(frontR)
		print(frontL)
		print(backR)
		print(backL)
except KeyboardInterrupt:
	print('Quitting...')
	