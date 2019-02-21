import stream
from math_boat import get_output
from base import get_position, get_imu

import time 




def main():
	#declare default level acceleration parameters
	defx = 0.0
	defy = 0.0
	defz = -1.0
	height=0
	delta=0
	start=time.time()
	try:
		while True:
			if delta>2:
				#start blynk stream 
				stream.blynk.run()

				#fetch position and imu data 
				position=get_position()
				print(position)
				imu=get_imu()

				#fetch user input parameters
				user_input=stream.get_input()
				
				#update level accelerations
				if user_input[0]==True:
					defx=imu[0]
					defy=imu[1]
					defz=imu[2]

				#update rover height
				if user_input[1]>0:
					height=user_input[1]

				#calculate output parameters with data 
				output_packet=get_output(position[0], position[1], position[2], imu[0], imu[1], imu[2], defx, defy, defz, height)
				print(output_packet)

				stream.send_data(output_packet[0], output_packet[1], output_packet[2],position[3],position[0], position[1],output_packet[3])

				delta=0
				start=time.time()
			else:
				delta=time.time()-start

	except KeyboardInterrupt:
		streamer.close()
		pass



if __name__ == '__main__':
	main()

	
