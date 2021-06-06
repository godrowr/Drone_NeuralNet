import os
import sys
import subprocess
import socket
import math
import clr
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
RPORT = 9999 #1060       # Port to listen on (non-privileged ports are > 1023)
MAX = 8096 #65535 
CNN = 0 #0 if the system uses the TestCNN, 1 if the system uses the proposed CNN, and 2 if the system uses the SQL database
TEST = 0 #1 if testing without any CNN , 0 if actual use of CNN
global rsock
global BUSY
BUSY = 0
global FLYING
FLYING = 0
global messages
messages = 0


# Safety Settings
max_ground_speed = 1 #m/s
takeoff_throttle = 1360
land_throttle = 1000
pitch_hold = 1520
roll_hold = 1516
yaw_hold = 1500
min_altitude = 0
max_altitude = 2
print ('Start Script')


 
def AltitudeCheck(pre_alt):
    curr_alt = cs.alt
    if (curr_alt > min_altitude and curr_alt < max_altitude):
        print("Altitude OK")
        return 1
    return 0
    
    #Returns the channel 1, 2, 3, and 4
def get_ChannelsOut():
    return cs.ch1out, cs.ch2out, cs.ch3out, cs.ch4out
    
def get_ChannelsIn():
    return cs.ch1out, cs.ch2out, cs.ch3out, cs.ch4out

def TakeOff_Action():
    global FLYING
    throttle = cs.ch3out
    previous_alt = 0
    #print("Take off action")
    try:
        FLYING = 1
        while throttle < takeoff_throttle: 
            Script.Sleep(50)
            throttle = throttle + 10
            Script.SendRC(1, 1500, True)
            Script.SendRC(2, 1500, True)
            Script.SendRC(4, 1500, True)
            Script.SendRC(3, throttle, True)
        Script.Sleep(1000)
        Script.SendRC(5,1500,False)
    except Exception as e:
        print("Error: Drone Can't Take off")
        print(e.__class__)
        rsock.close()
        sys.exit()     
    else:
        #print("Take off action complete")
        Hold()
        
def Land_Action():
    global FLYING
    #print("Land action")
    try:
        throttle = takeoff_throttle
        FLYING = 0
        while throttle > land_throttle:
            throttle = throttle - 10  
            Script.SendRC(1, 1500, True)
            Script.SendRC(2, 1500, True)
            Script.SendRC(4, 1500, True)
            Script.SendRC(3, throttle, True)
        Script.Sleep(1000)
    except Exception as e:
        print("Error: Drone Can't Take off")
        print(e.__class__)
        rsock.close()
        sys.exit()  
        

def YawLeft_Action():
    #print('Yaw Left Action')
    #Script.ChangeMode("Loiter")
    Script.SendRC(4,1410,True) # throttle back to land
    Script.Sleep(1000) # 1 sec 
    Script.SendRC(4,1500,True) # stabilize
    Hold()
    #print('Yaw Left Action complete')
    
def YawRight_Action():
    #print('Yaw Right Action')
    #Script.ChangeMode("Loiter")
    Script.SendRC(4,1700,True) # throttle back to land
    #Script.Sleep(1000) # 1 sec 
    #print('Yaw Right Action complete')




###################################################

def Left_Action():
    #print('Left Action')
    Script.SendRC(1,1400,True) 
    Script.Sleep(100) # 1 sec rolling right
    Script.SendRC(1,Script.GetParam('RC1_TRIM'),True)
    #Script.SendRC(5,2000,True) # stabilize
    Hold()
    #print('Left Action complete')
    
def Right_Action():
    #print('Right Action')
    Script.SendRC(1,1600,True)
    Script.Sleep(10) # 1 sec rolling left
    Script.SendRC(1,Script.GetParam('RC1_TRIM'),True)
    #Script.SendRC(5,2000,True) # stabilize
    Hold()
    #print('Right Action complete')

def Forward_Action():
    print('Forward Action')
    Script.SendRC(2,1300,True)
    Script.Sleep(100) # 0.1 sec pitch down
    Script.SendRC(2,Script.GetParam('RC2_TRIM'),True)
    Script.SendRC(5,2000,True) # stabilize
    Hold()
    print('Forward Action complete')
    
