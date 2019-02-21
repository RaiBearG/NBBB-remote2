
import datetime, BlynkLib


# Import the ISStreamer module
from ISStreamer.Streamer import Streamer

today = str(datetime.datetime.date(datetime.datetime.now()))
#define streaming bucket
streamer = Streamer(bucket_name=today, bucket_key=today, access_key="mygB9VqjZIzp4AJmQEZOTJl6mOdQlwUm")

BLYNK_AUTH = '8e3613ac6bda4b30a6fae2c18df0ab13'


height=0
calibrate=False

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

blynk.virtual_write(0, "              RAMP POSITION left- right+")
blynk.virtual_write(7, "Need help with the app ? \n -Contact Tim at timg@nicholsboats.com or 817-371-1679\n -To contact the developer email raigohalwar@gmail.com or call 778-683-3126\n")


@blynk.VIRTUAL_WRITE(5)
def v5_write_handler(value):
    print('Height of Rover: {}'.format(value[0]))
    global height 
    height=float(value[0])
    return

@blynk.VIRTUAL_WRITE(6)
def v6_write_handler(value):
    print('Calibrate: {}'.format(value[0]))
    global calibrate
    if(int(value[0])==1):
    	calibrate=True
    else:
    	calibrate=False
    return


def initial_state(dist, howfarout, fix, sats, lat, lon, tilt):
	streamer.log("Distance from Centre (inches)", dist)
	streamer.log("Distance out (ft)", howfarout)
	streamer.log("Latitude", lat)
	streamer.log("Longitude", lon)
	streamer.log("GPS Fix", fix)
	streamer.log("Number of Sattelites", sats)
	streamer.log("Boat Tilt angle (degrees)", tilt)
	return

def app(dist,howfarout, fix, sats, lat, lon, tilt):
	blynk.virtual_write(1, dist)
	blynk.virtual_write(2,fix)
	blynk.virtual_write(3, howfarout)
	blynk.virtual_write(9, tilt)
	blynk.virtual_write(4, sats)
	blynk.virtual_write(10, lat)
	blynk.virtual_write(11, lon)

	return 


def send_data(dist,howfarout, fix, sats, lat, lon, tilt):
	initial_state(dist,howfarout, fix, sats, lat, lon, tilt)
	app(dist,howfarout, fix, sats, lat, lon, tilt)
	return 

def get_input():
	return calibrate, height





