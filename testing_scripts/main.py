import time
import subprocess
import datetime


def adb_cmd():

    cmd_list  = ['adb', 'devices']
    #adb command to execute
    cmd_list  = ['adb', 'shell','dumpsys','location']
    #do the command
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE)
    out, err = process.communicate()
    #trim the output
    try:
        out = str(out)[str(out).find("Last Known Locations"):str(out).find("Geofences")]
    except: #if it fails, then ignore it
        print("error in finding last known in gps return")
        return ""

    out = out.replace("\\n","\n")
    out = out.replace('  ','')

    print(str(out))
    #print(type(out))

    return out

def log(info):
    #get timestamp
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    with open("gps_logs.txt","a") as logs:
        logs.write(timestamp+"\n"+info)
        logs.close()

def init_log():
    with open("gps_logs.txt","w") as logs:
        logs.write("")
        logs.close()


#wipes log
init_log()

count = 0
short = True
while True:
    if short and (count >= 20):
        break
    count+=1
    #gets info from phone
    gps_info = adb_cmd()
    #logs info to file
    log(gps_info)
    #wait 1 second
    time.sleep(1)
