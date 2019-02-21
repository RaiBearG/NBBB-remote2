"""
Extracts latitude, longitude, sattelite count, and imu
data from sbp messages received back form the rover over
the radio link.

Send that data over the callback IP 
""" 

from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_POS_LLH, MsgPosLLH
from sbp.imu import SBP_MSG_IMU_RAW, MsgImuRaw

SERIAL_PORT_IN = '/dev/ttyACM0'
SERIAL_BAUD_IN = 115200


def get_position():
	with PySerialDriver(SERIAL_PORT_IN, baud=SERIAL_BAUD_IN) as driver:
		with Handler(Framer(driver.read, None, verbose=True)) as source:
			try:
				for msg, metadata in source.filter(SBP_MSG_POS_LLH):
					pos = msg.lat, msg.lon, msg.flags, msg.n_sats
					break
			except KeyboardInterrupt:
				pass
	return pos

def get_imu():
	with PySerialDriver(SERIAL_PORT_IN, baud=SERIAL_BAUD_IN) as driver:
		with Handler(Framer(driver.read, None, verbose=True)) as source:
			try:
				for msg, metadata in source.filter(SBP_MSG_IMU_RAW):
					rate = msg.acc_x/4095.75, msg.acc_y/4095.75, msg.acc_z/4095.75
					break
			except KeyboardInterrupt:
				pass
	return rate


