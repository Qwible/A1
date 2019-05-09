#!/usr/bin/env python3
'''COM2009-3009 EV3DEV TEST PROGRAM'''

# Connect left motor to Output C and right motor to Output B
# Connect an ultrasonic sensor to Input 3

import os
import sys
import time
import ev3dev.ev3 as ev3
import statistics
import math
import random

# state constants
ON = True
OFF = False

def Average(lst): 
    return sum(lst) / len(lst) 

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):
    '''Sets the console font
    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)


def rejection():
    while True:
       x = random.uniform(0,1)
       y = random.uniform(0,1.5)
       fx = math.sqrt(1/(2*math.pi))*math.exp(-1/(2*x))/(x**1.5)
       if fx > y:
           break
    return x

def beaconing(mb, mc, lightSensor, oldLightValue):
    debug_print("STARTED BEACONING")
    # set the motor variables
    mb.run_direct(duty_cycle_sp=-50)
    mc.run_direct(duty_cycle_sp=-50)
    time.sleep(0.3)
    mb.run_direct(duty_cycle_sp= 0)
    mc.run_direct(duty_cycle_sp= 0)

    currentLightValue = lightSensor.value()
    if checkBeconing(oldLightValue, currentLightValue):
        debug_print("AFTER MOVING, EV3 GOT CLOSER TO THE LIGHT")
        mb.run_direct(duty_cycle_sp=-50)
        mc.run_direct(duty_cycle_sp=-50)
        time.sleep(0.5)
        mb.run_direct(duty_cycle_sp= 0)
        mc.run_direct(duty_cycle_sp= 0)
        beaconing(mb,mc,lightSensor,lightSensor.value())
    else:
        debug_print("ADJUSTING BEACONING, DIDNT MOVE CLOSER")
        # adjustBeaconing(mb, mc, lightSensor, oldLightValue)
        # debug_print("STOPPING BEACONING, DIDNT MOVE CLOSER")
  
        
def adjustBeaconing(mb, mc, lightSensor, oldLightValue, ci=0):
    if (ci == 0):
        mb.run_direct(duty_cycle_sp=-50)
        mc.run_direct(duty_cycle_sp=-25)
        currentLightValue = lightSensor.value()

        if checkBeconing(oldLightValue, currentLightValue):
            beaconing(mb,mc,lightSensor,lightSensor.value())

        else:
            adjustBeaconing(mb, mc, lightSensor, oldLightValue, ci+1)
    
    elif (ci==1):
        mb.run_direct(duty_cycle_sp=-25)
        mc.run_direct(duty_cycle_sp=-150)
        currentLightValue = lightSensor.value()
        if checkBeconing(oldLightValue, currentLightValue):
            beaconing(mb,mc,lightSensor,lightSensor.value())
        else:
            debug_print("STOPPING BEACONING, DIDNT MOVE CLOSER")



def checkBeconing(oldLightValue, currentLightValue):
    if (currentLightValue > oldLightValue):
        return True
    else:
        return False

# def randomWalk(mb, mc, leftSensor, rightSensor):
#         debug_print("NEW SEARCH DIRECTION")
#         t = random.uniform(0, 1.2)
#         mb.run_direct(duty_cycle_sp=100)
#         mc.run_direct(duty_cycle_sp=-100)
#         time.sleep(t)

#         mb.run_direct(duty_cycle_sp= -100)
#         mc.run_direct(duty_cycle_sp= -100)

#         s = rejection()*5
#         debug_print(s)
#         ss = s//0.1
#         ss = int(ss)
#         for x in range(ss):
#             time.sleep(0.1)
                

def avoidance(mb, mc, leftSensor, rightSensor):
        speed = -75


        leftSensorDistance = leftSensor.value()
        rightSensorDistance = rightSensor.value()
        if (leftSensorDistance < 100):
            mb.run_direct(duty_cycle_sp=0)
            mc.run_direct(duty_cycle_sp=speed)
            time.sleep(0.5)
            mb.run_direct(duty_cycle_sp=0)
            mc.run_direct(duty_cycle_sp=0)            

        elif (rightSensorDistance < 100):
            mb.run_direct(duty_cycle_sp=speed)
            mc.run_direct(duty_cycle_sp=0)
            time.sleep(0.5)
            mb.run_direct(duty_cycle_sp=0)
            mc.run_direct(duty_cycle_sp=0) 

# def avoidance():
#     debug_print('avoid')
    # desiredDistance = 100
    # leftFeedbackSignal = 0
#     rightFeedbackSignal = 0

#     # set the motor variables
#     mb = ev3.LargeMotor('outB') #left motor 
#     mc = ev3.LargeMotor('outC') #right motor

#     # set the ultrasonic sensor variable
#     leftSensor = ev3.UltrasonicSensor('in3')
#     rightSensor = ev3.UltrasonicSensor('in2')

#     Kp = 1.5
#     Ki = 0
#     Ku = 0
#     Kd = 0


#     # timePeriod = 0.1
#     timePeriod = 0.25

#     lastError = 0

#     rightCurrentError = 1000
#     leftCurrentError = 1000

#     leftIntegral = 0
#     rightIntegral = 0
    
#     leftSensorDistance = leftSensor.value()
#     rightSensorDistance = rightSensor.value()
#     debug_print(leftSensorDistance)
#     debug_print(rightSensorDistance)

#     while ((leftSensorDistance<100) or (rightSensorDistance<100)):
#         debug_print("loop")
#         initialTime = time.time() #gets the current time

#         leftCurrentError = desiredDistance - leftFeedbackSignal #(r-b)
#         rightCurrentError = desiredDistance - rightFeedbackSignal #(r-b)

#         # leftIntegral = leftIntegral +(leftCurrentError*timePeriod)
#         # leftDerivative = (leftCurrentError - leftLastError)/timePeriod

#         # rightIntegral = rightIntegral +(rightCurrentError*timePeriod)
#         # rightDerivative = (rightCurrentError - rightLastError)/timePeriod    


#         leftMotorSpeed = (Kp * leftCurrentError) #+ (Ki*integral) + (Kd*derivative)
#         rightMotorSpeed = (Kp * rightCurrentError)
        
#         # debug_print("U: ", u)
#         debug_print("Left Current error: ", leftCurrentError)
#         debug_print("Right Current error: ", rightCurrentError)

#         # us = u
#         # debug_print("US: ", us)

#         if (leftMotorSpeed > 100):
#             leftMotorSpeed = 100
#         elif (leftMotorSpeed<-100):
#             leftMotorSpeed=-100

#         if (rightMotorSpeed > 100):
#             rightMotorSpeed = 100
#         elif (rightMotorSpeed<-100):
#             rightMotorSpeed=-100

        
#         mb.run_direct(duty_cycle_sp=leftMotorSpeed)
#         mc.run_direct(duty_cycle_sp=rightMotorSpeed)
#         waitPeriod = 0.07 - (time.time() - initialTime)
#         time.sleep(waitPeriod)

#         leftSensorDistance = leftSensor.value()
#         rightSensorDistance = rightSensor.value()

#         leftFeedbackSignal = leftSensorDistance
#         rightFeedbackSignal = rightSensorDistance

       



        
        



def main():
    '''The main function of our program'''

    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font('Lat15-Terminus24x12')


    # set the motor variables
    mb = ev3.LargeMotor('outB') #left motor 
    mc = ev3.LargeMotor('outC') #right motor

    # set the ultrasonic sensor variable
    leftSensor = ev3.UltrasonicSensor('in3')
    rightSensor = ev3.UltrasonicSensor('in2')
    lightSensor = ev3.ColorSensor('in1')
    lightSensor.mode='COL-AMBIENT'

    while True:
        x = 1

        # s = rejection()*5
        # debug_print(s)
        # mb.run_direct(duty_cycle_sp= -100)
        # mc.run_direct(duty_cycle_sp= -100)
        # time.sleep(s)
        # mb.run_direct(duty_cycle_sp= 0)
        # mc.run_direct(duty_cycle_sp= 0)


        # leftSensorDistance = leftSensor.value()
        # rightSensorDistance = rightSensor.value()
        # lightValue = lightSensor.value()



        t = random.uniform(0, 1.2)
        leftSensorDistance = leftSensor.value()
        rightSensorDistance = rightSensor.value()
        
        mb.run_direct(duty_cycle_sp=75)
        mc.run_direct(duty_cycle_sp=-75)
        time.sleep(t)

        mb.run_direct(duty_cycle_sp= 0)
        mc.run_direct(duty_cycle_sp= 0)

        s = rejection()*5
        debug_print(s)
        ss = s//0.1
        ss = int(ss)
        for x in range(ss):
            lightValue = lightSensor.value()

            leftSensorDistance = leftSensor.value()
            rightSensorDistance = rightSensor.value()

            if ((leftSensorDistance<100) or (rightSensorDistance<100)):
                    debug_print('AVOIDING')
                    avoidance(mb, mc, leftSensor, rightSensor)
            elif (lightValue > 20):
                debug_print('THE ROBOT HAS STOPPED AS ITS CLOSE TO THE LIGHT')
                input("Press Enter to continue...")
            elif (lightValue > 14):
                beaconing(mb, mc, lightSensor,lightValue)
            else:
                mb.run_direct(duty_cycle_sp= -100)
                mc.run_direct(duty_cycle_sp= -100)
                time.sleep(0.1)
                mb.run_direct(duty_cycle_sp= 0)
                mc.run_direct(duty_cycle_sp= 0)
     

        # else if (LIGHT):
        #     beaconing()
    

        

    
            



   


    

if __name__ == '__main__':
    main()