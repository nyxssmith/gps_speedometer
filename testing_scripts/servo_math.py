"""

    0º 2.5
    90º 7.5
    180º 12.5


"""
def find_closest_value(num,values):
    best_dist_away = 99999
    best_value = None
    for value in values:
        dist_away = abs(num-value)
        #print("value",value,"dist away",dist_away)
        if dist_away < best_dist_away:
            best_dist_away = dist_away
            best_value = value

    return best_value

def set_degree_from_speed(speed):
    speed = float(speed)
    """
    deg mph
    ,0:0
    ,5:10
    ,13:15
    ,20:20
    ,30:25
    ,38:30
    ,45:35
    ,55:40
    ,63:45
    ,72:50
    ,82:55
    ,90:60
    ,100:65
    ,108:70
    ,125:80
    ,143:90
    ,160:100
    ,180:106.5
    
    180
    
    """

    degree_to_speed = {0: 0, 5: 10, 13: 15, 20: 20, 30: 25, 38: 30, 45: 35, 55: 40, 63: 45, 72: 50, 82: 55, 90: 60,
                       100: 65, 108: 70, 125: 80, 143: 90, 160: 100, 180: 106.5}
    degree_to_multiplier = {0: 1,
                            5: 1.1,
                            13: 1.1,
                            20: 1.1,
                            30: 1.2,
                            38: 1.2,
                            45: 1.2,
                            55: 1.2,
                            63: 1.2,
                            72: 1.2,
                            82: 1.2,
                            90: 1.2,
                            100: 1.2,
                            108: 1.2,
                            125: 1.2,
                            143: 1.1,
                            160: 1.1,
                            180: 1}

    #print(degree_to_speed.keys())
    
    closest_value = find_closest_value(speed,degree_to_speed.values())
    for key in degree_to_speed.keys():
        if degree_to_speed[key] == closest_value:
            closest_key = key
            break
    print("speed", speed,"closest key is",closest_key)
    speed_at_key = degree_to_speed[closest_key]
    print("speed at that key is",speed_at_key)
    dist_away = speed-speed_at_key
    print("dist away",dist_away)
    if dist_away < 0:
        pass

    multiplier = degree_to_multiplier[closest_key]
    degree = closest_key + dist_away*multiplier
    #print("speed*1/.5944", speed * (1 / .594444444))
    print("degree to set",degree)
    return degree


def set_degree(degree):
    """
    0 2.5
    90 7.5
    180 12.5



    """
    degree = float(degree)
    print(degree)

    pwm_out = (degree / 45) + 2.5
    duty = degree / 18 + 2.5

    print("pwm out " + str(duty))


while True:
    degree = set_degree_from_speed(input("enter speed"))
    set_degree(degree)