def Back_Action():
    print('Back Action')
    Script.SendRC(2,1600,True)
    Script.Sleep(100) # 0.1 sec pitch up
    Script.SendRC(2,Script.GetParam('RC2_TRIM'),True)
    Script.SendRC(5,2000,True) # stabilize
    Hold()
    print('Back Action complete')

def Up_Action():
    print('Up Action')
    throttle = cs.chx3in
    print(throttle)
    Script.SendRC(3,throttle + 25,True)
    Script.Sleep(100)
    Script.SendRC(3,Script.GetParam('RC3_TRIM'),True)
    Script.SendRC(5,2000,True) # stabilize
    Script.Sleep(2000) # 2 sec to stabilize
    Hold()
    
    print('Up Action complete')
    
def Down_Action():
    print('Down Action')
    Script.SendRC(5,1500,True) # stabilize
    Script.SendRC(3,takeoff_throttle - 15,True) # throttle back to land
    Script.Sleep(2000) # 2 sec to stabilize
    Hold()
    print('Down Action complete')
    
    
# Flight Fine Control methods
def ThrottleUp():
    print('Throttle Up')
    Script.SendRC(5,1500,True) # stabilize
   
def ThrottleDown():
    print('Throttle Down')
    Script.SendRC(5,1500,True) # stabilize

 
def PitchUp():
    print('Pitch Up')
    Script.SendRC(5,1500,True) # stabilize


def PitchDown():
    print('Pitch Down')
    Script.SendRC(5,1500,True) # stabilize

  
def RollRight():
    print('Roll Right')
    Script.SendRC(5,1500,True) # stabilize

    
def RollLeft():
    print('Roll Left')
    Script.SendRC(5,1500,True) # stabilize


def YawRight():
    print('Yaw Right')
    Script.SendRC(4,1600,True) # stabilize

    
def YawLeft():
    print('Yaw Left')
    Script.SendRC(4,1400,True) # stabilize
    

def Hold():
    print('Holding')
    Script.SendRC(1, 1500, True)
    Script.SendRC(2, 1500, True)
    Script.SendRC(4, 1500, True)
    
    #Script.ChangeMode("Loiter")


def handleFlightAction(command):
    if command == "L":
        Turn90_Action()
    #elif command == "C":
    #    Turn180_Action()
    elif command == "right" or command == "TwoRight":
        YawRight_Action() 
    elif command == "left" or command == "TwoLeft":
        YawLeft_action()
    #elif command == "RockOn":
    #    if cs.alt < 0.5:
    #        TakeOff_Action()
    #elif command == "SpockDown":
    #    Back_Action()
    #elif command == "SpockUp":
    #    Forward_Action()
    #elif command == "SpockRight":
    #    Right_Action()
    #elif command == "SpockLeft":
    #    Left_Action()
    elif (command == "Thumbsdown" or command == "thumbs-down" ):
        if FLYING == 1:
            Land_Action()
        else:
            print("Drone is not in flight")
    elif (command == "Thumbsup" or command == "thumb-up" ):
        if FLYING == 0:
            TakeOff_Action()
        else:
            print("Drone is in flight")
    #elif command == "Swing":
    #    while cs.alt > 0:
    #        Land_Action()
    else:
        Hold()
    

def handleFlightControls(command):
    if (command == "FistForward" or command == "fist-forward" ):
        PitchDown()
    elif (command == "Fist" or command == "fist-up"):
        PitchUp()
    #elif command == "Okay":  
        #Armable()
    #elif command == "One Down":
        #Down_Action()
    #elif command == "One":
        #Up_Action()
    elif (command == "PalmLeft" or command == "left" ):
        donothing = 0
        #RollLeft()
    elif (command == "PalmRight" or command == "right" ):
        donothing = 0
        #RollRight()
    elif (command == "Thumbsdown" or command == "thumb-down" ):
        ThrottleDown()
    elif (command == "Thumbsup" or command == "thumb-up" ):
        ThrottleUp()
    elif command == "TwoLeft":
        YawLeft()
    elif command == "TwoRight":
        YawRight()
    else:
        Hold()

    

def delimit(message):
    if (CNN == 2):
        data = message.split(',')
        command = data[-1]
    elif (CNN == 1):
        implemented = 0
    elif (CNN == 0):
        data = message.split(' ')
        command = data[0]
        command = command.split("'")[1]
        conf = data[1]
    return command, conf
    
