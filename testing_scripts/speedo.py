import gpsd

gpsd.connect()

packet = gpsd.get_current()

last_speed = -1

while True:
    packet = gpsd.get_current()
    speed = packet.speed()
    speed = float(speed) * 2.237
    speed = round(speed)
    if speed != last_speed:
        print("speed: "+str(speed))
    last_speed = speed

