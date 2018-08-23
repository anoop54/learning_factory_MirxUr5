#Learning Factory 2018.
#Author: Anoop Gadhrri & Simran Nijjar

import UrController
import CamController
import time
import urx
import cv2
import numpy as np
import math
import MirController as mir
#rob.movel_tool((0, 0, 0.1, 0, 0, 0), 0.1, 0.1)
#picture_pose = [-0.22226693438130987, 0.12836317970020147, 0.49793821361474033, 0.08154657639822435, 2.02985283250018, 2.32603606980001]

#Global Variable Declaration
global ids
global corners
global rvec
global tvec
global myur
global cam
global rob

def main():
    global ids
    global corners
    global rvec
    global tvec
    global myur
    global cam
    global rob
    
    rob = urx.Robot("10.0.2.64")
    rob.set_tcp((0, 0, 0, 0, 0, 0))
    
    myur = UrController.MyUR()
    cam = CamController.cam()
    
    if(cam.doOperation() != 0):
        ids,corners,rvec,tvec = cam.doOperation()
        print(tvec)


#want 0.07514064436138192
def kanban_pickup_valve_drop_off():
    register_clear(5)
    mir.append_mission()
    while(mir.register_get(2) != 1):
        print("Waiting")
        time.sleep(0.5)
    kanban_pick_up()
    mir.register_write(1,1)
    myur.Bin_Position()
    while(mir.register_get(2) != 0):
        print("Waiting")
    dropoff_()
    myur.UR2_Start()

    
def register_clear(x):
    for i in range(x):
        mir.register_write(i,0)
        time.sleep(0.1)


def CalibPlaneAngle():
    ids,corners,rvec,tvec = take_picture()

    y1 = [1,0,0]
    rotmat = cv2.Rodrigues(rvec)
    y2 = y1*rotmat[0]
    y2 = [y2[0][0],y2[1][0],y2[2][0]]

    print(y2)
    ang = angle(y1,y2)
    ###deg = ang
    print(ang*(180/math.pi))

    if(ang>0.08 or ang<-0.08):
        if(y2[2]>0):            
            print("-" + str(ang))
            rob.rz += ang
            #rob.movel_tool(((math.sin(ang)*distance(tvec))/1000, 0, 0, 0, 0, 0), 0.1, 0.1)
        else:            
            print(str(ang))
            rob.rz += -ang
            #rob.movel_tool((-(math.sin(ang)*distance(tvec))/1000, 0, 0, 0, 0, 0), 0.1, 0.1)


def check_plane_angle():
    y1 = [1,0,0]
    rotmat = cv2.Rodrigues(rvec)
    y2 = y1*rotmat[0]
    y2 = [y2[0][0],y2[1][0],y2[2][0]]

    ang = angle(y1,y2)
    deg = ang*(180/math.pi)
    return deg


def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


def length(v):
  return math.sqrt(dotproduct(v, v))


def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))


def kanban_pick_up():
    myur.TakePic()

    if(take_picture() == 0):
        search_all()
        kanban_pick_up()
    else:
        if(take_picture() != 0):
            calibXnY()
            rob.movel_tool((0, 0, 0.28, 0, 0, 0), 0.1, 1)
            CalibPlaneAngle()
            calibXnY()
            pickUp()

                
def search_all():
    found = 0
    if(found == 0):
        found = searchLeft()

    if(found == 0):
        found = searchRight()

    if(found == 0):
        found = searchDown()

    if(found == 0):
        print("Search: Marker Not Found")
        return found

    if(found == 1):
        print("Search: Marker Found")
        return found