def handleCommunication(rsock):
    command = " "
    conf = " "
    print('Listening at ' , rsock.getsockname())
    #keystroke = Script.waitKey(1) & 0xFF
    while 1:
        prevcommand = command
        print("Waiting to recv")
        
        msg, addr = rsock.recvfrom(8096)
        
        command, conf = delimit(repr(msg))
        #print(command)
        #print(conf)
        #if TEST == 0:
        #    if not cs.armed:
        #        Land_Action()
        
        #if command == "Palm": # TODO or keyboard.is_pressed('s'):
        #    print("Stopping")
        #    Hold()
        #    break
        #else:
    #try: 
        #if TEST == 0:
        #    roll, pitch, throttle, yaw = get_ChannelsIn()
        #    print("Throttle: " + throttle)
        FaultDetection(command, conf, prevcommand)
    #except Exception as e:
    #    print("Error: Drone failed after response")
    #    print(e.__class__)
    #    rsock.close()
    #    sys.exit()  
    #else:
    #    donothing = 0
            

            

def FaultDetection(command, conf, prevcommand):
    #This method checks for faults, too many commands in short order, low confidence, and handles reassurance. 
    global BUSY
    global FLYING
    global messages
    # Command Variance 

    # Fault 2 - Too many different commands in very short order
    if (prevcommand == command and conf > 88):
        #print("+1")
        messages = messages + 1
    else:
        #print("set to zero")
        messages = 0
        Hold()

    # Fault 4 - Reassure that command is really the command that the user wants to act on, 
    # wait for 10 messages to arrive. 
    
    if FLYING == 0 and not command == "thumb-up" and TEST == 0:
        #print("set to zero")
        messages = 0
    
    if FLYING == 1:
        Script.SendRC(3, takeoff_throttle, True)
        
    
    #if BUSY == 1:
    #    print("BUSY")
    #else:
    #    print("FREE")
    
    #print(messages)
    # High confidence actions wont be received more than 15 times, more than that and the command is 
    # most likely not even a hand. 
    if messages > 10 and BUSY == 0:
        if TEST == 1:
            print("Preforming action:", command)
            print(conf)
        else: 
        #try:
            print("-----------------")
            print("Preforming: " + command)
            #print(conf)
            BUSY = 1
            #print("BUSY")
            Script.Sleep(2000)
            handleFlightAction(command)
            #roll, pitch, throttle, yaw = get_ChannelsIn()
            #roll0, pitch0, throttle0, yaw0 = get_ChannelsOut()
            #print("Roll (in): " + roll + " | Roll (out): " + roll0)
            #print("Pitch (in): " + pitch + " | Pitch (out): " + pitch0)
            #print("Throttle (in):" + throttle + " | Throttle (in):" + throttle0)
            #print("Yaw (in):" + yaw + " | Yaw (out):" + yaw0)
            print("----------------")
            messages = 0
        #except Exception as e:
        #    print("Error: Drone failed at response inside Fault Detection")
        #    print(e.__class__)
        #    rsock.close()
        #    sys.exit()  
        #else: 
            #print("FREE")
            BUSY = 0
                

    

def main():
    print('Please Arm the Drone in 5 seconds')
    if TEST == 1:
        print("TESTING initiated")
    else: 
        Script.Sleep(10000)
        if not cs.armed:
            print("Drone is not armed!?")
            sys.exit()  
    
    rsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #SOCK_STREAM SOCK_DGRAM
    rsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listenaddr = (HOST,RPORT)
    try:     
       rsock.bind(listenaddr) 
    except socket.error, errmsg:
       print('Bind failed. Error Code:')
       sys.stderr.write("[ERROR] %s\n" % errmsg[1])
       rsock.close()
       sys.exit()  

    print 'Receive Socket bind complete on ' + str(RPORT)
   
    if TEST == 0:
        for chan in range(1,9):
            Script.SendRC(chan,1500,False)
            Script.SendRC(3,Script.GetParam('RC3_MIN'),True)
        print('Parameters Acquired')
        print(cs.alt)
    

    # Fault 6 - Loss of communication results in hold and break
    while 1:
    #try:
        handleCommunication(rsock)
    #except Exception as e:
    #    print("Error: Handling communication")
    #    print(e.__class__)
    #    rsock.close()
    #    sys.exit()  
        #else:
        #    continue
        
    rsock.close()
        
    print('Please Manually disarm the Drone')

main()