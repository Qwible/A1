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

def avoidance():
    debug_print('avoid')
    desiredDistance = 100

    # set the motor variables
    mb = ev3.LargeMotor('outB') #left motor 
    mc = ev3.LargeMotor('outC') #right motor

    # set the ultrasonic sensor variable
    leftSensor = ev3.UltrasonicSensor('in3')
    rightSensor = ev3.UltrasonicSensor('in2')

    Kp = -1
    Ki = -1
    Kd = -1

    previousError = integral = derivative = 0
    


    lastError = 0


    leftIntegral = 0
    rightIntegral = 0
    
    leftSensorDistance = leftSensor.value()
    rightSensorDistance = rightSensor.value()



    while ((leftSensorDistance<100) or (rightSensorDistance<100)):
        initialTime = time.time() #gets the current time

        if (leftSensorDistance<100) and (rightSensorDistance<100):
            currentError = leftSensorDistance - rightSensorDistance
            integral = (2/3)*integral + currentError 
            derivative = currentError - previousError #change in error 
            pid= (Kp * currentError) + (Ki * integral) + (Kd * derivative) # PID
            pid = pid/10

            sp = -80
            if pid > 40:
                pid = 40
            if pid < -40:
                pid = -40
            if pid > -5 and pid < 5:
                pid=0
            
            ml.run_direct(duty_cycle_sp=sp+(2/4*pid))
            mr.run_direct(duty_cycle_sp=sp-(2/4*pid))
            
            previousError = currentError

        else:
            leftCurrentError = desiredDistance -  leftSensorDistance 
            rightCurrentError = desiredDistance -  rightSensorDistance


            leftMotorSpeed = (Kp * leftCurrentError)
            rightMotorSpeed = (Kp * rightCurrentError)

            debug_print('LEFT:'+leftMotorSpeed)
            debug_print(+'RIGHT:'+rightMotorSpeed)

            if (leftMotorSpeed > 100):
                leftMotorSpeed = 100
            elif (leftMotorSpeed<-100):
                leftMotorSpeed=-100

            if (rightMotorSpeed > 100):
                rightMotorSpeed = 100
            elif (rightMotorSpeed<-100):
                rightMotorSpeed=-100

            
            mb.run_direct(duty_cycle_sp=leftMotorSpeed)
            mc.run_direct(duty_cycle_sp=rightMotorSpeed)

        waitPeriod = 0.07 - (time.time() - initialTime)
        time.sleep(waitPeriod)

        leftSensorDistance = leftSensor.value()
        rightSensorDistance = rightSensor.value()


       



        
        



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

    while True:
        debug_print("NEW SEARCH DIRECTION")
        t = random.uniform(0, 1.2)
        mb.run_direct(duty_cycle_sp=100)
        mc.run_direct(duty_cycle_sp=-100)
        time.sleep(t)

        mb.run_direct(duty_cycle_sp= -100)
        mc.run_direct(duty_cycle_sp= -100)

        s = rejection()*5
        debug_print(s)
        ss = s//0.1
        ss = int(ss)
        for x in range(ss):
            leftSensorDistance = leftSensor.value()
            rightSensorDistance = rightSensor.value()
            if ((leftSensorDistance<100) or (rightSensorDistance<100)):
                debug_print('AVOIDING')
                avoidance()
                debug_print('DONE AVOIDING')
                break
            time.sleep(0.1)
        
        
                

        


    

        

    
            



   


    

if __name__ == '__main__':
    main()