def pickUp():
    take_picture()
    #ids,corners,rvec,tvec = take_picture()
    time.sleep(1.5)
    print("Distance: " + str(distance_to_aruco(tvec)))
    #if(distance_to_aruco(tvec) < 1160):
    if(distance_to_aruco(tvec) < 2275):
        rob.movel_tool((0, 0, (tvec[0][0][2]-10)/1000, 0, 0, 0), 0.1, 1)
        rob.movel_tool((0, 0.08, 0, 0, 0, 0), 0.1, 0.1)
        rob.movel_tool((0, 0, -400/1000, 0, 0, 0), 0.1, 0.05)
    else:
        print("Bin Out Of Reach")

    
#def calibX():
    #take_picture()
    #rob.movel_tool((-(tvec[0][0][0])/1000, 0, 0, 0, 0, 0), 0.1, 1)

    
#def calibY():
    #rob.movel_tool((0,-(tvec[0][0][1])/1000, 0, 0, 0, 0), 0.1, 1)

    
def calibXnY():
    take_picture()
    rob.movel_tool(((-(tvec[0][0][0])/1000), 0, 0, 0, 0, 0), 0.1, 1)
    rob.movel_tool((0,-(tvec[0][0][1])/1000, 0, 0, 0, 0), 0.1, 1)


def dropoff_():
    #myur.KanBanDropOffImagePos()
    myur.Drop_Off_Picture()
    take_picture()
    #take_picture()
    myur.Drop_Off()
    rob.movel_tool(((-(tvec[0][0][0])/1000), 0, 0, 0, 0, 0), 0.1, 1)
    rob.movel_tool((0, 0, (tvec[0][0][2]-450)/1000, 0, 0, 0), 0.1, 1)
    rob.movel_tool((0,-40/1000, 0, 0, 0, 0), 0.1, 1)    
    rob.movel_tool((0,0,-200/1000, 0, 0, 0), 0.1, 1)
    time.sleep(0.5)
    myur.Home()

def searchDown():
    myur.PicTrigger()
    time.sleep(1)
    counter = 0
    
    while(cam.doOperation() == 0 and counter < 10):        
        print("Marker Not Found")
        #time.sleep(1)
        myur.PicTrigger()
        rob.movel_tool((0, -50/1000, 0, 0, 0, 0), 0.1, 0.1)
        counter = counter + 1
        print(counter)
    print("Stop Searching")

    
def searchUp():
    myur.PicTrigger()
    time.sleep(1)
    counter = 0
    
    while(cam.doOperation() == 0 and counter < 10):        
        print("Marker Not Found")
        #time.sleep(1)
        myur.PicTrigger()
        rob.movel_tool((0, 20/1000, 0, 0, 0, 0), 0.1, 0.1)
        counter = counter + 1
        print(counter)
    print("Stop Searching")


def searchRight():
    counter = 0

    while(take_picture() == 0 and counter < 3 ):        
        print("Marker Not Found")
        rob.rz += -0.1
        counter = counter + 1
        print(counter)
        
    if(counter == 3):
        return 0
    else:
        return 1
    print("Stop Searching")


def searchLeft():
    counter = 0
    
    while(take_picture() == 0 and counter < 3):        
        print("Marker Not Found")
        rob.rz += 0.1
        counter = counter + 1
        print(counter)
            
    if(counter == 3):
        return 0
    else:
        return 1
    print("Stop Searching")

   
def take_picture():
    global ids
    global corners
    global rvec
    global tvec
    global myur
    global cam
    global rob
    
    #myur.PicTrigger()
    #time.sleep(2)
    if(cam.doOperation() != 0):
        ids,corners,rvec,tvec = cam.doOperation()
    return cam.doOperation()


def distance(tvec): #distance in meters
    return np.sqrt((tvec[0][0][0]**2) + (tvec[0][0][1]**2)+ (tvec[0][0][2]**2))-.125


def distance_to_aruco(tvec): #distance in meters
    pos = rob.get_pos()
    return np.sqrt((tvec[0][0][0]**2) + (tvec[0][0][1]**2)+ (tvec[0][0][2]**2))-.125 + np.sqrt(((pos[0]*1000)**2) + ((pos[1]*1000)**2)+ ((pos[2]*1000)**2))
